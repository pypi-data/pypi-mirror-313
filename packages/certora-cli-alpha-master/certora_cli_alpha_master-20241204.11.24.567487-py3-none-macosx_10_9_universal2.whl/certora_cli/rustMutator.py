#!/usr/bin/env python3

import shutil
import subprocess
import argparse
from pathlib import Path
import logging
import re
import os

from Shared import certoraUtils as Util

rust_mutator_logger = logging.getLogger("rust_mutator")

NUM_MUTANTS = 10

def parse_args() -> argparse.Namespace:
    """
    Parse command-line arguments.

    Returns:
        argparse.Namespace: Parsed arguments containing source_file and mutant_dir.
    """
    parser = argparse.ArgumentParser(
        description=(
            "Run universalmutator on a Rust source file, generate mutants, "
            "and ensure the original file remains unchanged."
        )
    )
    parser.add_argument(
        "--file_to_mutant",
        "-s",
        type=Path,
        required=True,
        help="Path to the Rust source file to mutate (e.g., src/lib.rs)"
    )
    parser.add_argument(
        "--mutants_location",
        "-m",
        type=Path,
        default="mutantsDir",
        help="Directory to store generated mutants (e.g., mutants_output)"
    )
    parser.add_argument(
        "--num_mutants",
        "-n",
        type=int,
        default=NUM_MUTANTS,
        help=f"The upper bound on the number of mutants to generate (default: {NUM_MUTANTS})"
    )
    parser.add_argument(
        "--debug",
        "-d",
        action="store_true",
        help="Enable debug logging"
    )
    return parser.parse_args()


def restore_source(backup_file: Path, file_to_mutant: Path) -> None:
    """
    Restore the original source file from the backup.

    Args:
        backup_file (Path): Path to the backup file.
        file_to_mutant (Path): Path to the original source file.
    """
    rust_mutator_logger.info(f"Restoring the original '{file_to_mutant}' from '{backup_file}'...")
    if Util.restore_backup(backup_file):
        rust_mutator_logger.info(f"Original '{file_to_mutant}' restored successfully.")
    else:
        rust_mutator_logger.warning(f"No backup file '{backup_file}' found. Skipping restoration.")


def clean_temp_files() -> None:
    """
    Remove temporary mutant output files matching the pattern '.um.mutant_output.*'.
    """
    temp_files = Path().glob(".um.mutant_output.*")

    rust_mutator_logger.info("Removing temporary mutant output files...")
    for temp_file in temp_files:
        temp_file.unlink()
        rust_mutator_logger.info(f"Removed: {temp_file}")
    rust_mutator_logger.info("Temporary files removal completed.")


def setup_logger(debug: bool = False) -> None:
    """
    Set up the logger for the Rust Mutator script.

    Args:
        debug (bool): Enable debug logging.
    """
    logging.basicConfig(
        level=logging.DEBUG if debug else logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.StreamHandler()
        ]
    )


def validate_source_file(file_to_mutant: Path) -> None:
    """
    Validate that the source file exists and has a .rs extension.

    Args:
        file_to_mutant (Path): Path to the Rust source file.

    Raises:
        Util.CertoraUserInputError: If validation fails.
    """
    if not file_to_mutant.exists():
        raise Util.CertoraUserInputError(f"Source file '{file_to_mutant}' does not exist.")
    if not file_to_mutant.is_file():
        raise Util.CertoraUserInputError(f"Source file '{file_to_mutant}' is not a file.")
    if file_to_mutant.suffix != ".rs":
        raise Util.CertoraUserInputError(f"Source file '{file_to_mutant}' does not have a .rs extension.")


def validate_mutant_dir(mutants_location: Path) -> None:
    """
    Validate that the mutant directory exists and is empty. If the directory does not exist, create it.

    Args:
        mutants_location (Path): Directory to store generated mutants.

    Raises:
        Util.CertoraUserInputError: If validation fails.
    """
    if mutants_location.exists():
        rust_mutator_logger.debug(f"Mutant directory '{mutants_location}' already exists.")
        # Check if the directory is empty
        if any(mutants_location.iterdir()):
            raise Util.CertoraUserInputError(f"Mutant directory '{mutants_location}' is not empty.")
    else:
        mutants_location.mkdir(parents=True)
        rust_mutator_logger.info(f"Mutant directory '{mutants_location}' created successfully.")


