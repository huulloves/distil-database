def format_table(columns, rows):
    """
    Formats columns and rows into a readable string for display.
    """
    output = ', '.join(columns) + '\n'
    for row in rows:
        output += ', '.join(str(cell) for cell in row) + '\n'
    return output