import os
import pandas as pd
from src.gen_files.ConsoleHelpers import print_functions as pf, input_helper as ih
from src.gen_files import file_utils as fu, stats_for_metrics as sfm, gen_scripts as gs, paths as p
from src import application_properties as ap
import os
import pandas as pd

notes = ["This script adds a suffix to each test name in given csv files",
         "It will run on all csv's in the given directory",
         "If there are other files in the directory, it will not read them",
         "It will read the column headers from the first csv, and assume that the chosen column header exists in every other csv"
         "The output can be found in " + p.output_dir]


def main_script():
    pf.print_step_separator("Add Suffix to Test name in CSV file")
    gs.clear_create_dir(p.add_suffix_output_dir)
    pf.print_note_list(notes, "How this works:")
    suffix = input("Enter the Suffix you would like to add to the test names (for example - " + ap.ng_suffix + ")")
    src_dir = ih.get_input_ensure_valid("Enter the path to the directory containing the csv files: ", os.path.isdir,
                           "Please ensure that path leads to a valid directory")

    total_rows_edited = add_suffix_to_autotest_names(src_dir, suffix)

    print(" ")
    pf.print_note("Edited a total of " + str(total_rows_edited) + " in all csv files")

    sfm.append_to_stats(version=ap.version, user_name=gs.get_cur_user_name(), date=gs.get_date(), time=gs.get_time(),
                        product=sfm.product_names.Add_Suffix_To_CSV.name, is_success=True,
                        tests_analyzed= total_rows_edited)


def add_suffix_to_autotest_names(input_directory_path, suffix, ):
    # List all CSV files in the directory
    csv_files = [file for file in os.listdir(input_directory_path) if file.endswith('.csv')]
    if len(csv_files) == 0:
        pf.print_warning("Did not find any valid csv files in " + input_directory_path)
        return 0

    dir_name = os.path.basename(input_directory_path)
    output_dir = os.path.join(p.add_suffix_output_dir, dir_name)
    gs.clear_create_dir(output_dir)

    first_file = os.path.join(input_directory_path, csv_files[0])
    column_header = ih.get_one_item_from_list('Discovered the following column header names',
                                              'Which column to add the ' + suffix + ' to?',
                                              pd.read_csv(first_file).columns.to_list())

    total_rows_edited = 0

    pf.print_note("Adding '" + suffix + "' to every row under '" + column_header +"'")
    # Loop through each CSV file
    for file_name in csv_files:
        input_file_path = os.path.join(input_directory_path, file_name)

        # Read CSV file into a DataFrame
        df = pd.read_csv(input_file_path)
        original_non_nan_count = df[column_header].notna().sum()
        # Add suffix to the end of every non-NaN value in the chosen column, before the '.'
        df[column_header] = df[column_header].apply(lambda x: x.replace('.', f'{suffix}.') if pd.notna(x) and '.' in x else (f'{x}{suffix}' if pd.notna(x) else x))

        # Write the modified DataFrame back to the CSV file
        output_file_path = os.path.join(output_dir, suffix + '_Version_' + file_name)
        df.to_csv(output_file_path, index=False)
        pf.print_note("Created: " + output_file_path)
        total_rows_edited += original_non_nan_count

    return total_rows_edited


if __name__ == '__main__':
    main_script()