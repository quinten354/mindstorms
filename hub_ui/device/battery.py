import hub

def get_voltage():
    return hub.battery.voltage()

def get_power():
    return hub.battery.current()

def get_current():
    return hub.battery.capacity_left()

def get_temp():
    return hub.battery.temperature()

