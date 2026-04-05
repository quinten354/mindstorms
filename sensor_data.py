from time import sleep as wait
import os
import multiprocessing

# start tkinter window
def main(hub):
    # import tkinter
    import tkinter as tk
    from tkinter import Button, Label

    # check if tkinter window still running
    if hub._sdevent.is_set():
        raise RuntimeError('sensor data viewer is already running.')

    def sensor_data_viewer():
        # setup tk window
        hub._to_kill.append(os.getpid())
        hub._sdpid = os.getpid()
        hub._sdevent.set()
        root = tk.Tk()
        root.geometry('600x500')

        # setup tk widgets
        hub._sdwidgets['refresh'] = Button(text = 'Refresh', command = hub.get_sensor_data)
        hub._sdwidgets['refresh'].place(x = 500, y = 10, width = 65, height = 30)
        hub._sdwidgets['auto'] = Button(text = 'Auto', command = hub.startstop_send_sensor_data)
        hub._sdwidgets['auto'].place(x = 500, y = 50, width = 65, height = 30)
        hub._sdwidgets['auto_state'] = Label(text = '')
        hub._sdwidgets['auto_state'].place(x = 575, y = 50, width = 20, height = 30)
        hub._sdwidgets['acceleration'] = Label(text = 'Acceleration')
        hub._sdwidgets['acceleration'].place(x = 10, y = 10, width = 100, height = 30)
        hub._sdwidgets['accelerationx'] = Label(text = '')
        hub._sdwidgets['accelerationx'].place(x = 110, y = 10, width = 50, height = 30)
        hub._sdwidgets['accelerationy'] = Label(text = '')
        hub._sdwidgets['accelerationy'].place(x = 170, y = 10, width = 50, height = 30)
        hub._sdwidgets['accelerationz'] = Label(text = '')
        hub._sdwidgets['accelerationz'].place(x = 230, y = 10, width = 50, height = 30)
        hub._sdwidgets['acceleration'] = Label(text = 'Gyroscope')
        hub._sdwidgets['acceleration'].place(x = 10, y = 50, width = 100, height = 30)
        hub._sdwidgets['gyroscopex'] = Label(text = '')
        hub._sdwidgets['gyroscopex'].place(x = 110, y = 50, width = 50, height = 30)
        hub._sdwidgets['gyroscopey'] = Label(text = '')
        hub._sdwidgets['gyroscopey'].place(x = 170, y = 50, width = 50, height = 30)
        hub._sdwidgets['gyroscopez'] = Label(text = '')
        hub._sdwidgets['gyroscopez'].place(x = 230, y = 50, width = 50, height = 30)
        hub._sdwidgets['yaw'] = Label(text = 'Yaw')
        hub._sdwidgets['yaw'].place(x = 10, y = 90, width = 100, height = 30)
        hub._sdwidgets['yawv'] = Label(text = '')
        hub._sdwidgets['yawv'].place(x = 110, y = 90, width = 50, height = 30)
        hub._sdwidgets['pitch'] = Label(text = 'Pitch')
        hub._sdwidgets['pitch'].place(x = 10, y = 130, width = 100, height = 30)
        hub._sdwidgets['pitchv'] = Label(text = '')
        hub._sdwidgets['pitchv'].place(x = 110, y = 130, width = 50, height = 30)
        hub._sdwidgets['roll'] = Label(text = 'Roll')
        hub._sdwidgets['roll'].place(x = 10, y = 170, width = 100, height = 30)
        hub._sdwidgets['rollv'] = Label(text = '')
        hub._sdwidgets['rollv'].place(x = 110, y = 170, width = 50, height = 30)
        hub._sdwidgets['battery'] = Label(text = 'Battery')
        hub._sdwidgets['battery'].place(x = 230, y = 130, width = 100, height = 30)
        hub._sdwidgets['batteryv'] = Label(text = '')
        hub._sdwidgets['batteryv'].place(x = 330, y = 130, width = 50, height = 30)
        hub._sdwidgets['temperature'] = Label(text = 'Temperature')
        hub._sdwidgets['temperature'].place(x = 230, y = 170, width = 100, height = 30)
        hub._sdwidgets['temperaturev'] = Label(text = '')
        hub._sdwidgets['temperaturev'].place(x = 330, y = 170, width = 50, height = 30)
        hub._sdwidgets['A'] = Label(text = 'Port A: ')
        hub._sdwidgets['A'].place(x = 10, y = 210, height = 30)
        hub._sdwidgets['B'] = Label(text = 'Port B: ')
        hub._sdwidgets['B'].place(x = 10, y = 250, height = 30)
        hub._sdwidgets['C'] = Label(text = 'Port C: ')
        hub._sdwidgets['C'].place(x = 10, y = 290, height = 30)
        hub._sdwidgets['D'] = Label(text = 'Port D: ')
        hub._sdwidgets['D'].place(x = 10, y = 330, height = 30)
        hub._sdwidgets['E'] = Label(text = 'Port E: ')
        hub._sdwidgets['E'].place(x = 10, y = 370, height = 30)
        hub._sdwidgets['F'] = Label(text = 'Port F: ')
        hub._sdwidgets['F'].place(x = 10, y = 410, height = 30)

        def update_sd():
            root.after(500, update_sd)
            update(hub)

        root.after(500, update_sd)

        # mainloop
        root.mainloop()

        # close tk window
        hub._to_kill.remove(os.getpid())
        exit()

    # start process
    process = multiprocessing.Process(target = sensor_data_viewer, daemon = True)
    process.start()

