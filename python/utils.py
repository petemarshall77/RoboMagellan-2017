# MONTY III Utility fuctions

def delta_angle(target, actual):
    delta_angle = target - actual
    if delta_angle > 180:
        return delta_angle - 360
    elif delta_angle < -180:
        return 360 + delta_angle
    return delta_angle 
