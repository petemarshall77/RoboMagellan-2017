# Probe for RoboMagellan USB devices
import subprocess, re

installed_devices = {'95437313334351516052': 'chias-test',
                     '95437313335351514292': 'speedometer-test',
		     '9543731313535140B152': 'chias',
		     '95437313334351519012': 'compass-bump',
		     '9543731333435151B2E1': 'speedometer',
		     '9543731333535131D0D2': 'killswitch'}

def probe():
    ports = {}
    for index in range(10):
        port = '/dev/ttyACM%s' % index
        command = 'udevadm info -a -n %s' % port 
        try:
            out = subprocess.check_output(command.split(),
                                          stderr=subprocess.STDOUT)
            
            regex = re.compile("{serial}==\"(\w+)\"")
            match = regex.search(out)
            if match:
                serial_num = match.group(1)
                if serial_num in installed_devices:
                    ports[installed_devices[serial_num]] = port
        except:
            pass

    return ports

