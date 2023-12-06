import pyvisa as visa

def list_all_addresses(device_name):
    """
    Takes device name argument and searches through resources for it
    Sometimes the registered name may vary from the actual name to list all connected device names run XXXX
    """
    rm = visa.ResourceManager()
    pm_addr = None

    for item in rm.list_resources():
        try:
            inst = rm.open_resource(item)
            idn = inst.query('*IDN?').strip()
            print("\nVISA Resource: ",item, ", IDN: ",idn)  # Print information about detected devices
        except Exception as e:
            print(f"Error querying VISA resource {item}: {e}")


