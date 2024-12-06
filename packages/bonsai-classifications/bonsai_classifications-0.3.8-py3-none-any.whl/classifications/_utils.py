import os
from logging import getLogger
from pathlib import Path

import pandas

from ._mapping_type import get_comment, get_skos_uri

logger = getLogger("root")

ROOT_PATH = Path(os.path.dirname(__file__))

activitytype_path = "data/flow/activitytype/"
location_path = "data/location/"
dataquality_path = "data/dataquality/"
unit_path = "data/unit/"
uncertainty_path = "data/uncertainty/"
time_path = "data/time/"
flowobject_path = "data/flow/flowobject/"
flow_path = "data/flow/"

# Lookup function for pandas DataFrame
def lookup(self, keyword):
    """Filter the DataFrame based on the keyword in the "name" column"""
    filtered_df = self[self["name"].str.contains(keyword)]
    return filtered_df


def get_children(self, parent_code):
    """Get all children of a certain parent_code"""
    try:
        filtered_df = self[self["parent_code"] == parent_code]
    except KeyError as e:
        raise KeyError("Data table has no column 'parent_code'") from e
    return filtered_df


def create_conc(df_A, df_B, source="", target="", intermediate=""):
    """Create new concordance based on two other tables.

    Argument
    --------
    df_A : pandas.DataFrame
        concordance table A
        with mapping from "x" to "y"
    df_B : pandas.DataFrame
        concordance table B
        with mapping from "y" to "z"
    target : str
        header name that specifies "x"
    source : str
        header name that specifies "z"
    intermediate : str
        header name that specifies "y"

    Returns
    -------
    pandas.DataFrame
        concordance table with mapping form "x" to "z"
    """
    new_mapping = pandas.merge(df_A, df_B, on=intermediate)

    # Drop duplicate pairs of source and target
    new_mapping = new_mapping.drop_duplicates(subset=[source, target])

    # Calculate the counts of each source and target in the merged DataFrame
    source_counts = new_mapping[source].value_counts().to_dict()
    target_counts = new_mapping[target].value_counts().to_dict()
    # Apply the get_comment function to each row
    new_mapping["comment"] = new_mapping.apply(
        lambda row: get_comment(
            source_counts[row[source]],
            target_counts[row[target]],
            s=row[source],
            t=row[target],
        ),
        axis=1,
    )
    new_mapping["skos_uri"] = new_mapping.apply(
        lambda row: get_skos_uri(
            source_counts[row[source]], target_counts[row[target]]
        ),
        axis=1,
    )

    new_mapping = new_mapping[[source, target, "comment", "skos_uri"]]
    new_mapping = new_mapping.reset_index(drop=True)
    return new_mapping


# Subclass pandas DataFrame
class CustomDataFrame(pandas.DataFrame):
    lookup = lookup
    get_children = get_children


def _get_concordance_file(file_path):
    try:
        # Read the concordance CSV into a DataFrame
        return pandas.read_csv(file_path, dtype=str)
        # return multiple_dfs
    except FileNotFoundError:
        return None
    except Exception as e:
        logger.error(f"Error reading concordance file: {e}")
        return None


def get_concordance(from_classification, to_classification):
    """
    Get the concordance DataFrame based on the specified classifications.
    Parameters
    ----------
    from_classification: str
        The source classification name (e.g., "bonsai").
    to_classification: str
        The target classification name (e.g., "nace_rev2").
    Returns
    -------
    pd.DataFrame
        The concordance DataFrame if 1 file is found; otherwise, a dict of DataFrames.
    """
    # Construct the file name
    fitting_file_names = [
        f"conc_{from_classification}_{to_classification}.csv",
        f"concpair_{from_classification}_{to_classification}.csv",
    ]
    reversed_file_names = [
        f"conc_{to_classification}_{from_classification}.csv",
        f"concpair_{to_classification}_{from_classification}.csv",
    ]
    file_paths = [
        activitytype_path,
        location_path,
        dataquality_path,
        unit_path,
        uncertainty_path,
        time_path,
        flowobject_path,
        flow_path,
    ]
    multiple_dfs = {}
    for f in file_paths:
        for n in fitting_file_names:
            file_path = ROOT_PATH.joinpath(f, n)
            df = _get_concordance_file(file_path)
            if not df is None:
                multiple_dfs[f"{f}"] = df
        for n in reversed_file_names:
            file_path = ROOT_PATH.joinpath(f, n)
            df = _get_concordance_file(file_path)
            if not df is None:
                # Renaming columns
                new_columns = {}
                for col in df.columns:
                    if "_from" in col:
                        new_columns[col] = col.replace("_from", "_to")
                    elif "_to" in col:
                        new_columns[col] = col.replace("_to", "_from")
                df.rename(columns=new_columns, inplace=True)

                # Changing the comment column
                df["comment"] = df["comment"].replace(
                    {
                        "one-to-many correspondence": "many-to-one correspondence",
                        "many-to-one correspondence": "one-to-many correspondence",
                    }
                )
                df["skos_uri"] = df["skos_uri"].replace(
                    {
                        "http://www.w3.org/2004/02/skos/core#narrowMatch": "http://www.w3.org/2004/02/skos/core#broadMatch",
                        "http://www.w3.org/2004/02/skos/core#broadMatch": "http://www.w3.org/2004/02/skos/core#narrowMatch",
                    }
                )
                multiple_dfs[f"{f}"] = df

    if len(multiple_dfs):
        return multiple_dfs[next(iter(multiple_dfs))]
    else:
        return multiple_dfs
