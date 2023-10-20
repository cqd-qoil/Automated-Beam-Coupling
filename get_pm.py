import pyvisa as visa

def get_power_meter_address(connection_method, COM_port=None):
    """
    Takes connection_method argument ('USB' or 'COM') and optionally COM_port='COM#' if using COM
    """
    rm = visa.ResourceManager()
    pm_addr = None
    
    # Dictionary for different connection methods and their address formats
    address_formats = {
        'USB': 'USB0::0x0000::0x0000::0::INSTR',
        'COM': f'ASRL{COM_port}::INSTR'
    }
    
    # Get the corresponding address format
    address = address_formats.get(connection_method)
    
    if address is None:
        print(f"Invalid connection method: {connection_method}")
        return None
    
    if 'COM' in connection_method and COM_port is not None:
        address = address.format(COM_port=COM_port)

    try:
        inst = rm.open_resource(address)
        idn = inst.query('*IDN?').strip()
        print(f"VISA Resource: {address}, IDN: {idn}")  # Print information about detected device
        return address
    except Exception as e:
        print(f"Error querying VISA resource {address}: {e}")
        print("Power meter not found.")
        return None

# Example usage
pm_addresses = get_power_meter_addresses('USB', COM_port=None)
