import pyvisa as visa

def get_power_meter_addresses():
    rm = visa.ResourceManager()
    pm_addresses = []

    # Search through all VISA resources
    for item in rm.list_resources():
        try:
            inst = rm.open_resource(item)
            idn = inst.query('*IDN?').strip()
            print(f"VISA Resource: {item}, IDN: {idn}")  # Print information about detected devices
            if 'PM100D' in idn or 'PM160' in idn:  # Replace with the specific models of your power meters
                pm_addresses.append(item)
        except Exception as e:
            print(f"Error querying VISA resource {item}: {e}")

    if not pm_addresses:
        print("No power meters found.")
        return []

    # If you know the COM port of one of them, you can directly add it
    known_com_port = "COM3"  # replace with your known COM port
    pm_addresses.append(f"ASRL{known_com_port}::INSTR")

    print(f"Power meter VISA addresses: {pm_addresses}")
    return pm_addresses

# Example usage
pm_addresses = get_power_meter_addresses()
