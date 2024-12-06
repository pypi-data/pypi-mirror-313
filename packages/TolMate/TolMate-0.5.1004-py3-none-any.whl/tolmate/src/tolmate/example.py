
from tolmate import configure_behavior, tolmate

# Main program
def celsius_to_kelvin(celsius):
    """Convert Celsius to Kelvin."""
    return celsius + 273.15

# Main loop for initial value input
try:
    # Configure global behavior (example: enable both message and popup)
    configure_behavior(show_popup=True, show_message=True)
    
    value = float(input("Enter the temperature in degrees Celsius: "))

    if tolmate(value, 20, 40, 10, 50, 0, 60):  # Example ranges
        kelvin = celsius_to_kelvin(value)
        print(f"The temperature in Kelvin is: {kelvin:.2f}")

except ValueError:
    print("Please enter a valid number!")
