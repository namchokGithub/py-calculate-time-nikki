import tkinter as tk
from tkinter import messagebox
from datetime import datetime, timedelta
import pytz
from PIL import Image, ImageTk
import os
import sys

# Dynamically locate resources in PyInstaller's temporary folder
def resource_path(relative_path):
    """ Get the absolute path to the resource, works for dev and PyInstaller """
    try:
        # PyInstaller creates a temporary folder and stores the resource path there
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def calculate_time():
    try:
        # Get inputs from user
        if current_value_entry.get():
            current_value = int(current_value_entry.get())
        else:
            current_value_entry.delete(0, tk.END)
            current_value_entry.insert(0, "1")
            current_value = 1
        if target_value_entry.get():
            target_value = int(target_value_entry.get())
        else:
            target_value_entry.delete(0, tk.END)
            target_value_entry.insert(0, "350")
            target_value = 350
        increment_interval = 5  # Fixed increment interval

        # Get current time in Bangkok timezone
        bangkok_timezone = pytz.timezone("Asia/Bangkok")
        current_time = datetime.now(bangkok_timezone)

        # Calculate required units and time
        if target_value == '':
            target_value = 350

        required_units = target_value - current_value
        total_minutes = required_units * increment_interval
        target_time = current_time + timedelta(minutes=total_minutes)

        # Check if target_time is on the next day
        is_next_day = current_time.date() != target_time.date()
        next_day_text = " (TMR)" if is_next_day else " (TODAY)"

        # Display result
        result_label.config(text=f"Target Time: {target_time.strftime('%H:%M:%S')}{next_day_text}")
    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid numbers.")

def validate_number_input(value):
    """Validate that the input contains only numbers."""
    if value == "":
        return True
    if value.isdigit():
        return int(value) <= 350
    return value == ""

def validate_number_input_target(value):
    """Validate that the input contains only numbers or is empty."""
    if value == "":  # Allow empty input for intermediate editing
        return True
    if value.isdigit():
        return int(value) <= 350
    return False

def set_default_target_value(event):
    """Set default value to 350 if the entry is empty or 0."""
    value = target_value_entry.get()
    if value == "" or value == "0":
        target_value_entry.delete(0, tk.END)
        target_value_entry.insert(0, "350")

# Create the main window
root = tk.Tk()
root.title("Target Time Calculator")

# Add the logo image to the title bar
icon_path = resource_path("assets/nikki.png")
icon = tk.PhotoImage(file=icon_path)
root.iconphoto(False, icon)

# Add the logo image
# Use resource_path to load the logo
logo_path = resource_path("assets/nikki-logo.png")
original_logo = Image.open(logo_path)  # Dynamically locate the image
resized_logo = original_logo.resize((400, 150))  # Resize to 300x100 pixels
logo = ImageTk.PhotoImage(resized_logo)

# Display the logo
logo_label = tk.Label(root, image=logo)
logo_label.grid(row=0, column=0, columnspan=4, pady=5)

validate_number = root.register(validate_number_input)
validate_number_target = root.register(validate_number_input_target)

# Input fields
# Function to clear the input field
def clear_current_value():
    current_value_entry.delete(0, tk.END)
def clear_target_value():
    target_value_entry.delete(0, tk.END)
def max_target_value():
    target_value_entry.delete(0, tk.END)
    target_value_entry.insert(0, "350")
def add_ten_current_value():
    try:
        current_value = int(current_value_entry.get()) if current_value_entry.get() else 0
        new_value = current_value + 10
        if new_value > 350:
            new_value = 350
        if new_value >= 350:
            add_ten_button.config(state="disabled")
        current_value_entry.delete(0, tk.END)
        current_value_entry.insert(0, str(new_value))
    except ValueError:
        messagebox.showerror("Input Error", "Please enter a valid number.")

def monitor_current_value(*args):
    try:
        current_value = int(current_value_entry.get()) if current_value_entry.get() else 0
        if current_value >= 350:
            add_ten_button.config(state="disabled")
            clear_current_button.config(state="normal", bg="gray")
        elif current_value > 0 :
            add_ten_button.config(state="normal")
            clear_current_button.config(state="normal", bg="gray")
        else:
            add_ten_button.config(state="normal")
            clear_current_button.config(state="disabled", bg="#888888")
    except ValueError:
        add_ten_button.config(state="disabled")
        clear_current_button.config(state="normal", bg="gray")

# Attach trace to monitor changes
current_value_var = tk.StringVar()
current_value_var.trace_add("write", monitor_current_value)

tk.Label(root, text="Current Value:").grid(row=1, column=0, padx=5, pady=5)
current_value_entry = tk.Entry(root, textvariable=current_value_var, validate="key", validatecommand=(validate_number, "%P"))
current_value_entry.grid(row=1, column=1, padx=5, pady=5)
add_ten_button = tk.Button(
    root,
    text="ADD 10",
    command=add_ten_current_value,
    fg="black",
    font=("Arial", 10),
    relief="raised",
    bd=1,
    padx=10,
    pady=2
)
add_ten_button.grid(row=1, column=2, padx=5, pady=5)
clear_current_button = tk.Button(
    root,
    text="X",
    command=clear_current_value,
    bg="gray",
    fg="white",  # Text color
    font=("Arial", 10, "bold"),  # Font style
    relief="raised",  # Border style
    bd=1,  # Border width
    padx=10,  # Padding inside the button
    pady=2    # Padding inside the button
)
clear_current_button.grid(row=1, column=3, padx=5, pady=5)
clear_current_button.config(state="disabled", bg="#888888")

