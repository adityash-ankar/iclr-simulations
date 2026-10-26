import chamber_geometry
from thermodynamic_functions import run_rocket_cea, initialise_thermal_arrays, GasProps, fuel_phase, get_mach_number
from material_list import Material
import channel_pressure

import numpy as np
import math
import matplotlib.pyplot as plt
from rocketcea.cea_obj import CEA_Obj
from pyfluids import Fluid, FluidsList, Input, Phases
from CoolProp.CoolProp import PropsSI
from scipy.ndimage import median_filter
import scipy as sp

#%%==========================[USER INPUTS]=========================   - create a json script
ox               = 'N2O'
fuel             = 'Ethanol'
material         = 'AlSi10Mg'  # 'Inconel', 'AlSi10Mg', 'ABD900'

Chamber_Pressure = 30.0   # bar
Feed_Pressure    = 40.0   # bar
Thrust_req       = 6000.0 # N
OF               = 3.5  
CR               = 4.5    # contraction ratio Ac/At
Lstar_target_mm  = 600.0  # mm (chamber only)
tw               = 1e-3 # wall thickness [m]
channel_height   = 1.5e-3 # [m]
arc_angle        = 3.8    # degrees
n                = 50     # channels
fcp              = 0.22    # film-cooling percentage 

#Graphs 
Complete_Thermal_Analysis = True
Thermal_Diagnostic_3x3    = False
Film_Cooling_vs_No_FC     = True
SF_and_Temps_3D           = False #Looks Great, Takes like 5 Minutes to run, proceed with caution
Stress_Plot               = True
# Efficiencies
eta_cstar = 0.94
eta_Cf    = 0.98

#%%==========================[CEA / IDEAL PERFORMANCE]=========================  
ISP_vac_ideal,ISP_SL_act,Rt_SI, mdot_act, ISP_SL_act, F_check_SL, Area_Ratio = run_rocket_cea(ox,fuel,OF,Chamber_Pressure,eta_cstar,eta_Cf,Thrust_req)

#%%==========================[GEOMETRY IN mm]=========================
x_full, y_full, Rc_mm, Rt_mm, Re_mm, throat_node_fwd = chamber_geometry.get(Rt_SI, Area_Ratio, CR, Lstar_target_mm)

#%%==========================[CREATE REVERSED ARRAYS]=========================
fuel_mdot   = mdot_act/(OF + 1)
ox_mdot = mdot_act * OF / (OF + 1)
feed_press  = Feed_Pressure*1e5

# Channel width from printing arc
channel_width = (y_full + (tw*1e3) + 0.5*(channel_height*1e3)) * math.sin(math.radians(arc_angle)) * 1e-3  # [m]
w = channel_width
h = channel_height
Dh = 2*h*w/(h+w)

# Wall angle (radians) at nodes (forward)
angles_node = np.zeros_like(y_full, dtype=float)
for i in range(len(y_full)):
    if i == 0 or i == len(y_full)-1:
        angles_node[i] = 0.0
    else:
        dy = y_full[i] - y_full[i-1]
        dx = x_full[i] - x_full[i-1]
        angles_node[i] = math.atan2(dy, dx)


material_class = Material(material)
roughness_array = material_class.surf_roughness(angles_node)

# Reverse for coolant counterflow
rev = {
    'x': x_full[::-1],          # mm
    'r': y_full[::-1],          # mm
    'Dh': Dh[::-1],             # m
    'w': w[::-1],               # m
    'eps': roughness_array[::-1] # m (as k_s)
}
throat_idx_rev = np.argmin(rev['r'])

#%%==========================[THERMAL ARRAYS]=========================
Nseg = len(rev['r']) - 1             # segments in reversed march
qg_array,alpha_t_array, twg_array, twc_array, te_array, tc_array, Mach_array, regen_pressures, Nu_array, Re_array = initialise_thermal_arrays(Nseg)

gas_prop_class = GasProps(ox, fuel, Chamber_Pressure, OF)
T0             = gas_prop_class.T0
cp_g           = gas_prop_class.cp
mu_g           = gas_prop_class.mu
Pr_g           = gas_prop_class.Pr
cstar          = gas_prop_class.c_star
gamma          = gas_prop_class.gamma(Area_Ratio)

