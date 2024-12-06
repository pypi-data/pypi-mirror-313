import os
from pathlib import Path

import pandas as pd
import pytest

from classifications import _mapping_type

test_file = Path(os.path.dirname(__file__)).parent / "tests/data/conc_test.csv"


def test_mapping_type():
    _mapping_type.add_mapping_comment(test_file)
    df_result = pd.read_csv(test_file)
    assert df_result["comment"].to_list() == [
        "one-to-many correspondence",
        "one-to-many correspondence",
        "one-to-one correspondence",
        "many-to-one correspondence",
        "many-to-one correspondence",
        "one-to-many correspondence",
        "many-to-many correspondence",
        "many-to-one correspondence",
    ]
