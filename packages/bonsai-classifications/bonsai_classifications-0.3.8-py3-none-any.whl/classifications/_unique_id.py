import csv
import os
import shutil
import tempfile
import uuid
from pathlib import Path

ROOT_PATH = Path(os.path.dirname(__file__))


def add_unique_identifiers(csv_file):

    # Read CSV file
    with open(csv_file, mode="r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        data = list(reader)

    # Identify empty rows and add UUIDs
    for row in data:
        if not row.get("prefixed_id"):
            row["prefixed_id"] = str(uuid.uuid4())

    # Write updated data to a temporary file
    with tempfile.NamedTemporaryFile(
        mode="w", delete=False, newline="", encoding="utf-8"
    ) as temp_file:
        with open(temp_file.name, mode="w", newline="", encoding="utf-8") as file:
            # Write header
            fieldnames = (
                data[0].keys() if data else []
            )  # Get fieldnames from the first row
            writer = csv.DictWriter(file, fieldnames=fieldnames, lineterminator="\n")
            writer.writeheader()

            # Write rows
            for row in data:
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
        csv_files = [
            os.path.join(d, file) for file in os.listdir(d) if file.endswith(".csv")
        ]
        for file in csv_files:
            if "resources.csv" not in str(file):
                add_unique_identifiers(file)
