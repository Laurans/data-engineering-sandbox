import re


def sanitize_sql_identifier(input_string):
    # Define a regular expression pattern to match special characters
    pattern = r"[^a-zA-Z0-9_]"

    # Use the re.sub() function to remove special characters from the input string
    cleaned_string = re.sub(pattern, "", input_string)

    # Check if the cleaned string is a reserved keyword in SQL
    reserved_keywords = [
        "SELECT",
        "INSERT",
        "UPDATE",
        "DELETE",
        "FROM",
        "WHERE",
        "AND",
        "OR",
        "JOIN",
        "GROUP BY",
        "ORDER BY",
        "LIMIT",
        "TRUNCATE",
        "DROP",
        "TABLE",
        "DATABASE"
        # Add more reserved keywords as needed
    ]

    cleaned_string = cleaned_string.upper()  # Convert to uppercase for comparison

    if cleaned_string in reserved_keywords:
        # Append an underscore to the cleaned string if it is a reserved keyword
        cleaned_string += "_"

    return cleaned_string.lower()
