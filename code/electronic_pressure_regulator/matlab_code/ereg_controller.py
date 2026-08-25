
def ereg_controller(n2_pressure, propellant_pressure, pressure_setpoint, Kp, mdot_prop, rho_prop):
    nd_error = (1 - propellant_pressure/pressure_setpoint) #Non dimensional error
    total_angle_command = nd_error * Kp + feed_forward_angle(n2_pressure, mdot_prop, rho_prop) #In degrees

    return total_angle_command


def feed_forward_angle(n2_pressure, mdot_prop, rho_prop):
    CdA = (mdot_prop / rho_prop) * (n2_pressure) ** -0.5 * 0.9258
    return CdA_to_theta(CdA)

def CdA_to_theta(CdA):
    theta_array = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90]
    CdA_array   = [0, 0.11, 0.22, 0.33, 0.44, 0.55, 0.66, 0.77, 0.88, 0.99]

    # Clamp to LUT limits
    if CdA <= CdA_array[0]:
        return theta_array[0]

    if CdA >= CdA_array[-1]:
        return theta_array[-1]

    # Linear interpolation
    for i in range(len(CdA_array) - 1):
        if CdA_array[i] <= CdA <= CdA_array[i + 1]:

            theta = theta_array[i] + (
                (CdA - CdA_array[i]) /
                (CdA_array[i + 1] - CdA_array[i])
            ) * (theta_array[i + 1] - theta_array[i])

            return theta


# if __name__ == "__main__":
#     Kp = 1 #TBD
#     pressure_setpoint = 60e+05 #bar

#     mdot_prop = 3.26 #TBD
#     rho_prop = 786 #TBD


#     ##ASSUMING MEASURED PRESSURE IN PASCALS
#     total_angle_command = ereg_controller(n2_pressure, propellant_pressure, pressure_setpoint, Kp, mdot_prop, rho_prop)