tk.Label(root, text="Target Value:").grid(row=2, column=0, padx=5, pady=5)
target_value_entry = tk.Entry(root, validate="key", validatecommand=(validate_number_target, "%P"))
target_value_entry.grid(row=2, column=1, padx=5, pady=5)
clear_button = tk.Button(
    root,
    text="X",
    command=clear_target_value,
    fg="black",  # Text color
    font=("Arial", 10, "bold"),  # Font style
    relief="raised",  # Border style
    bd=1,  # Border width
    padx=10,  # Padding inside the button
    pady=1    # Padding inside the button
)
clear_button.grid(row=2, column=3, padx=5, pady=1)
max_button = tk.Button(
    root,
    text="MAX",
    command=max_target_value,
    fg="black",  # Text color
    font=("Arial", 10),  # Font style
    relief="raised",  # Border style
    bd=1,  # Border width
    padx=10,  # Padding inside the button
    pady=1    # Padding inside the button
)
max_button.grid(row=2, column=2, padx=5, pady=1)

# Bind focus-out event to set default value
# target_value_entry.bind("<FocusOut>", set_default_target_value)

tk.Label(root, text="Increment Interval (min):").grid(row=3, column=0, padx=5, pady=5)
tk.Label(root, text="5 (fixed)").grid(row=3, column=1, columnspan=4, padx=5, pady=5)

# # Fixed current time (Bangkok timezone)
# bangkok_timezone = pytz.timezone("Asia/Bangkok")
# current_time = datetime.now(bangkok_timezone).strftime("%H:%M")
# tk.Label(root, text="Current Time:").grid(row=4, column=0, padx=5, pady=5)
# tk.Label(root, text=f"{current_time} (Bangkok)").grid(row=4, column=1, padx=5, pady=5)

# Function to update current time
def update_time():
    bangkok_timezone = pytz.timezone("Asia/Bangkok")
    current_time = datetime.now(bangkok_timezone).strftime("%H:%M:%S")  # Add seconds for real-time updates
    current_time_label.config(text=f"{current_time} (Bangkok)")  # Update the label's text
    root.after(1000, update_time)  # Schedule the function to run again after 1 second (1000ms)

# Fixed current time label
tk.Label(root, text="Current Time:").grid(row=4, column=0, padx=5, pady=5)
current_time_label = tk.Label(root, text="", font=("Arial", 10))  # Placeholder for the time
current_time_label.grid(row=4, column=1, columnspan=4, padx=5, pady=5)

# Start updating the time
update_time()

# Create a frame for buttons to align them properly
button_frame = tk.Frame(root)
button_frame.grid(row=5, column=0, columnspan=4, pady=10)

# Calculate button
calculate_button = tk.Button(
    button_frame, text="Calculate", command=calculate_time,
    bg="#d8e2dc",  # Background color
    fg="black",  # Text color
    font=("Arial", 10),  # Font style
    relief="raised",  # Border style
    bd=1,  # Border width
    padx=10,  # Horizontal padding inside the button
    pady=5   # Vertical padding inside the button
)
calculate_button.pack(side="left", padx=10)  # Add space between buttons

# Clear button
def clear_input_and_result():
    current_value_entry.delete(0, tk.END)  # Clear current value input
    target_value_entry.delete(0, tk.END)   # Clear target value input
    result_label.config(text="Target Time: 00:00:00")  # Reset result label

clear_button = tk.Button(
    button_frame,
    text="Clear",
    command=clear_input_and_result,
    bg="#ffe5d9",  # Background color
    fg="black",  # Text color
    font=("Arial", 10),  # Font style
    relief="raised",  # Border style
    bd=1,  # Border width
    padx=10,  # Horizontal padding inside the button
    pady=5   # Vertical padding inside the button
)
clear_button.pack(side="left", padx=10)  # Add space between buttons

# Close Program button
close_button = tk.Button(
    button_frame,
    text="Close",
    command=root.quit,
    bg="#ffcad4",  # Background color
    fg="black",  # Text color
    font=("Arial", 10),  # Font style
    relief="raised",  # Border style
    bd=1,  # Border width
    padx=10,  # Horizontal padding inside the button
    pady=5   # Vertical padding inside the button
)
close_button.pack(side="left", padx=10)

# Result label
result_label = tk.Label(
    root,
    text="Target Time: 00:00:00",
    font=("Arial", 14, "bold"),  # Larger bold font
    fg="#2E86C1",  # Hex color for blue text
    bg="#F0F8FF",  # Hex color for light background
    relief="groove",  # Adds a border
    bd=2,  # Border width
    padx=10,  # Padding inside the label (horizontal)
    pady=5   # Padding inside the label (vertical)
)
result_label.grid(row=6, column=0, columnspan=4, pady=10)

# Display text using grid
tk.Label(root, text="v0.0.1", font=("Arial", 7), fg="black").grid(row=7, column=0, columnspan=4)

# Start the GUI event loop
root.mainloop()
