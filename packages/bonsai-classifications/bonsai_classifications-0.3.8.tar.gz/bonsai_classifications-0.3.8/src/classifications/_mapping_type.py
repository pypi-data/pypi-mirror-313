import csv
import os
import shutil
import tempfile
from logging import getLogger
from pathlib import Path

ROOT_PATH = Path(os.path.dirname(__file__))

logger = getLogger("root")

# Define a function to determine the comment based on the counts
def get_comment(source_count, target_count, s, t):
    if source_count == 1 and target_count == 1:
        return "one-to-one correspondence"
    elif source_count > 1 and target_count == 1:
        return "one-to-many correspondence"
    elif source_count == 1 and target_count > 1:
        return "many-to-one correspondence"
    elif source_count > 1 and target_count > 1:
        logger.info(
            f"'many-to-many' relation occured when mapping source code '{s}' to target code '{t}'. Make sure that you only map source codes to target codes each with the most disaggregated level!"
        )
        return "many-to-many correspondence"
    else:
        return ""


# Define a function to determine the skos ui based on the counts
def get_skos_uri(source_count, target_count):
    if source_count == 1 and target_count == 1:
        return "http://www.w3.org/2004/02/skos/core#exactMatch"
    elif source_count > 1 and target_count == 1:
        return "http://www.w3.org/2004/02/skos/core#narrowMatch"
    elif source_count == 1 and target_count > 1:
        return "http://www.w3.org/2004/02/skos/core#broadMatch"
    elif source_count > 1 and target_count > 1:
        return "http://www.w3.org/2004/02/skos/core#relatedMatch"
    else:
        return ""


def add_mapping_comment(csv_file):

    # Read CSV file
    with open(csv_file, mode="r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        rows = list(reader)
        column_names = reader.fieldnames

    source_name = column_names[0]
    target_name = column_names[1]

    # Update the rows with the comments
    for row in rows:
        source_count = sum(1 for r in rows if r[source_name] == row[source_name])
        target_count = sum(1 for r in rows if r[target_name] == row[target_name])
        row["comment"] = get_comment(
            source_count, target_count, s=row[source_name], t=row[target_name]
        )
        row["skos_uri"] = get_skos_uri(source_count, target_count)

    # Write updated data to a temporary file
    with tempfile.NamedTemporaryFile(
        mode="w", delete=False, newline="", encoding="utf-8"
    ) as temp_file:
        with open(temp_file.name, mode="w", newline="", encoding="utf-8") as file:
            # Write header
            fieldnames = (
                rows[0].keys() if rows else []
            )  # Get fieldnames from the first row
            writer = csv.DictWriter(file, fieldnames=fieldnames, lineterminator="\n")
            writer.writeheader()

            # Write rows
            for row in rows:
                # Handle values with commas
                formatted_row = []
                for value in row.values():
                    try:
                        if isinstance(value, list):
                            formatted_row.append(",".join(value))
                        elif "," in value:
                            formatted_row.append(f'"{value}"')
                        else:
                            formatted_row.append(value)
                    except TypeError:
                        pass
                file.write(",".join(formatted_row) + "\n")

    # Replace the original file with the temporary one
    shutil.move(temp_file.name, csv_file)


# Function to combine the two columns for source and the two columns for target
def combine_columns(row, col1, col2):
    return f"{row[col1]}-{row[col2]}" if col1 and col2 in row else ""


def add_mapping_comment_concpair(csv_file, overwrite=False):
    # Read the CSV file
    with open(csv_file, mode="r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        rows = list(reader)
        column_names = reader.fieldnames

    if not column_names or len(column_names) < 4:
        raise ValueError(
            "The CSV file must have at least four columns: two for source and two for target."
        )

    # Check if the "comment" column already exists
    comment_exists = "comment" and "skos_uri" in column_names

    # If the comment column exists, decide whether to overwrite or not
    if comment_exists and not overwrite:
        logger.warning(
            "The 'comment' column already exists. Skipping update as overwrite_comment=False."
        )
        return

    # Assumes first two columns are source and next two are target
    source_col1, source_col2 = column_names[0], column_names[1]
    target_col1, target_col2 = column_names[2], column_names[3]

    # Update the rows with the comments
    for row in rows:
        # Combine the values from the two source and two target columns
        source_combined = combine_columns(row, source_col1, source_col2)
        target_combined = combine_columns(row, target_col1, target_col2)

        # Calculate source and target counts for each combined pair
        source_count = sum(
            1
            for r in rows
            if combine_columns(r, source_col1, source_col2) == source_combined
        )
        target_count = sum(
            1
            for r in rows
            if combine_columns(r, target_col1, target_col2) == target_combined
        )

        # Add the comment based on the correspondence
        row["comment"] = get_comment(
            source_count, target_count, s=source_combined, t=target_combined
        )
        row["skos_uri"] = get_skos_uri(source_count, target_count)

    # Write updated data to a temporary file
    with tempfile.NamedTemporaryFile(
        mode="w", delete=False, newline="", encoding="utf-8"
    ) as temp_file:
        # Writing updated rows to temp file
        fieldnames = column_names + ["comment"] + ["skos_uri"]
        writer = csv.DictWriter(temp_file, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)

    # Replace the original file with the updated temp file
    shutil.move(temp_file.name, csv_file)


if __name__ == "__main__":
    directories = [
        ROOT_PATH.joinpath("data/flow/activitytype"),
        ROOT_PATH.joinpath("data/dataquality"),
        ROOT_PATH.joinpath("data/flow/flowobject"),
        ROOT_PATH.joinpath("data/location"),
        ROOT_PATH.joinpath("data/time"),
        ROOT_PATH.joinpath("data/uncertainty"),
        ROOT_PATH.joinpath("data/unit"),
        ROOT_PATH.joinpath("data/flow"),
    ]
    for d in directories:
        conc_csv_files = [
            os.path.join(d, file)
            for file in os.listdir(d)
            if file.endswith(".csv") and file.startswith("conc_")
        ]
        for file in conc_csv_files:
            add_mapping_comment(file)

        concpair_csv_files = [
            os.path.join(d, file)
            for file in os.listdir(d)
            if file.endswith(".csv") and file.startswith("concpair_")
        ]
        for file in concpair_csv_files:
            add_mapping_comment_concpair(file)
