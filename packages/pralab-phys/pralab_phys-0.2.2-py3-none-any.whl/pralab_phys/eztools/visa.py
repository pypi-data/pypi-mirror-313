import pyvisa

def show_connected_visa(timeout=5000):
    rm = pyvisa.ResourceManager()
    res_list = rm.list_resources()

    for i in res_list:
        inst = rm.open_resource(i)
        inst.timeout = timeout
        try:
            print(i, ": ", inst.query("*IDN?"))
        except Exception:
            print(i, ": ", "Unknown instruments (*IDN? command failed)")

def list_visa_resources():
    return pyvisa.ResourceManager().list_resources()