from pathlib import Path
from Shared import certoraUtils as Util
from Mutate import mutateConstants as Constants

# this variable keeps the total number of mutants
TOTAL_MUTANTS = -1


class EmptyMutationReport(Util.CertoraUserInputError):
    pass


def mutant_counter(test_name: str) -> int:
    """
    when we have multiple mutations, each run_mutant() runs in a different process. We would like to show
    the user the progress - how many mutants were sent so far to the server. To keep a single counter we use a file
    under the 'applied_mutants' directory. The file is of the form <test_id>.<current_counter>. The file itself
    is empty. Each time a new mutant is sent to the server the suffix is incremented by one and the new counter is
    sent back to the caller

    :param test_name: test id
    :return: new counter
    """

    if TOTAL_MUTANTS == -1:
        raise Util.ImplementationError("TOTAL_MUTANTS not set")

    Constants.MUTANTS_COUNTER_DIR.mkdir(parents=True, exist_ok=True)
    for file_path in Constants.MUTANTS_COUNTER_DIR.iterdir():

        stem = file_path.stem
        suffix = file_path.suffix[1:]

        if stem == test_name:
            # Parse the counter as an integer
            try:
                new_counter = int(suffix) + 1
                file_path.unlink()
                Path(f"{file_path.with_suffix('.' + str(new_counter))}").touch()
                return new_counter
            except ValueError:
                pass

    # did not find the test_id

    Path(f"{Constants.MUTANTS_COUNTER_DIR}/{test_name}.1").touch()
    return 1
