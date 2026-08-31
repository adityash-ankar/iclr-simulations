
def get_press(Press_ref, Tc_loc, mass_flow_rate, Aflow, Dh_i, roughness, seg_len, boundary,
              tol=5e-2, min_p=1e5, max_p=5e8, max_iter=50):
    """
    Iterates channel outlet pressure using Darcy–Weisbach + minor loss.
    Returns converged downstream pressure and ΔP for one segment.
    """
    from pyfluids import Fluid, FluidsList, Input
    from thermal_functions import fuel_phase
    import math

    regen_press = float(Press_ref)
    it = 0

    while True:
        Press_ref = float(regen_press)
        T_celsius = Tc_loc - 273.15

        # fluid properties
        fuel_ref = Fluid(FluidsList.Ethanol).with_state(Input.pressure(Press_ref), Input.temperature(T_celsius))
        fuel_ref = fuel_phase(Tc_loc, Press_ref, fuel_ref)
        rho_ref  = fuel_ref.density
        mu_ref   = fuel_ref.dynamic_viscosity

        # velocity + Reynolds
        u = mass_flow_rate / (rho_ref * Aflow)
        Re = rho_ref * u * Dh_i / mu_ref

        # friction factor
        fD = (-1.8 * math.log10(roughness/(3.7*Dh_i) + (6.9/Re)**1.1))**-2

        # ΔP from friction + minor loss
        dyn = 0.5 * rho_ref * u**2
        dP = fD * (seg_len / Dh_i) * dyn
        if boundary:
            dP += 0.8 * dyn

        # new iterate, clamp
        regen_new = max(min(Press_ref - dP, max_p), min_p)

        # check conv
        if abs(regen_new - Press_ref) / max(Press_ref, min_p) <= tol:
            regen_press = regen_new
            break

        regen_press = regen_new
        it += 1
        if it >= max_iter:
            break

    return float(regen_press), float(dP)
