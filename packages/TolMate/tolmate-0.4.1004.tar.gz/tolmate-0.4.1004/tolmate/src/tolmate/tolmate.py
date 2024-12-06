
import tkinter as tk
from tkinter import simpledialog

# Initialize the Tkinter root window only once
root = tk.Tk()
root.withdraw()  # Hide the main root window

# Global settings for popup and message behavior
SHOW_POPUP = True
SHOW_MESSAGE = True

def configure_behavior(show_popup=True, show_message=True):
    """
    Configure the behavior of the tolmate function globally.
    """
    global SHOW_POPUP, SHOW_MESSAGE
    SHOW_POPUP = show_popup
    SHOW_MESSAGE = show_message

def show_popup(value=None, level="info", title="Message", message="", limits=()):
    """
    Generalized popup function to handle warnings and errors dynamically.
    
    Parameters:
    - value: The value being checked (optional, used for warnings).
    - level: "Info", "Warning", or "Error" to define the popup's appearance.
    - title: Title of the popup window.
    - message: The message to display in the popup.
    - limits: The tolerance limits passed from the main tolmate call (used for rechecking).
    """
    popup = tk.Toplevel(root)
    popup.title(title)

    # Configure colors based on the level
    colors = {
        "info": {"bg": "green", "fg": "white"},
        "warning": {"bg": "orange", "fg": "black"},
        "error": {"bg": "red", "fg": "yellow"}
    }

    bg_color = colors[level]["bg"]
    fg_color = colors[level]["fg"]
    popup.configure(bg=bg_color)
    popup.geometry("400x250")

    # Symbol and Message Layout
    frame_content = tk.Frame(popup, bg=bg_color)
    frame_content.pack(pady=10, padx=10)

    symbols = {
        "info": "ℹ️",       # Information symbol
        "warning": "⚠️",  # Warning triangle
        "error": "❌"     # Error cross
    }
    symbol = symbols.get(level, "")  # Default to empty if level not found

    label_symbol = tk.Label(frame_content, text=symbol, font=("Arial", 32), bg=bg_color, fg=fg_color)
    label_symbol.grid(row=0, column=0, padx=10)

    label_message = tk.Label(frame_content, text=message, bg=bg_color, fg=fg_color, wraplength=250, justify="left")
    label_message.grid(row=0, column=1, padx=10)

    ### Optional Limits Display
    if limits:
        label_limits = tk.Label(frame_content, text=f"\nDefined limits: {limits}", bg=bg_color, fg=fg_color)
        label_limits.grid(row=1, column=1, sticky="w", padx=10)

    # Button Section
    frame_buttons = tk.Frame(popup, bg=bg_color)
    frame_buttons.pack(pady=10)

    def confirm():
        popup.destroy()
        print(f"Value confirmed: {value}")

    def change_value():
        popup.destroy()
        new_value = simpledialog.askfloat("Input", "Enter a new value:")
        if new_value is not None:
            print(f"New value entered: {new_value}")
            if limits:
                tolmate(new_value, *limits)  # Dynamically pass the same limits for rechecking

    def acknowledge():
        popup.destroy()

    button_actions = {
        "info": [("OK", acknowledge)],
        "warning": [("Confirm", confirm), ("Change", change_value)],
        "error": [("OK", acknowledge)]
    }

    for btn_text, action in button_actions.get(level, []):
        button = tk.Button(frame_buttons, text=btn_text, command=action)
        button.pack(side="left", padx=10)

    # Ensure Popup is Interactive
    popup.transient()  # Make the popup window transient to the root window
    popup.grab_set()  # Ensure the user can only interact with the popup
    popup.lift()  # Bring the popup to the front
    popup.attributes('-topmost', 1)  # Ensure the popup stays on top
    popup.wait_window()  # Wait until the popup is closed

def tolmate(value, *args):
    """
    Check if the given value is within the specified tolerance ranges and provide different messages.
    
    - Within ±t1 limits: "Info" (between first two arguments)
    - Within ±t2 limits: "Soft warning" (between next two arguments)
    - Within ±t3 limits: "Hard warning" (between next two arguments)
    """
    if len(args) >= 2:
        t1_lower, t1_upper = args[0], args[1]
        specs_lower, specs_upper = args[0], args[1]

        if t1_lower <= value <= t1_upper:
            if SHOW_MESSAGE:
                print(f"Info: the value {value} is within [{t1_lower},{t1_upper}]")
            if SHOW_POPUP:
                show_popup(value=value, level="info", title="->| Info |<-",
                           message=f"Info: \nthe value \n\n{value} \n\nis within \n\n[{t1_lower},{t1_upper}]",
                           limits=args)
            return True
    
    if len(args) >= 4:
        t2_lower, t2_upper = args[2], args[3]
        specs_lower, specs_upper = args[2], args[3]

        if t2_lower <= value <= t2_upper:
            if SHOW_MESSAGE:
                print(f"Soft Warning: The temperature is within [{t2_lower},{t2_upper}]")
            if SHOW_POPUP:
                show_popup(value=value, level="warning", title="->| Soft Warning |<-",
                           message=f"Warning: \nthe value \n\n{value} \n\nis within \n\n[{t2_lower},{t2_upper}]",
                           limits=args)
            return True

    if len(args) == 6:
        t3_lower, t3_upper = args[4], args[5]
        specs_lower, specs_upper = args[4], args[5]

        if t3_lower <= value <= t3_upper:
            if SHOW_MESSAGE:
                print(f"Critical Warning: the value {value} is within [{t3_lower},{t3_upper}]")
            if SHOW_POPUP:
                show_popup(value=value, level="warning", title="->| Critical Warning |<-",
                           message=f"Critical Warning: \n\nthe value \n\n{value} \n\nis within \n\n[{t3_lower},{t3_upper}]",
                           limits=args)
            return True
    
    if SHOW_MESSAGE:
        print(f"Error: the value {value} is out of specifications [{specs_lower},{specs_upper}]")
    if SHOW_POPUP:
        show_popup(level="error", title="->| Error |<- ", message=f"The value \n\n{value} \n\nis outside specifications \n\n[{specs_lower},{specs_upper}]", limits=args)
    
    return False