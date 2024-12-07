def ascii(text):
    """Converts a string into its ASCII representation."""
    ascii_values = [ord(char) for char in text]  # Convert each character to its ASCII value
    print("ASCII values:", ascii_values)  # Print the list of ASCII values
