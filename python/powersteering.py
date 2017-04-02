from serial import Serial

# Interface to steering servo and power controller
#    Input values:
#        Steering: from -500 (full left) to +500 (full right)
#        Power:    from -500 (full reverse) to +500 (full forward)
#
#        All values are further constained to limit steering and
#        (especially) power.
STEER_MAX = 500
POWER_MAX = 150

class PowerSteering:

    def __init__(self, port_name, baud_rate, logger):
        self.logger = logger
        self.logger.write("PowerSteering: started.")
        self.serial = Serial(port_name, baud_rate)
        self.current_steer = 0
        self.current_power = 0
        self.set_steer_and_pwr(0,0)

    def stop(self):
        self.logger.write("PowerSteering: stop")
        self.set_steer_and_pwr(0, 0)
        self.current_steer = 0
        self.current_power  = 0

    def set_steer_and_pwr(self, steer_value, power_value):
        self.logger.write("PowerSteering: steer %d, power %d" %
                          (steer_value, power_value))
        # Condition values past
        if steer_value > STEER_MAX:
            steer_value = STEER_MAX
        elif steer_value < -STEER_MAX:
            steer_value = -STEER_MAX
        if power_value > POWER_MAX:
            power_value = POWER_MAX
        elif power_value < -POWER_MAX:
            power_value = -POWER_MAX

        # Save current values
        self.current_steer = steer_value
        self.current_power = power_value

        # Convert to servo values
        steer_value = 1500-steer_value
        power_value = 1500+power_value

        self.serial.write(str(steer_value) + "," + str(int(power_value)))
        self.serial.write('\n')
        self.serial.flush()

    def set_steer(self, steer_value):
        self.set_steer_and_pwr(steer_value, self.current_power)

    def set_power(self, power_value):
        self.set_steer_and_pwr(self.current_steer, power_value)

    def delta_power(self, delta_value):
        self.set_power(self.current_power + delta_value)
