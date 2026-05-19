from datetime import datetime

# Get current date and time
current_time = datetime.now()

# Create and open a text file in write mode
with open("current_time.txt", "w") as file:
    file.write(f"Current Date & Time: {current_time}\n")

# Print the current time
print("Current Date & Time:", current_time)
