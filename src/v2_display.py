def display_output(rows):
    """
    Format dataset rows for display: one row per line, single space between rows.
    Also prints each row to the console with a line break.
    """
    output_lines = []
    for row in rows:
        print(row)  # Print each row to the console
        output_lines.append(str(row))
    return "\n\n".join(output_lines)  # Double line break for GUI