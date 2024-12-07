import random
import string

def generate_password(length=12):
    """Generates a random password with the specified length."""
    if length < 4:
        raise ValueError("Password length must be at least 4 characters.")  # Ensure a minimum length
    
    # Define the character set
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for _ in range(length))  # Generate the password
    print("Generated Password:", password)  # Print the generated password
    return password  # Return the generated password