def validate_mutant_count(file_to_mutant: Path, mutants_location: Path, num_mutants: int) -> None:
    """
    Validate that the number of mutants generated is less than or equal to the specified limit.
    If the number of mutants generated is greater than the specified limit, only the first 'num_mutants' mutants will be kept.

    Args:
        file_to_mutant (Path): Path to the original Rust source file.
        mutants_location (Path): Directory containing generated mutants.
        num_mutants (int): Upper bound on the number of mutants to generate.
    """
    # Define the regex pattern to extract the mutant number
    pattern = re.compile(rf"{re.escape(file_to_mutant.stem)}\.mutant\.(\d+)\.rs$")

    # Filter mutants that match the naming pattern and delete the ones exceeding the specified limit
    num_mutants_generated = 0
    for mutant in mutants_location.iterdir():
        match = pattern.match(str(mutant.name))
        if match:
            num_mutants_generated += 1
            if int(match.group(1)) >= num_mutants:
                mutant.unlink()

    if num_mutants_generated == 0:
        raise Util.CertoraUserInputError("No mutants generated. Exiting...")

    rust_mutator_logger.info(f"Number of mutants generated: {num_mutants_generated}")
    if num_mutants_generated < num_mutants:
        rust_mutator_logger.warning(f"Number of mutants generated ({num_mutants_generated}) is less than the specified limit ({num_mutants}).")


def validate_cargo() -> None:
    """
    Validate that the cargo.toml file is in the current working directory.

    Raises:
        Util.CertoraUserInputError: If validation fails.
    """
    if not Path(Util.CARGO_FILE).exists():
        raise Util.CertoraUserInputError(f"'{Util.CARGO_FILE}' not found in the current working directory: {os.getcwd()}")


def validate_mutate_command() -> None:
    """
    Validate that the universalmutator command is available in the PATH.

    Raises:
        Util.CertoraUserInputError: If validation fails.
    """
    if shutil.which("mutate") is None:
        raise Util.CertoraUserInputError("universalmutator command 'mutate' not found in PATH.")


def run_mutate(file_to_mutant: Path, mutants_location: Path, build_command: str, debug: bool = False) -> None:
    """
    Execute the universalmutator command to generate mutants.

    Args:
        file_to_mutant (Path): Path to the Rust source file.
        mutants_location (Path): Directory to store generated mutants.
        build_command (str): Command to execute for each mutant to verify compilation.
        debug (bool): Enable debug logging.
    """
    mutate_command = [
        "mutate",
        str(file_to_mutant),
        "rust",
        "--mutantDir",
        str(mutants_location),
        "--cmd",
        build_command
    ]

    rust_mutator_logger.info("Generating mutants...")
    rust_mutator_logger.debug(f"Running universalmutator with command: {' '.join(mutate_command)}")
    if not debug:
        subprocess.run(mutate_command, check=True, stdout=subprocess.DEVNULL)
    else:
        subprocess.run(mutate_command, check=True)
    rust_mutator_logger.info("Mutation generation completed successfully.")


def run_universal_mutator(file_to_mutant: Path, mutants_location: Path, num_mutants: int = NUM_MUTANTS, debug: bool = False) -> None:
    f"""
    Generate mutants for the specified source file and ensure the original file remains unchanged.

    Args:
        file_to_mutant (Path): Path to the Rust source file.
        mutants_location (Path): Directory to store generated mutants.
        num_mutants (int): Upper bound on the number of mutants to generate (default: {NUM_MUTANTS}).
        debug (bool): Enable debug logging.

    Raises:
        Util.CertoraUserInputError: If any validation fails.
        Exception: For unexpected errors.
    """

    # Define the build command, ensuring it dynamically references the correct source file
    build_command = (
        f'cp MUTANT {file_to_mutant} && '
        'RUSTFLAGS="-C strip=none --emit=llvm-ir" '
        'cargo build --target=wasm32-unknown-unknown --release --features certora'
    )

    try:
        # Set up the logger
        setup_logger(debug)

        # Validate mutate command is available
        validate_mutate_command()

        # Validate cargo.toml is in CWD
        validate_cargo()

        # Validate source file
        validate_source_file(file_to_mutant)

        # Backup the original source file
        rust_mutator_logger.info(f"Backing up '{file_to_mutant}' ...")
        backup_file = Util.create_backup(file_to_mutant)
        if backup_file:
            rust_mutator_logger.info(f"Backing up '{file_to_mutant}' to '{backup_file} succeeded")
        else:
            rust_mutator_logger.warning(f"Backing up '{file_to_mutant}' to '{backup_file} failed")

        # Validate or create mutant directory
        validate_mutant_dir(mutants_location)

        # Run the mutation command
        run_mutate(file_to_mutant, mutants_location, build_command, debug)

        # Make sure the number of mutants generated is less than or equal to the specified limit
        validate_mutant_count(file_to_mutant, mutants_location, num_mutants)

    finally:
        # Restore the original source file
        assert backup_file, "run_universal_mutator: null backup_file"
        Util.restore_backup(backup_file)
        # Clean up temporary files
        clean_temp_files()


if __name__ == "__main__":
    # Parse command-line arguments
    args = parse_args()
    run_universal_mutator(args.file_to_mutant, args.mutants_location, args.num_mutants, args.debug)
