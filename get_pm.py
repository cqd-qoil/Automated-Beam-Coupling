import pyvisa as visa

def get_power_meter_address(device_name):
    """
    Takes connection_method argument ('USB' or 'COM') and optionally COM_port='COM#' if using COM
    """
    rm = visa.ResourceManager()
    pm_addr = None

    for item in rm.list_resources():
        try:
            inst = rm.open_resource(item)
            idn = inst.query('*IDN?').strip()
            print("VISA Resource: {item}, IDN: {idn}")  # Print information about detected devices
            if device_name in idn:  # Search for device model 
                pm_addr = item
                break
        except Exception as e:
            print(f"Error querying VISA resource {item}: {e}")

    if pm_addr:
        print("Power meter VISA address: {pm_addr}")
        return pm_addr
    else:
        print("Power meter not found.")
        return 0

# Example usage
pm_addresses = get_power_meter_addresses('PM100D')
