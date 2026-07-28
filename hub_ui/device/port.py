import hub

class motor:
    def get_speed(port):
        port = _get_port(port)
        port.motor.mode([(1, 0)])
        return port.motor.get()[0]

    def get_rel_pos(port):
        port = _get_port(port)
        port.motor.mode([(2, 0)])
        return port.motor.get()[0]

    def set_rel_pos(port, pos = 0):
        port = _get_port(port)
        port.motor.preset(pos)

    def get_abs_pos(port):
        port = _get_port(port)
        port.motor.mode([(3, 0)])
        return port.motor.get()[0]

    def float(port):
        port = _get_port(port)
        port.motor.float()

    def brake(port):
        port = _get_port(port)
        port.motor.brake()

    def hold(port):
        port = _get_port(port)
        port.motor.hold()

    def get_busy(port):
        port = _get_port(port)
        return port.motor.busy(1)

    def run_speed(port, speed, **kwargs):
        port = _get_port(port)
        port.motor.run_at_speed(speed, **kwargs)

    def run_for_sec(port, sec, **kwargs):
        port = _get_port(port)
        port.motor.run_for_time(sec * 1000, **kwargs)

    def run_for_degrees(port, degrees, **kwargs):
        port = _get_port(port)
        port.motor.run_for_degrees(degrees, **kwargs)

    def run_to_rel_pos(port, pos, **kwargs):
        port = _get_port(port)
        port.motor.run_to_position(pos, **kwargs)

    def run_to_abs_pos(port, pos, direction = 'fastest', **kwargs):
        port = _get_port(port)
        port.motor.mode([(3, 0)])
        abs_position = port.motor.get()[0]
        to_position = pos - abs_position
        if direction == 'fastest':
            while to_position > 180:
                to_position = to_position - 360
            while to_position < -180:
                to_position = to_position + 360
        if direction == 'left':
            while to_position > 0:
                to_position = to_position - 360
            while to_position < -360:
                to_position = to_position + 360
        if direction == 'right':
            while to_position > 360:
                to_position = to_position - 360
            while to_position < 0:
                to_position = to_position + 360
        port.motor.mode([(2, 0)])
        rel_position = port.motor.get()[0]
        to_rel_position = rel_position + to_position
        port.motor.run_to_position(to_rel_position)

    def set_default(port, **kwargs):
        port = _get_port(port)
        port.motor.default(**kwargs)