Rt = Rt_SI
Dt = 2.0 * Rt
At = np.pi * Rt**2

#%%==========================[MAIN BARTZ LOOP (reversed coolant direction)]=========================

Pc = Chamber_Pressure * 1e5

for i in range(Nseg):  # segment i is between nodes i and i+1 in REVERSED arrays
    # --- Segment midpoint geometry (used everywhere below) ---
    R_mid_m   = 0.5 * (rev['r'][i] + rev['r'][i+1]) * 1e-3   # m
    A_mid     = math.pi * R_mid_m**2                         # m^2
    x_mid_mm  = 0.5 * (rev['x'][i] + rev['x'][i+1])          # m

    # Segment lengths
    dr = abs(rev['r'][i+1] - rev['r'][i]) * 1e-3             # m
    dx = abs(rev['x'][i+1] - rev['x'][i]) * 1e-3             # m
    seg_len = math.hypot(dx, dr)

    # --- Coolant hydraulics on this segment ---
    mass_flow_rate = fuel_mdot / n
    Dh_i  = rev['Dh'][i]
    Aflow = channel_height * rev['w'][i]
    epsilon = rev['eps'][i]

    # pressure reference
    Press_ref = float(feed_press) if i == 0 else float(regen_pressures[i-1])
    Tc_loc    = float(tc_array[i])
    
    boundary = True if i == 0 or i == Nseg - 1 else False
    regen_press = channel_pressure.get_press(Press_ref, Tc_loc, mass_flow_rate, Aflow, Dh_i, epsilon, seg_len, boundary)
    regen_pressures[i] = regen_press
    # coolant props at regen_press
    fuel_st = Fluid(FluidsList.Ethanol).with_state(Input.pressure(regen_press), Input.temperature(Tc_loc - 273.15))  
    fuel_st = fuel_phase(Tc_loc, regen_press, fuel_st)
    rho     = fuel_st.density
    mu_f    = fuel_st.dynamic_viscosity
    lam_c   = fuel_st.conductivity
    cp_c    = fuel_st.specific_heat
    Pr_c    = cp_c * mu_f / lam_c

    Throat_Downstream = True if i < throat_idx_rev else False
    M  = get_mach_number(Area_Ratio, ox, fuel, Pc, OF, Throat_Downstream)
    Mach_array[i] = M
    
    # --- Edge temperature (Bartz recovery) ---
    Pr_use = float(Pr_g) if (np.isfinite(Pr_g) and Pr_g > 0.0) else 0.7
    r      = Pr_use ** (1.0/3.0)
    den    = 1.0 + 0.5*(gamma - 1.0)*M*M
    den    = max(den, 1e-8)  # guard
    Te     = T0 * (1.0 + r*0.5*(gamma - 1.0)*M*M) / den
    te_array[i] = Te
    
    # --- Coolant-side HTC (Dittus-Boelter) ---
    u1   = mass_flow_rate / (rho * Aflow)
    # print(u1, rho, Aflow, mass_flow_rate)
    Re_c = rho * u1 * Dh_i / mu_f
    Nu   = Nusselt_Number(Re_c, Pr_c, fD)
    Nu_array[i] = Nu
    Re_array[i] = Re_c
    alpha_c = Nu * lam_c / Dh_i
    
   # --- Bartz alpha_T using MIDPOINT geometry ratios ---
    At_over_A = At / A_mid
    Dt_over_R = (2.0*Rt) / R_mid_m
    
    # iterative wall solve (with cap + under-relax)
    Twg_0   = Te - 50.0
    tol     = 1e-4
    max_it  = 200
    relax   = 0.45
    
    # guard values
    alpha_c_eff = max(alpha_c, 50.0)
    lambda_w_min = 1.0
    tw_eff = max(tw, 1e-4)
    base2 = max(1.0 + 0.5*(gamma - 1.0)*M*M, 1e-9)
    
    def bartz_alpha_T(Twg_local):
        base1 = 0.5*(Twg_local/max(T0,1e-6))*base2 + 0.5
        base1 = max(base1, 1e-9)
        sigma = (base1 ** -0.68) * (base2 ** -0.12)
        return 0.026 * (Dt**-0.2) * (mu_g**0.2) * cp_g * (Pr_g**-0.6) \
               * ((Pc_SI/cstar)**0.8) * (Dt_over_R**0.1) \
               * (At_over_A**0.9) * sigma
    
    for k in range(max_it):
        alpha_T = bartz_alpha_T(Twg_0)
        qg  = alpha_T * max(Te - Twg_0, 0.0)
        Twc = qg / alpha_c_eff + Tc_loc
    
        if isinstance(conductivity, np.ndarray):
            lambda_w = np.interp((Twg_0+Twc)/2.0, conductivity_temps, conductivity)
        else:
            lambda_w = conductivity
        lambda_w = max(lambda_w, lambda_w_min)
    
        Twg_new = Twc + qg * tw_eff / lambda_w
    
        Twg_1 = (1.0 - relax)*Twg_0 + relax*Twg_new
        if abs(Twg_1 - Twg_0)/max(abs(Twg_1), 1.0) < tol:
            Twg_0 = Twg_1
            break
        Twg_0 = Twg_1
    else:
        # didn’t converge — keep last Twg_0
        pass
    
    # final values after iteration
    alpha_T = bartz_alpha_T(Twg_0)
    qg  = alpha_T * max(Te - Twg_0, 0.0)
    Twc = qg / alpha_c_eff + Tc_loc
    if isinstance(conductivity, np.ndarray):
        lambda_w = np.interp((Twg_0+Twc)/2.0, conductivity_temps, conductivity)
    else:
        lambda_w = conductivity
    lambda_w = max(lambda_w, lambda_w_min)
    
    Twg_1 = Twc + qg * tw_eff / lambda_w

    # ================= IEVLEV BOUNDARY-LAYER COOLING CORRECTION =================
    # Uses q''_film = q''_nofilm * (S_surf / S_core), with S per Ievlev.
    # Assumes the following vars already exist in your loop:
    # T0, M, gamma, Pr_g, mu_g, cp_g, Pc_SI, rev['r'][i], Twg_1, qg, alpha_c_eff,
    # Tc_loc, tw_eff, conductivity, conductivity_temps, lambda_w_min
    
    # --- knobs / safe defaults (change if you have better sources) ---
    try:
        blc_strength = max(0.05, min(0.60, 0.50 * fcp))  # if 'fcp' exists
    except NameError:
        blc_strength = 0.30                               # otherwise use 30%
    T_film_inj    = max(200.0, min(Tc_loc, 700.0))        # K, proxy for injected layer temp
    mu_T_exponent = 0.7                                    # mu ~ T^0.7 for surface layer
    
    # --- core (edge) static state & Re (isentropic relations) ---
    den_isent     = 1.0 + 0.5*(gamma - 1.0)*M*M
    Te_core       = T0 / den_isent                                         # static K
    Rg            = cp_g * (gamma - 1.0) / gamma                           # J/(kg.K)
    P_core        = Pc_SI / (den_isent ** (gamma/(gamma - 1.0)))           # static Pa
    a_core        = (gamma * Rg * Te_core) ** 0.5
    u_core        = M * a_core
    rho_core      = P_core / max(Rg * Te_core, 1e-9)
    D_char        = 2.0 * (rev['r'][i] * 1e-3)                              # m
    Re_core       = rho_core * u_core * D_char / max(mu_g, 1e-12)
    r_recovery    = max(Pr_g, 1e-9) ** (1.0/3.0)
    Taw_core      = T0 * (1.0 + r_recovery * 0.5*(gamma - 1.0)*M*M) / den_isent
    
    # --- surface layer proxy (cooled near-wall mixture) ---
    Te_surf       = (1.0 - blc_strength) * Te_core + blc_strength * T_film_inj
    Te_surf       = max(200.0, min(Te_surf, Te_core))                       # clamp
    T0_surf       = Te_surf * den_isent
    Taw_surf      = T0_surf * (1.0 + r_recovery * 0.5*(gamma - 1.0)*M*M) / den_isent
    mu_surf       = mu_g * (Te_surf / max(Te_core, 1e-9)) ** mu_T_exponent
    a_surf        = (gamma * Rg * Te_surf) ** 0.5
    u_surf        = M * a_surf
    rho_surf      = P_core / max(Rg * Te_surf, 1e-9)
    Re_surf       = rho_surf * u_surf * D_char / max(mu_surf, 1e-12)
    
    # --- Ievlev S-factors (core vs surface layer) ---
    num_core = max(Taw_core - Twg_1, 0.0) * (Te_core ** 0.425) * (mu_g ** 0.15)
    den_core = (Re_core ** 0.425) * ((Te_core + Twg_1) ** 0.595) * ((3.0*Te_core + Twg_1) ** 0.15)
    S_core   = num_core / max(den_core, 1e-30)
    
    num_surf = max(Taw_surf - Twg_1, 0.0) * (Te_surf ** 0.425) * (mu_surf ** 0.15)
    den_surf = (Re_surf ** 0.425) * ((Te_surf + Twg_1) ** 0.595) * ((3.0*Te_surf + Twg_1) ** 0.15)
    S_surf   = num_surf / max(den_surf, 1e-30)
    
    # --- apply correction to convective heat flux; keep within sane bounds ---
    ratio   = max(0.2, min(1.0, S_surf / max(S_core, 1e-30)))  # 0.2–1.0 clamp for stability
    qg_corr = qg * ratio
    
    # --- recompute wall temperatures with corrected convective load ---
    Twc = qg_corr / alpha_c_eff + Tc_loc
    if isinstance(conductivity, np.ndarray):
        lambda_w = np.interp((Twg_1 + Twc)/2.0, conductivity_temps, conductivity)
    else:
        lambda_w = conductivity
    lambda_w = max(lambda_w, lambda_w_min)
    Twg_1 = Twc + qg_corr * tw_eff / lambda_w
    
    # overwrite with film-cooled result
    qg = qg_corr
    # ================= END IEVLEV CORRECTION =================

    # store segment results (still reversed order)
    qg_array[i]       = qg
    alpha_t_array[i]  = alpha_T
    twg_array[i]      = Twg_1
    twc_array[i]      = Twc

    Ahot_seg = 2.0 * math.pi * R_mid_m * seg_len          # m^2
    Q_seg    = qg * Ahot_seg                               # W (J/s)
    tc_array[i+1] = tc_array[i] + Q_seg / (fuel_mdot * cp_c)

