import hub

def get_acceleration(filtered = False):
    return hub.motion.accelerometer(filtered)

def get_gyroscope(filtered = False):
    return hub.motion.gyroscope(filtered)

def get_yaw(filtered = False):
    return hub.motion.yaw_pitch_roll()[0]

def get_pitch(filtered = False):
    return hub.motion.yaw_pitch_roll()[1]

def get_roll(filtered = False):
    return hub.motion.yaw_pitch_roll()[2]

def set_yaw(value):
    return hub.motion.yaw_pitch_roll(yaw_preset = value)

def was_tapped():
    return hub.motion.gesture() == hub.motion.TAPPED

def was_double_tapped():
    return hub.motion.gesture() == hub.motion.DOUBLETAPPED

def was_shaked():
    return hub.motion.gesture() == hub.motion.SHAKE

def was_freefall():
    return hub.motion.gesture() == hub.motion.FREEFALL

