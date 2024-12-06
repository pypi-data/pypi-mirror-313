
def get_csv_separator(csv_file_path):
    with open(csv_file_path, 'r') as file:
        first_line = file.readline().strip()  # Read the first line

    # Define a list of common separators to check
    common_separators = [',', ';', '\t', '|']

    # Find the separator used in the first line
    for separator in common_separators:
        if separator in first_line:
            return separator

    # If none of the common separators are found, return None
    return None