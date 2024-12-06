import json5
import logging
from pathlib import Path
from typing import Dict, Any

import EVMVerifier.certoraContext as Ctx
import EVMVerifier.certoraContextAttributes as Attrs
from EVMVerifier.certoraContextClass import CertoraContext
from Shared import certoraUtils as Util

"""
This file is responsible for reading and writing configuration files.
"""

# logger for issues regarding the general run flow.
# Also serves as the default logger for errors originating from unexpected places.
run_logger = logging.getLogger("run")


def current_conf_to_file(context: CertoraContext) -> Dict[str, Any]:
    """
    Saves current command line options to a configuration file
    @param context: context object
    @:return the data that was written to the file (in json/dictionary form)

    We are not saving options if they were not provided (and have a simple default that cannot change between runs).
    Why?
    1. The .conf file is shorter
    2. The .conf file is much easier to read, easy to find relevant arguments when debugging
    3. Reading the .conf file is quicker
    4. Parsing the .conf file is simpler, as we can ignore the null case
    """
    def input_arg_with_value(k: Any, v: Any) -> Any:
        all_conf_names = Attrs.get_attribute_class().all_conf_names()
        return v is not None and v is not False and k in all_conf_names

    context_to_save = {k: v for k, v in vars(context).items() if input_arg_with_value(k, v)}
    all_conf_names = Attrs.get_attribute_class().all_conf_names()
    context_to_save = dict(sorted(context_to_save.items(), key=lambda x: all_conf_names.index(x[0])))
    context_to_save.pop('build_dir', None)  # build dir should not be saved, each run should define its own build_dir
    context_to_save.pop('mutation_test_id', None)  # mutation_test_id should be recreated for every run

    out_file_path = Util.get_last_conf_file()
    run_logger.debug(f"Saving last configuration file to {out_file_path}")
    Ctx.write_output_conf_to_path(context_to_save, out_file_path)

    return context_to_save


def read_from_conf_file(context: CertoraContext) -> None:
    """
    If the file in the command line is a conf file, read data from the configuration file and add each key to the
    context namespace if the key was not set in the command line (command line shadows conf data).
    @param context: A namespace containing options from the command line
    """

    conf_file_path = Path(context.files[0])
    assert conf_file_path.suffix == ".conf", f"conf file must be of type .conf, instead got {conf_file_path}"

    with conf_file_path.open() as conf_file:
        configuration = json5.load(conf_file, allow_duplicate_keys=False)
        try:
            check_conf_content(configuration, context)
        except Util.CertoraUserInputError as e:
            raise Util.CertoraUserInputError(f"Error when reading {conf_file_path}", e) from None
        context.conf_file = str(conf_file_path)


def check_conf_content(conf: Dict[str, Any], context: CertoraContext) -> None:
    """
    validating content read from the conf file
    Note: a command line definition trumps the definition in the file.
    If in the .conf file solc is 4.25 and in the command line --solc solc6.10 was given, sol6.10 will be used
    @param conf: A json object in the conf file format
    @param context: A namespace containing options from the command line, if any
    """
    for option in conf:
        if hasattr(context, option):
            val = getattr(context, option)
            if val is None or val is False:
                setattr(context, option, conf[option])
            elif option != Attrs.EvmProverAttributes.FILES.get_conf_key() and val != conf[option]:
                cli_val = ' '.join(val) if isinstance(val, list) else str(val)
                conf_val = ' '.join(conf[option]) if isinstance(conf[option], list) else str(conf[option])
                run_logger.warning(f"Note: attribute {option} value in CLI ({cli_val}) overrides value stored in conf"
                                   f" file ({conf_val})")
        else:
            raise Util.CertoraUserInputError(f"{option} appears in the conf file but is not a known attribute. ")
    if 'files' not in conf:
        raise Util.CertoraUserInputError("Mandatory 'files' attribute is missing from the configuration")
    context.files = conf['files']  # Override the current .conf file