class devices:
    class distance_sensor:
        def get_cm(port):
            if get_type(port) != 62:
                raise RuntimeError('No distance sensor (dev 62) connected to port ' + str(port) + '.')
            port = _get_port(port)
            port.device.mode(0)
            return port.device.get()[0]

        def get_inch(port):
            if get_type(port) != 62:
                raise RuntimeError('No distance sensor (dev 62) connected to port ' + str(port) + '.')
            port = _get_port(port)
            port.device.mode(0)
            try:
                return port.device.get()[0] / 2.54
            except:
                return None

        def set_light(port, v1, v2, v3, v4):
            if get_type(port) != 62:
                raise RuntimeError('No distance sensor (dev 62) connected to port ' + str(port) + '.')
            v1 = str(hex(v1))[2:]
            v2 = str(hex(v2))[2:]
            v3 = str(hex(v3))[2:]
            v4 = str(hex(v4))[2:]
            if len(v1) < 2:
                v1 = '0' + v1
            if len(v2) < 2:
                v2 = '0' + v2
            if len(v3) < 2:
                v3 = '0' + v3
            if len(v4) < 2:
                v4 = '0' + v4
            v1 = eval("'\\\\x" + v1 + "'")
            v2 = eval("'\\\\x" + v2 + "'")
            v3 = eval("'\\\\x" + v3 + "'")
            v4 = eval("'\\\\x" + v4 + "'")
            port = _get_port(port)
            port.device.mode(5, v1 + v2 + v3 + v4)

        def get_light(port):
            if get_type(port) != 62:
                raise RuntimeError('No distance sensor (dev 62) connected to port ' + str(port) + '.')
            port = _get_port(port)
            port.device.mode(5)
            return port.device.get()

    class color_sensor:
        def on(port):
            if get_type(port) != 61:
                raise RuntimeError('No color sensor (dev 61) connected to port ' + str(port) + '.')
            port = _get_port(port)
            port.device.mode(8)

        def off(port):
            if get_type(port) != 61:
                raise RuntimeError('No color sensor (dev 61) connected to port ' + str(port) + '.')
            port = _get_port(port)
            port.device.mode(2)

        def get_color(port):
            if get_type(port) != 61:
                raise RuntimeError('No color sensor (dev 61) connected to port ' + str(port) + '.')
            port = _get_port(port)
            port.device.mode(0)
            return port.device.get()[0]

        def get_reflection(port):
            if get_type(port) != 61:
                raise RuntimeError('No color sensor (dev 61) connected to port ' + str(port) + '.')
            port = _get_port(port)
            port.device.mode(1)
            return port.device.get()[0]

        def get_rgb(port):
            if get_type(port) != 61:
                raise RuntimeError('No color sensor (dev 61) connected to port ' + str(port) + '.')
            port = _get_port(port)
            port.device.mode(5)
            return port.device.get()[:3]

    class light_matrix:
        def clear(port):
            if get_type(port) != 64:
                raise RuntimeError('No light matrix (dev 64) connected to port ' + str(port) + '.')
            port = _get_port(port)
            port.device.mode(2)
            port.device.mode(2, '0' * 9)

        def set_color(port, color):
            if get_type(port) != 64:
                raise RuntimeError('No light matrix (dev 64) connected to port ' + str(port) + '.')
            port = _get_port(port)
            port.device.mode(2)
            if type(color) == str:
                if len(color) == 9:
                    port.device.mode(2, color)
                else:
                    raise ValueError('String must be 9 length.')

            elif type(color) == list:
                if len(color) == 9:
                    string = ''
                    for item in color:
                        try:
                            string = string + item
                        except:
                            raise ValueError('List must be 9 strings, not ' + str(type(item)) + '.')

                    port.device.mode(2, string)
                else:
                    raise ValueError('List must be 9 length.')
            else:
                raise TypeError('Color must be str or list (9 length), not ' + str(type(color)) + '.')

    class color_distance_sensor:
        def red(port):
            if get_type(port) != 37:
                raise RuntimeError('No color-distance sensor (dev 37) connected to port ' + str(port) + '.')
            port = _get_port(port)
            port.device.mode(3)

        def green(port):
            if get_type(port) != 37:
                raise RuntimeError('No color-distance sensor (dev 37) connected to port ' + str(port) + '.')
            port = _get_port(port)
            port.device.mode(1)

        def blue(port):
            if get_type(port) != 37:
                raise RuntimeError('No color-distance sensor (dev 37) connected to port ' + str(port) + '.')
            port = _get_port(port)
            port.device.mode(4)

        def white(port):
            if get_type(port) != 37:
                raise RuntimeError('No color-distance sensor (dev 37) connected to port ' + str(port) + '.')
            port = _get_port(port)
            port.device.mode(0)

        def off(port):
            if get_type(port) != 37:
                raise RuntimeError('No color-distance sensor (dev 37) connected to port ' + str(port) + '.')
            port = _get_port(port)
            port.device.mode(5)

        def get_cm(port):
            if get_type(port) != 37:
                raise RuntimeError('No color-distance sensor (dev 37) connected to port ' + str(port) + '.')
            port = _get_port(port)
            port.device.mode(1)
            output =  port.device.get()[0]
            if type(output) == int:
                return output * 2.54
            else:
                return None

        def get_color(port):
            if get_type(port) != 37:
                raise RuntimeError('No color-distance sensor (dev 37) connected to port ' + str(port) + '.')
            port = _get_port(port)
            port.device.mode(0)
            return port.device.get()[0]

        def get_inches(port):
            if get_type(port) != 37:
                raise RuntimeError('No color-distance sensor (dev 37) connected to port ' + str(port) + '.')
            port = _get_port(port)
            port.device.mode(1)
            return port.device.get()[0]

        def get_reflection(port):
            if get_type(port) != 37:
                raise RuntimeError('No color-distance sensor (dev 37) connected to port ' + str(port) + '.')
            port = _get_port(port)
            port.device.mode(3)
            return port.device.get()[0]

        def get_counted(port):
            if get_type(port) != 37:
                raise RuntimeError('No color-distance sensor (dev 37) connected to port ' + str(port) + '.')
            port = _get_port(port)
            port.device.mode(2)
            return port.device.get()[0]

    class force_sensor:
        def get_newton(port):
            if get_type(port) != 63:
                raise RuntimeError('No force sensor (dev 63) connected to port ' + str(port) + '.')
            port = _get_port(port)
            port.device.mode(0)
            return port.device.get()[0]

        def get_newton_float(port):
            if get_type(port) != 63:
                raise RuntimeError('No force sensor (dev 63) connected to port ' + str(port) + '.')
            port = _get_port(port)
            port.device.mode(4)
            return (port.device.get()[0] - 375) / 32

        def get_touch(port):
            if get_type(port) != 63:
                raise RuntimeError('No force sensor (dev 63) connected to port ' + str(port) + '.')
            port = _get_port(port)
            port.device.mode(2)
            return bool(port.device.get()[0])

    class tilt_sensor:
        def get_tilt(port):
            if get_type(port) != 34:
                raise RuntimeError('No tilt sensor (dev 34) connected to port ' + str(port) + '.')
            port = _get_port(port)
            port.device.mode(0)
            return port.device.get()

    class motion_sensor:
        last_count = 0

        def get_inches(port):
            if get_type(port) != 35:
                raise RuntimeError('No motion sensor (dev 35) connected to port ' + str(port) + '.')
            port = _get_port(port)
            port.device.mode(0)
            return port.device.get()[0]

        def get_cm(port):
            if get_type(port) != 35:
                raise RuntimeError('No motion sensor (dev 35) connected to port ' + str(port) + '.')
            port = _get_port(port)
            port.device.mode(0)
            return port.device.get()[0] * 2.54

        def get_counted(port):
            if get_type(port) != 35:
                raise RuntimeError('No motion sensor (dev 35) connected to port ' + str(port) + '.')
            port = _get_port(port)
            port.device.mode(1)
            return port.device.get()[0]

        def get_count_diff(port):
            if get_type(port) != 35:
                raise RuntimeError('No motion sensor (dev 35) connected to port ' + str(port) + '.')
            port = _get_port(port)
            port.device.mode(1)
            count = port.device.get()[0]
            diff = count - devices.motion_sensor.last_count
            devices.motion_sensor.last_count = count
            return diff

def _get_port(port):
    return eval('hub.port.' + port.upper())

def get_type(port):
    port = _get_port(port)
    return port.info()['type']

def pw_up_get(port):
    port = _get_port(port)
    return port.device.get()

def set_mode(port, mode, data = None):
    port = _get_port(port)
    if data:
        port.device.mode(mode, data)
    else:
        port.device.mode(mode)

def get_mode(port):
    port = _get_port(port)
    return port.device.mode()

