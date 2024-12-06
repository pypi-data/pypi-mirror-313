#!/usr/bin/env python3

import sys
from pathlib import Path

scripts_dir_path = Path(__file__).parent.resolve()  # containing directory
sys.path.insert(0, str(scripts_dir_path))

from EquivalenceCheck.equivCheck import ext_equivcheck_entry_point


def equiv_check_entry_point() -> None:
    ext_equivcheck_entry_point()


if __name__ == '__main__':
    equiv_check_entry_point()