# update window
def update(hub):
    if hub._sdevent.is_set():
        hub._sdevent.clear()
        if hub._sdsend:
            hub._sdwidgets['auto_state']['text'] = 'on'
        else:
            hub._sdwidgets['auto_state']['text'] = 'off'
        try:
            sd = eval(hub._io['sensor_data'])
        except:
            hub.get_sensor_data()
            wait(1)
            try:
                sd = eval(hub._io['sensor_data'])
            except:
                sd = []

        for item in sd:
            if item['type'] == 'acceleration':
                hub._sdwidgets['accelerationx']['text'] = str(item['x'])
                hub._sdwidgets['accelerationy']['text'] = str(item['y'])
                hub._sdwidgets['accelerationz']['text'] = str(item['z'])
            elif item['type'] == 'gyroscope':
                hub._sdwidgets['gyroscopex']['text'] = str(item['x'])
                hub._sdwidgets['gyroscopey']['text'] = str(item['y'])
                hub._sdwidgets['gyroscopez']['text'] = str(item['z'])
            elif item['type'] == 'yaw':
                hub._sdwidgets['yawv']['text'] = str(item['value'])
            elif item['type'] == 'pitch':
                hub._sdwidgets['pitchv']['text'] = str(item['value'])
            elif item['type'] == 'roll':
                hub._sdwidgets['rollv']['text'] = str(item['value'])
            elif item['type'] == 'battery':
                hub._sdwidgets['batteryv']['text'] = str(item['capacity'])
            elif item['type'] == 'temperature':
                hub._sdwidgets['temperaturev']['text'] = str(item['value'])
            elif item['type'] == 'port':
                if not item['device_type']:
                    hub._sdwidgets[item['port']]['text'] = 'Port ' + item['port'] + ': not connected.'
                # color-distance sensor
                elif item['device_type'] == 37:
                    hub._sdwidgets[item['port']]['text'] = 'Port ' + item['port'] + ': ' + item['name'] + ' (' + str(item['device_type']) + '), color: ' + str(item['color']) + ', reflection: ' + str(item['reflection']) + ', counted: ' + str(item['counted']) + ', inches: ' + str(item['inches']) + ', cm: ' + str(item['cm'])
                elif item['device_type'] == 47 or item['device_type'] == 75:
                    hub._sdwidgets[item['port']]['text'] = 'Port ' + item['port'] + ': ' + item['name'] + ' (' + str(item['device_type']) + '), busy: ' + str(item['busy']) + ', speed: ' + str(item['speed']) + ', rel pos: ' + str(item['rel_pos']) + ', abs pos: ' + str(item['abs_pos'])
                elif item['device_type'] == 61:
                    hub._sdwidgets[item['port']]['text'] = 'Port ' + item['port'] + ': ' + item['name'] + ' (' + str(item['device_type']) + '), color: ' + str(item['color']) + ', reflection: ' + str(item['reflection']) + ', rgb: ' + str(item['rgb'])
                elif item['device_type'] == 62:
                    hub._sdwidgets[item['port']]['text'] = 'Port ' + item['port'] + ': ' + item['name'] + ' (' + str(item['device_type']) + '), cm: ' + str(item['cm']) + ', inches: ' + str(item['inches']) + ', light: ' + str(item['light'])
                elif item['device_type'] == 64:
                    hub._sdwidgets[item['port']]['text'] = 'Port ' + item['port'] + ': ' + item['name'] + ' (' + str(item['device_type']) + ')'
                else:
                    hub._sdwidgets[item['port']]['text'] = 'Port ' + item['port'] + ': ' + item['name'] + ' (' + str(item['device_type']) + '): unknown'