# =========================[FLIP to forward gas-flow order]=========================
def flip_seg(arr):
    return arr[-1:0:-1]  # reverse and drop the first element to get length Nseg-1? No:
# Safer: our arrays are length Nseg; we want forward order with same length as forward segments
# Use simple reverse:
def flip_full(arr):
    return arr[::-1]

qg_fwd       = flip_full(qg_array).squeeze()
alphaT_fwd   = flip_full(alpha_t_array).squeeze()
Twg_fwd      = flip_full(twg_array).squeeze()
Twc_fwd      = flip_full(twc_array).squeeze()
Mach_fwd     = flip_full(Mach_array).squeeze()
Tc_fwd_nodes = flip_full(tc_array).squeeze()   # node-based (reversed march had Nseg+1 nodes)
Te_fwd       = flip_full(te_array).squeeze()
Pcool_fwd    = flip_full(regen_pressures).squeeze()
Taw_core     = Twg_fwd + qg_fwd / np.maximum(alphaT_fwd, 1e-9)

# Build forward segment midpoints for plotting (length = len(x_full)-1)
x_nodes_mm = np.asarray(x_full).ravel()
r_nodes_mm = np.asarray(y_full).ravel()
x_seg_mm   = 0.5*(x_nodes_mm[:-1] + x_nodes_mm[1:])
r_seg_mm   = 0.5*(r_nodes_mm[:-1] + r_nodes_mm[1:])
x_throat   = x_nodes_mm[throat_node_fwd]

# tc bulk per segment (avg of adjacent nodes)
Tc_seg = 0.5*(Tc_fwd_nodes[:-1] + Tc_fwd_nodes[1:])



