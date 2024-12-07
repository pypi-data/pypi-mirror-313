import time

def timer(seconds):
    """Counts down from the specified number of seconds."""
    try:
        for i in range(seconds, 0, -1):
            print(f"Time remaining: {i} seconds", end='\r')  # Print remaining time on the same line
            time.sleep(1)  # Wait for 1 second
        print("Time's up!")  # Indicate the countdown is finished
    except KeyboardInterrupt:
        print("\nTimer interrupted!")  # Handle interruption gracefully