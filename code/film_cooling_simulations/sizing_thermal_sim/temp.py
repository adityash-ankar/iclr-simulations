
#%% -------------------------[HELPER FUNCTIONS AND BOOKKEEPING]------------------------
import numpy as np
import math
import matplotlib.pyplot as plt
# Enable LaTeX rendering
plt.rcParams['text.usetex'] = False
plt.rcParams['font.family'] = 'serif'  # This works well with LaTeX
plt.rcParams['text.latex.preamble'] = r''  # Empty or no override
from rocketcea.cea_obj import CEA_Obj
from pyfluids import Fluid, FluidsList, Input, Phases
from CoolProp.CoolProp import PropsSI
from scipy.ndimage import median_filter
import scipy as sp
import sizing_thermal_sim

#%% -------------------------[UNITS: RocketCEA -> SI multipliers]------------------------
_degR_to_K         = 5.0/9.0          # K per degR
_ftps_to_mps       = 0.3048           # m/s per ft/s
_BTUlbmR_to_JkgK   = 4186.8           # J/(kg·K) per (BTU/lbm·°R)
_millipoise_to_Pas = 1e-4             # Pa·s per millipoise
_mcalcmKs_to_WmK   = 418.4            # W/(m·K) per mcal/(cm·K·s)

def ethanol_Tsat_from_P(P_pa):
    P_mmhg = np.asarray(P_pa) / 133.322368
    A1,B1,C1 = 8.20417, 1642.89, 230.3
    A2,B2,C2 = 7.68117, 1332.04, 199.200
    logP = np.log10(P_mmhg)
    T1_C = B1/(A1 - logP) - C1
    T2_C = B2/(A2 - logP) - C2
    T_C  = np.where(T1_C <= 78.3, T1_C, T2_C)
    return T_C + 273.15

def Nusselt_Number(Re_c,Pr_c,fD):
    # if   Re_c < 2300:
    #     Nu = 3.66  # or developing-flow correlation if you track Graetz
    # elif Re_c < 3000:
    #     Nu_turb = (fD/8.0) * (Re_c - 1000.0) * Pr_c / (1.0 + 12.7*math.sqrt(fD/8.0)*(Pr_c**(2.0/3.0) - 1.0))
    #     Nu = 0.5*(0.023*Re_c**0.8*Pr_c**0.4 + Nu_turb)  # smooth blend
    # else:
    #     Nu = (fD/8.0) * (Re_c - 1000.0) * Pr_c / (1.0 + 12.7*math.sqrt(fD/8.0)*(Pr_c**(2.0/3.0) - 1.0))  
    Nu = 0.023 * (Re_c ** 0.8 )* (Pr_c **0.4)
    return(Nu)




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
ISP_vac_ideal,ISP_SL_act,Rt_SI, mdot_act, ISP_SL_act, F_check_SL, Area_Ratio = sizing_thermal_sim.run_rocket_cea(ox,fuel,OF,Chamber_Pressure,eta_cstar,eta_Cf,Thrust_req)
#%%==========================[GEOMETRY IN mm]=========================
x_full, y_full, Rc_mm, Rt_mm, Re_mm, throat_node_fwd = sizing_thermal_sim.get_chamber_geometry(Rt_SI, Area_Ratio, CR, Lstar_target_mm)
#%%==========================[REGEN PREP]=========================
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
# Roughness from build angle; clip to table range for continuity

mat       = Materi
roughness_node = np.interp(angles_clipped, manufacturing_angle, Surf_roughness)

# Reverse for coolant counterflow
rev = {
    'x': x_full[::-1],          # mm
    'r': y_full[::-1],          # mm
    'Dh': Dh[::-1],             # m
    'w': w[::-1],               # m
    'eps': roughness_node[::-1] # m (as k_s)
}
throat_idx_rev = np.argmin(rev['r'])

#%%==========================[THERMAL ARRAYS]=========================
Nseg = len(rev['r']) - 1             # segments in reversed march
qg_array,alpha_t_array, twg_array, twc_array, te_array, tc_array, Mach_array, regen_pressures, Nu_array, Re_array = sizing_thermal_sim.initialise_thermal_arrays(Nseg)
T0, cp_g, mu_g, Pr_g, cstar, gamma = sizing_thermal_sim.get_gas_props(ox, fuel, Chamber_Pressure, OF, Area_Ratio)

Rt = Rt_SI
Dt = 2.0 * Rt
At = np.pi * Rt**2

#%%==========================[MAIN BARTZ LOOP (reversed coolant direction)]=========================

# Ethanol critical point (CoolProp values)
_ETH_Tc = 514.0        # K (approx)
_ETH_Pc = 6.38e6       # Pa (approx)

def fuel_phase(Tc_loc_K, regen_press, fuel_st, *, pressure_in_pa=True):
    """
    Robust ethanol state chooser for PyFluids:
    - Lets EOS decide from (P,T) first.
    - If that fails, picks phase by Tsat(P), then retries.
    - Adds tiny nudges near saturation to avoid singularities.
    - Expects Tc_loc_K in Kelvin. 'regen_press' in Pa if pressure_in_pa=True, else bar.
    Returns: a PyFluids Fluid(FluidsList.Ethanol) at the requested state.
    """

    # --- Units ---
    P = float(regen_press if pressure_in_pa else regen_press * 1e5)  # Pa
    T_K = float(Tc_loc_K)                                            # K
    T_C = T_K - 273.15                                               # °C (PyFluids expects °C)
    if not (np.isfinite(P) and np.isfinite(T_K)) or P <= 0.0:
        raise ValueError(f"Bad inputs to fuel_phase: P={P} Pa, T={T_K} K")

    # Use a FRESH instance so we don't carry a previously specified phase
    fs = Fluid(FluidsList.Ethanol)

    # Quick supercritical check: if clearly supercritical, don't force a phase
    if (P > 0.99*_ETH_Pc and T_K > 0.99*_ETH_Tc):
        try:
            return fs.with_state(Input.pressure(P), Input.temperature(T_C))
        except ValueError:
            # tiny nudge in T to get off critical manifold
            return fs.with_state(Input.pressure(P), Input.temperature((T_K + 0.2) - 273.15))

    # First try: let backend pick the region automatically
    try:
        return fs.with_state(Input.pressure(P), Input.temperature(T_C))
    except ValueError:
        # Decide side of saturation line
        try:
            Tsat_K = PropsSI('T', 'P', P, 'Q', 0, 'Ethanol')  # sat. liquid T at this P
        except Exception as e:
            # If saturation query fails (rare), nudge T and retry auto
            return fs.with_state(Input.pressure(P), Input.temperature((T_K + 0.2) - 273.15))

        # Stay a hair away from the coexistence curve to avoid singularities
        eps = 0.15  # K
        if T_K < Tsat_K - eps:
            fs.specify_phase(Phases.Liquid)
            T_try = T_K + eps
        elif T_K > Tsat_K + eps:
            fs.specify_phase(Phases.Gas)
            T_try = T_K - eps
        else:
            # Within epsilon of Tsat: treat as liquid side for regen coolant
            fs.specify_phase(Phases.Liquid)
            T_try = Tsat_K - eps

        # Retry with explicit phase
        try:
            return fs.with_state(Input.pressure(P), Input.temperature(T_try - 273.15))
        except ValueError:
            # Final fallback: tiny additional nudge
            return fs.with_state(Input.pressure(P), Input.temperature((T_try + 0.3) - 273.15))

        
for i in range(Nseg):  # segment i is between nodes i and i+1 in REVERSED arrays
    # --- Segment midpoint geometry (used everywhere below) ---
    R_mid_m   = 0.5 * (rev['r'][i] + rev['r'][i+1]) * 1e-3   # m
    A_mid     = math.pi * R_mid_m**2                         # m^2
    x_mid_mm  = 0.5 * (rev['x'][i] + rev['x'][i+1])          # mm

    # Segment lengths
    dr = abs(rev['r'][i+1] - rev['r'][i]) * 1e-3             # m
    dx = abs(rev['x'][i+1] - rev['x'][i]) * 1e-3             # m
    seg_len = math.hypot(dx, dr)

    # --- Coolant hydraulics on this segment ---
    mass_flow_rate = fuel_mdot / n
    Dh_i  = rev['Dh'][i]
    Aflow = channel_height * rev['w'][i]

    # pressure reference
    Press_ref = float(feed_press) if i == 0 else float(regen_pressures[i-1])
    Tc_loc    = float(tc_array[i])

    # 1) provisional pressure drop then one light iterate
    fuel_ref = Fluid(FluidsList.Ethanol).with_state(Input.pressure(Press_ref), Input.temperature(Tc_loc - 273.15))
    fuel_ref = fuel_phase(Tc_loc, Press_ref, fuel_ref)
    rho_ref  = fuel_ref.density
    mu_f_ref = fuel_ref.dynamic_viscosity
    u1       = mass_flow_rate/(rho_ref*Aflow)
    Re_c     = rho_ref * u1 * Dh_i / mu_f_ref
    # Darcy with roughness (k_s ~ eps)
    fD = (-1.8*math.log10(rev['eps'][i]/(3.7*Dh_i) + (6.9/Re_c)**1.1))**-2
    dyn_head   = 0.5*rho_ref*u1**2
    dP_segment = fD * seg_len/Dh_i * dyn_head
    if i == 0 or i == (Nseg-1):
        dP_segment += 0.8*dyn_head
    regen_press = float(Press_ref - dP_segment)     # Pa
    regen_press = max(regen_press, 1e5)             # guard: avoid ≤ 0 Pa
    regen_pressures[i] = regen_press

    # refine once
    if abs(regen_press - Press_ref)/Press_ref > 5e-2:
        Press_ref = float(regen_press)
        fuel_ref = Fluid(FluidsList.Ethanol).with_state(Input.pressure(Press_ref), Input.temperature(Tc_loc - 273.15))
        fuel_ref = fuel_phase(Tc_loc, Press_ref, fuel_ref)
        rho_ref  = fuel_ref.density
        mu_f_ref = fuel_ref.dynamic_viscosity
        u1       = mass_flow_rate/(rho_ref*Aflow)
        Re_c     = rho_ref*u1*Dh_i/mu_f_ref
        fD       = (-1.8*math.log10(rev['eps'][i]/(3.7*Dh_i) + (6.9/Re_c)**1.1))**-2
        dyn_head = 0.5*rho_ref*u1**2
        dP_segment = fD * seg_len/Dh_i * dyn_head
        if i == 0 or i == (Nseg-1):
            dP_segment += 0.8*dyn_head
        regen_press = Press_ref - dP_segment

    regen_pressures[i] = regen_press

    # coolant props at regen_press
    fuel_st = Fluid(FluidsList.Ethanol).with_state(Input.pressure(regen_press), Input.temperature(Tc_loc - 273.15))  
    fuel_st = fuel_phase(Tc_loc, regen_press, fuel_st)
    rho     = fuel_st.density
    mu_f    = fuel_st.dynamic_viscosity
    lam_c   = fuel_st.conductivity
    cp_c    = fuel_st.specific_heat
    Pr_c    = cp_c * mu_f / lam_c

    # --- Mach number from area ratio at segment MIDPOINT ---
    if (i + 0.5) > throat_idx_rev:
        # upstream of throat (subsonic)
        M = ispObj.get_Chamber_MachNumber(Pc=Pc_psia, MR=OF, fac_CR=A_mid/At)
    elif (i + 0.5) < throat_idx_rev:
        # downstream (supersonic)
        M = ispObj.get_MachNumber(Pc=Pc_psia, MR=OF, eps=A_mid/At,
                                  frozen=0, frozenAtThroat=0)
    else:
        M = 1.0
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

#%%==========================[FILM COOLING]========================= Use boolean
cp_g_array     = np.zeros_like(x_seg_mm) #Specific heat capacity of freestream gas in chamber
Pr_g_array     = np.zeros_like(x_seg_mm) #Prandtl number of freestream gas in chamber
mu_g_array     = np.zeros_like(x_seg_mm) #Viscosity of freestream gas in chamber
gamma_array    = np.zeros_like(x_seg_mm) #Ratio of specific heat capacities for freestream gas in chamber
Mg_array       = np.zeros_like(x_seg_mm) #Molecular weight of freestream gas in chamber
pressure_array = np.zeros_like(x_seg_mm)
T_fcool_array  = np.zeros_like(x_seg_mm)
Gamma_array    = np.zeros_like(x_seg_mm)
h_corr_array   = np.zeros_like(x_seg_mm)
q_corr_array   = np.zeros_like(x_seg_mm)
throat_idx     = np.argmin(r_seg_mm)
Mv             = 46 #g/mol for Ethanol
Km_array       = np.zeros_like(x_seg_mm) #Blowing factor correction term
eps_array      = r_seg_mm**2 / np.min(r_seg_mm)**2
ethanol_latent_heat_vap = 2.5e5 #J/kg

dx_seg_m = np.diff(x_nodes_mm) * 1e-3  # length = Nseg
def dx_at(i):
    # safe pick even at the last usable index
    return float(dx_seg_m[min(i, dx_seg_m.size-1)])


for i in range(len(x_seg_mm)):
    cp_g_array[i], mu_g_array[i], _, Pr_g_array[i] = ispObj.get_Chamber_Transport(Pc=Pc_psia, MR=OF, frozen=0, eps = eps_array[i])
    cp_g_array[i]*=_BTUlbmR_to_JkgK
    Mg_array[i],gamma_array[i] = ispObj.get_Chamber_MolWt_gamma(Pc=Pc_psia, MR=OF, eps = eps_array[i])
    Km_array[i] = (Mg_array[i]/Mv)**0.6 if Mg_array[i]>Mv else (Mg_array[i]/Mv)**0.35 
    g = float(gamma_array[i])
    M = float(Mach_fwd[i])
    pressure_array[i] = Pc_SI / (1.0 + 0.5*(g-1.0)*M*M)**(g/(g-1.0))
    
#-----------------------------------[LIQUID FILM]--------------------------------------------------
#Initially, since film cooling is injected at x=0
Gamma_init  = (fuel_mdot*fcp)/(2*np.pi*r_seg_mm[0]*1e-3) #Initial Mass flow of coolant per unit circumference
T_fcoolant  = np.max(Tc_seg)
dT_liq      = 0
Gamma       = Gamma_init
burnout_idx = None
for i in range(throat_idx):
    Tsat             = ethanol_Tsat_from_P(pressure_array[i])
    T_fcool_array[i] = T_fcoolant
    coolant_ref      = Fluid(FluidsList.Ethanol).with_state(Input.pressure(pressure_array[i]), Input.temperature(T_fcoolant - 273.15))
    cp_cool_liq      = coolant_ref.specific_heat  # J/(kg·K) from PyFluids
    h0               = alphaT_fwd[i]
    q_conv0          = h0 * (Te_fwd[i] - T_fcoolant)
    mdotvap          = q_conv0/max(ethanol_latent_heat_vap,1.0)

    wet_P            = 2 *np.pi * r_seg_mm[i] *1e-3
        
    DeltaT = max(Te_fwd[i] - T_fcoolant, 0.0)                 # Te_fwd is your Taw(core)
    H      = (cp_g_array[i] * Km_array[i] / ethanol_latent_heat_vap) * DeltaT
    h      = h0 * np.log1p(H) / max(H, 1e-12)                 # correction outside the log
    
    h_corr_array[i] = h
    
    Gamma_array[i] = Gamma
    
    # Use per-span heat: (W/m^2)*m -> W/m  (no perimeter here)
    dx_seg = dx_at(i)  # or your unified dx
    q_to_film_per_span = qg_fwd[i] * dx_seg
    
    # Liquid film temperature rise (per-span energy balance)
    dT_liq      = q_to_film_per_span / max(Gamma * cp_cool_liq, 1e-12)
    T_fcoolant += dT_liq
    
    # When at saturation: evaporate film (per-span mass removal)
    if T_fcoolant >= Tsat - 1e-9:
        T_fcoolant = Tsat
        # mdotvap is kg/(m^2·s); multiply by dx [m] -> kg/(m·s) per span
        dGamma = - mdotvap * dx_seg
        Gamma  = max(Gamma + dGamma, 1e-12)
        if Gamma < 1e-8:
            burnout_idx = i
            break

    
# If never burned out in chamber region
if burnout_idx is None:
    burnout_idx = throat_idx


# ------------------------------[GAS FILM — per-span m′]------------------------------
L = len(twg_array)

# Per-span film mass flow m′ (kg/(m·s))
mbl        = np.zeros(L - burnout_idx, dtype=float)
P0         = 2*np.pi*max(r_seg_mm[burnout_idx]*1e-3, 1e-9)
mbl[0]   = max(Gamma_init, 1e-8) 

# Per-span bookkeeping terms (entrainment, geometry, etc.)
dmb1       = np.zeros_like(mbl)  # predictor (entrainment only), per-span
dmb2       = np.zeros_like(mbl)  # corrector (entrainment only), per-span
dmb_e      = np.zeros_like(mbl)  # entrained increment this step, per-span
dmb_geom   = np.zeros_like(mbl)  # geometry (area-change) increment, per-span

# Temperature bookkeeping
dTe        = np.zeros_like(mbl)
Taw_fc_g   = np.zeros_like(mbl)
Tsat_burn = ethanol_Tsat_from_P(pressure_array[burnout_idx])
Taw_seed  = np.clip(Tsat_burn, T_fcoolant, Taw_core[burnout_idx])
Taw_fc_g[0] = Taw_seed


for i in range(burnout_idx, L-1):
    j = i - burnout_idx  # zero-index for the reduced arrays

    Kt = 1.0
    Km = (Mv / max(Mg_array[i], 1e-12))**0.14   # (kept as you have it)
    
    P_i             = 2 * np.pi  * r_seg_mm[i] * 1e-3
    # Core external mass flux (kg/m^2/s). If you separate streams elsewhere, keep this as-is.
    mdotgas         = (ox_mdot + fuel_mdot*(1 - fcp))
    A_g             = np.pi * (max(r_seg_mm[i]*1e-3, 1e-9))**2
    mdot_total_core = (ox_mdot + fuel_mdot*(1 - fcp))
    mdot_film       = mbl[j] * P_i                   # per-span * perimeter -> kg/s
    mdot_core_free  = max(mdot_total_core - mdot_film, 1e-9)
    G               = mdot_core_free / max(A_g, 1e-9)

    # Film properties at the local film temperature
    ethanol_gas = Fluid(FluidsList.Ethanol).with_state(
        Input.pressure(pressure_array[i]),
        Input.temperature(Taw_fc_g[j] - 273.15)
    )
    cp_c = ethanol_gas.specific_heat

    # Geometry terms
    D   = 2.0 * max(r_seg_mm[i]*1e-3, 1e-9)                  # local diameter [m]
    dD  = 2.0 * (r_seg_mm[i+1] - r_seg_mm[i]) * 1e-3         # finite diff ∆D over segment [m]
    dx  = max(dx_at(i), 1e-12)                             # segment length

    # Local perimeters (start/end of segment)
    P_i   = 2*np.pi*max(r_seg_mm[i]*1e-3,   1e-9)
    P_ip1 = 2*np.pi*max(r_seg_mm[i+1]*1e-3, 1e-9)

    # ---------------- Entrainment growth (per-span) with predictor–corrector ---------------
    # Predictor at station i
    mu_g_i = mu_g_array[i]
    m_i    = max(mbl[j], 1e-12)
    dmb1[j]= 0.1963 * Kt * G * (mu_g_i / m_i)**0.25 * dx

    # Corrector using provisional m′ at i+1
    m_p    = max(mbl[j] + dmb1[j], 1e-12)
    mu_g_ip1 = mu_g_array[i+1]
    # Use same dx for the step (safer than indexing dx_array[i+1] at the end of domain)
    dmb2[j]= 0.1963 * Kt * G * (mu_g_ip1 / m_p)**0.25 * dx

    # Trapezoidal average entrainment increment (per-span)
    dmb_e[j] = 0.5 * (dmb1[j] + dmb2[j])

    # ---------------- Geometry (area-change) term (per-span) ----------------
    # dm'/dx|geom ≈ - m' * (1/D) * dD/dx  -> finite-diff over the segment:
    dmb_geom[j] = - m_i * (dD / max(D, 1e-12))

    # ---------------- Update film per-span mass flow ----------------
    m_next = mbl[j] + dmb_e[j] + dmb_geom[j]
    mbl[j+1] = max(m_next, 1e-12)

    # ---------------- Temperature update (use TOTALS for heat capacities) ----------------
    # Convert per-span to totals at station i using P_i
    m_f_tot = mbl[j]        * P_i           # film already in the layer
    m_e_tot = max(dmb_e[j], 0.0) * P_i      # entrained this step (only the positive part)

    # External reference temperature (kept as your Te_fwd; if you prefer recovery, swap here)
    Tr = Taw_core[i]

    C_f   = m_f_tot * max(cp_c, 1e-6)                   # film capacity rate
    C_e   = m_e_tot * Km * max(cp_g_array[i], 1e-6)     # external (weighted) capacity rate
    denom = max(C_f + C_e, 1e-9)

    dTe[j]        = (Tr - Taw_fc_g[j]) * (C_e / denom)
    Taw_fc_g[j+1] = Taw_fc_g[j] + dTe[j]

    
#-------------------------------------[REDOING BARTZ WITH FILM COOLING]--------------------------------------------

#Initialise reversed arrays for film cooling thermals
Twg_fc_rev        = np.zeros_like(Twg_fwd)
Twc_fc_rev        = np.zeros_like(Twg_fwd)
Tc_fc_rev         = np.zeros_like(Twg_fwd)
Pc_fc_rev         = np.zeros_like(Twg_fwd)
qg_fc_rev         = np.zeros_like(Twg_fwd)
Tc_fc_rev[0]      = 300.0

#Assign new h for liquid region and keep old h for gaseous region:
h_fc_array        = np.concatenate((h_corr_array[:burnout_idx+1], alphaT_fwd[burnout_idx+1:]))
h_fc_array_rev    = flip_full(h_fc_array)
burnout_idx_rev   = len(h_fc_array_rev) - burnout_idx 

#Assign new Taw for gaseous region and keep old Taw for liquid region:
Taw_fc_array        = np.concatenate((Taw_core[:burnout_idx+1], Taw_fc_g[1:]))
Taw_fc_array_rev    = flip_full(Taw_fc_array)

for i in range(len(Twg_fc_rev)-1):
    # --- Segment midpoint geometry (used everywhere below) ---
    R_mid_m   = 0.5 * (rev['r'][i] + rev['r'][i+1]) * 1e-3   # m
    A_mid     = math.pi * R_mid_m**2                         # m^2
    x_mid_mm  = 0.5 * (rev['x'][i] + rev['x'][i+1])          # mm

    # Segment lengths
    dr = abs(rev['r'][i+1] - rev['r'][i]) * 1e-3             # m
    dx = abs(rev['x'][i+1] - rev['x'][i]) * 1e-3             # m
    seg_len = math.hypot(dx, dr)

    # --- Coolant hydraulics on this segment ---
    mass_flow_rate = fuel_mdot / n
    Dh_i  = rev['Dh'][i]
    Aflow = channel_height * rev['w'][i]

    # pressure reference
    Press_ref = float(feed_press) if i == 0 else float(regen_pressures[i-1])
    Tc_loc    = float(Tc_fc_rev[i]) 

    # 1) provisional pressure drop then one light iterate
    fuel_ref = Fluid(FluidsList.Ethanol).with_state(Input.pressure(Press_ref), Input.temperature(Tc_loc - 273.15))
    fuel_ref = fuel_phase(Tc_loc, Press_ref, fuel_ref)
    rho_ref  = fuel_ref.density
    mu_f_ref = fuel_ref.dynamic_viscosity
    u1       = mass_flow_rate/(rho_ref*Aflow)
    Re_c     = rho_ref * u1 * Dh_i / mu_f_ref
    # Darcy with roughness (k_s ~ eps)
    fD = (-1.8*math.log10(rev['eps'][i]/(3.7*Dh_i) + (6.9/Re_c)**1.1))**-2
    dyn_head   = 0.5*rho_ref*u1**2
    dP_segment = fD * seg_len/Dh_i * dyn_head
    if i == 0 or i == (Nseg-1):
        dP_segment += 0.8*dyn_head
    regen_press = float(Press_ref - dP_segment)     # Pa
    regen_press = max(regen_press, 1e5)             # guard: avoid ≤ 0 Pa
    regen_pressures[i] = regen_press

    # refine once
    if abs(regen_press - Press_ref)/Press_ref > 5e-2:
        Press_ref = float(regen_press)
        fuel_ref = Fluid(FluidsList.Ethanol).with_state(Input.pressure(Press_ref), Input.temperature(Tc_loc - 273.15))
        fuel_ref = fuel_phase(Tc_loc, Press_ref, fuel_ref)
        rho_ref  = fuel_ref.density
        mu_f_ref = fuel_ref.dynamic_viscosity
        u1       = mass_flow_rate/(rho_ref*Aflow)
        Re_c     = rho_ref*u1*Dh_i/mu_f_ref
        fD       = (-1.8*math.log10(rev['eps'][i]/(3.7*Dh_i) + (6.9/Re_c)**1.1))**-2
        dyn_head = 0.5*rho_ref*u1**2
        dP_segment = fD * seg_len/Dh_i * dyn_head
        if i == 0 or i == (Nseg-1):
            dP_segment += 0.8*dyn_head
        regen_press = Press_ref - dP_segment

    regen_pressures[i] = regen_press

    # coolant props at regen_press
    fuel_st = Fluid(FluidsList.Ethanol)
    fuel_st = fuel_phase(Tc_loc, regen_press, fuel_st)
    rho     = fuel_st.density
    mu_f    = fuel_st.dynamic_viscosity
    lam_c   = fuel_st.conductivity
    cp_c    = fuel_st.specific_heat
    Pr_c    = cp_c * mu_f / lam_c

    # --- Mach number from area ratio at segment MIDPOINT ---
    if (i + 0.5) > throat_idx_rev:
        # upstream of throat (subsonic)
        M = ispObj.get_Chamber_MachNumber(Pc=Pc_psia, MR=OF, fac_CR=A_mid/At)
    elif (i + 0.5) < throat_idx_rev:
        # downstream (supersonic)
        M = ispObj.get_MachNumber(Pc=Pc_psia, MR=OF, eps=A_mid/At,
                                  frozen=0, frozenAtThroat=0)
    else:
        M = 1.0
    Mach_array[i] = M
    
    # --- Coolant-side HTC (Dittus-Boelter) ---
    u1   = mass_flow_rate / (rho * Aflow)
    Re_c = rho * u1 * Dh_i / mu_f
    Nu   = Nusselt_Number(Re_c, Pr_c, fD)
    alpha_c = Nu * lam_c / Dh_i

    # iterative wall solve (with cap + under-relax)
    Taw     = Taw_fc_array_rev[i]
    Twg_0   = Taw - 50.0
    tol     = 1e-4
    max_it  = 200
    
    # guard values
    alpha_c_eff = max(alpha_c, 1e-9)
    lambda_w_min = 1.0
    tw_eff = max(tw, 1e-4)
    base2 = max(1.0 + 0.5*(gamma - 1.0)*M*M, 1e-9)
    
    if isinstance(conductivity, np.ndarray):
        lambda_w = np.interp((Twg_0+Twc)/2.0, conductivity_temps, conductivity)
    else:
        lambda_w = conductivity
    lambda_w = max(lambda_w, lambda_w_min)

    h   = h_fc_array_rev[i] 
    qg_i  = (Taw_fc_array_rev[i] - Tc_loc)/(1/h + 1/alpha_c_eff + tw/lambda_w)
    Twc = qg_i / alpha_c_eff + Tc_loc   
    Twg_1 = Taw_fc_array_rev[i] - qg_i/h
    
    # store segment results (still reversed order)
    qg_fc_rev[i]       = qg_i
    Twg_fc_rev[i]      = Twg_1
    Twc_fc_rev[i]      = Twc

    Ahot_seg = 2.0 * math.pi * R_mid_m * seg_len          # m^2
    Q_seg    = qg_i * Ahot_seg                               # W (J/s)
    Tc_fc_rev[i+1] = Tc_fc_rev[i] + Q_seg / (fuel_mdot * cp_c)
    
Tc_max = np.max(Tc_fc_rev)
# After the for-loop that fills qg_fc_rev, Twg_fc_rev, Twc_fc_rev
Twg_fc_rev[-1] = Twg_fc_rev[-2]
Twc_fc_rev[-1] = Twc_fc_rev[-2]
qg_fc_rev[-1]  = qg_fc_rev[-2]


#%%--------------------------[RUN CODE UNTIL COOLANT TEMP CONVERGES]----------------------------------------
iter_count = 0
while abs(Tc_fc_rev[-1] - T_fcool_array[0])/T_fcool_array[0] >1e-4 and iter_count < 25:
    #-----------------------------------[LIQUID FILM]--------------------------------------------------
    #Initially, since film cooling is injected at x=0
    Gamma_init  = (fuel_mdot*fcp)/(2*np.pi*r_seg_mm[0]*1e-3) #Initial Mass flow of coolant per unit circumference
    T_fcoolant  = Tc_fc_rev[-1]
    dT_liq      = 0
    Gamma       = Gamma_init
    burnout_idx = None
    for i in range(throat_idx):
        Tsat             = ethanol_Tsat_from_P(pressure_array[i])
        T_fcool_array[i] = T_fcoolant
        coolant_ref      = Fluid(FluidsList.Ethanol).with_state(Input.pressure(pressure_array[i]), Input.temperature(T_fcoolant - 273.15))
        cp_cool_liq      = coolant_ref.specific_heat  # J/(kg·K) from PyFluids
        h0               = alphaT_fwd[i]
        q_conv0          = h0 * (Te_fwd[i] - T_fcoolant)
        mdotvap          = q_conv0/max(ethanol_latent_heat_vap,1.0)
    
        wet_P            = 2 *np.pi * r_seg_mm[i] *1e-3
            
        DeltaT = max(Te_fwd[i] - T_fcoolant, 0.0)                 # Te_fwd is your Taw(core)
        H      = (cp_g_array[i] * Km_array[i] / ethanol_latent_heat_vap) * DeltaT
        h      = h0 * np.log1p(H) / max(H, 1e-12)                 # correction outside the log
        
        h_corr_array[i] = h
        
        Gamma_array[i] = Gamma
        q_to_film   = qg_fwd[i] * wet_P * dx_at(i)  # W/m² * m * m = J/m (per circumference)
        dT_liq      = q_to_film / max(Gamma*cp_cool_liq, 1e-12)
        T_fcoolant += dT_liq
        if T_fcoolant >= Tsat - 1e-9:
            T_fcoolant = Tsat
            dGamma = - mdotvap * wet_P * dx_at(i)           # kg/s/m (per circumference)
            Gamma  = Gamma + dGamma
            if Gamma < 1e-8:
                burnout_idx = i
                break
        
    # If never burned out in chamber region
    if burnout_idx is None:
        burnout_idx = throat_idx
    
    
    # ------------------------------[GAS FILM — per-span m′]------------------------------
    L = len(twg_array)
    
    # Per-span film mass flow m′ (kg/(m·s))
    mbl        = np.zeros(L - burnout_idx, dtype=float)
    P0         = 2*np.pi*max(r_seg_mm[burnout_idx]*1e-3, 1e-9)
    mbl[0]   = max(Gamma_init, 1e-8) 
    
    # Per-span bookkeeping terms (entrainment, geometry, etc.)
    dmb1       = np.zeros_like(mbl)  # predictor (entrainment only), per-span
    dmb2       = np.zeros_like(mbl)  # corrector (entrainment only), per-span
    dmb_e      = np.zeros_like(mbl)  # entrained increment this step, per-span
    dmb_geom   = np.zeros_like(mbl)  # geometry (area-change) increment, per-span
    
    # Temperature bookkeeping
    dTe        = np.zeros_like(mbl)
    Taw_fc_g   = np.zeros_like(mbl)
    Tsat_burn = ethanol_Tsat_from_P(pressure_array[burnout_idx])
    Taw_seed  = np.clip(Tsat_burn, T_fcoolant, Taw_core[burnout_idx])
    Taw_fc_g[0] = Taw_seed

    for i in range(burnout_idx, L-1):
        j = i - burnout_idx  # zero-index for the reduced arrays
    
        Kt = 1.0
        Km = (Mv / max(Mg_array[i], 1e-12))**0.14   # (kept as you have it)
        
        P_i             = 2 * np.pi  * r_seg_mm[i] * 1e-3
        # Core external mass flux (kg/m^2/s). If you separate streams elsewhere, keep this as-is.
        mdotgas         = (ox_mdot + fuel_mdot*(1 - fcp))
        A_g             = np.pi * (max(r_seg_mm[i]*1e-3, 1e-9))**2
        mdot_total_core = (ox_mdot + fuel_mdot*(1 - fcp))
        mdot_film       = mbl[j] * P_i                   # per-span * perimeter -> kg/s
        mdot_core_free  = max(mdot_total_core - mdot_film, 1e-9)
        G               = mdot_core_free / max(A_g, 1e-9)
    
        # Film properties at the local film temperature
        ethanol_gas = Fluid(FluidsList.Ethanol).with_state(
            Input.pressure(pressure_array[i]),
            Input.temperature(Taw_fc_g[j] - 273.15)
        )
        cp_c = ethanol_gas.specific_heat
    
        # Geometry terms
        D   = 2.0 * max(r_seg_mm[i]*1e-3, 1e-9)                  # local diameter [m]
        dD  = 2.0 * (r_seg_mm[i+1] - r_seg_mm[i]) * 1e-3         # finite diff ∆D over segment [m]
        dx  = max(dx_at(i), 1e-12)                             # segment length
    
        # Local perimeters (start/end of segment)
        P_i   = 2*np.pi*max(r_seg_mm[i]*1e-3,   1e-9)
        P_ip1 = 2*np.pi*max(r_seg_mm[i+1]*1e-3, 1e-9)
    
        # ---------------- Entrainment growth (per-span) with predictor–corrector ---------------
        # Predictor at station i
        mu_g_i = mu_g_array[i]
        m_i    = max(mbl[j], 1e-12)
        dmb1[j]= 0.1963 * Kt * G * (mu_g_i / m_i)**0.25 * dx
    
        # Corrector using provisional m′ at i+1
        m_p    = max(mbl[j] + dmb1[j], 1e-12)
        mu_g_ip1 = mu_g_array[i+1]
        # Use same dx for the step (safer than indexing dx_array[i+1] at the end of domain)
        dmb2[j]= 0.1963 * Kt * G * (mu_g_ip1 / m_p)**0.25 * dx
    
        # Trapezoidal average entrainment increment (per-span)
        dmb_e[j] = 0.5 * (dmb1[j] + dmb2[j])
    
        # ---------------- Geometry (area-change) term (per-span) ----------------
        # dm'/dx|geom ≈ - m' * (1/D) * dD/dx  -> finite-diff over the segment:
        dmb_geom[j] = - m_i * (dD / max(D, 1e-12))
    
        # ---------------- Update film per-span mass flow ----------------
        m_next = mbl[j] + dmb_e[j] + dmb_geom[j]
        mbl[j+1] = max(m_next, 1e-12)
    
        # ---------------- Temperature update (use TOTALS for heat capacities) ----------------
        # Convert per-span to totals at station i using P_i
        m_f_tot = mbl[j]        * P_i           # film already in the layer
        m_e_tot = max(dmb_e[j], 0.0) * P_i      # entrained this step (only the positive part)
    
        # External reference temperature (kept as your Te_fwd; if you prefer recovery, swap here)
        Tr = Taw_core[i]
    
        C_f   = m_f_tot * max(cp_c, 1e-6)                   # film capacity rate
        C_e   = m_e_tot * Km * max(cp_g_array[i], 1e-6)     # external (weighted) capacity rate
        denom = max(C_f + C_e, 1e-9)
    
        dTe[j]        = (Tr - Taw_fc_g[j]) * (C_e / denom)
        Taw_fc_g[j+1] = Taw_fc_g[j] + dTe[j]
    
        
    #-------------------------------------[REDOING BARTZ WITH FILM COOLING]--------------------------------------------
    
    #Initialise reversed arrays for film cooling thermals
    Twg_fc_rev        = np.zeros_like(Twg_fwd)
    Twc_fc_rev        = np.zeros_like(Twg_fwd)
    Tc_fc_rev         = np.zeros_like(Twg_fwd)
    Pc_fc_rev         = np.zeros_like(Twg_fwd)
    qg_fc_rev         = np.zeros_like(Twg_fwd)
    Tc_fc_rev[0]      = 300.0
    
    #Assign new h for liquid region and keep old h for gaseous region:
    h_fc_array        = np.concatenate((h_corr_array[:burnout_idx], alphaT_fwd[burnout_idx:]))
    h_fc_array_rev    = flip_full(h_fc_array)
    burnout_idx_rev   = len(h_fc_array_rev) - burnout_idx 
    
    #Assign new Taw for gaseous region and keep old Taw for liquid region:
    Taw_fc_array = np.concatenate((Taw_core[:burnout_idx], Taw_fc_g))
    Taw_fc_array_rev    = flip_full(Taw_fc_array)
    
    for i in range(len(Twg_fc_rev)-1):
        # --- Segment midpoint geometry (used everywhere below) ---
        R_mid_m   = 0.5 * (rev['r'][i] + rev['r'][i+1]) * 1e-3   # m
        A_mid     = math.pi * R_mid_m**2                         # m^2
        x_mid_mm  = 0.5 * (rev['x'][i] + rev['x'][i+1])          # mm
    
        # Segment lengths
        dr = abs(rev['r'][i+1] - rev['r'][i]) * 1e-3             # m
        dx = abs(rev['x'][i+1] - rev['x'][i]) * 1e-3             # m
        seg_len = math.hypot(dx, dr)
    
        # --- Coolant hydraulics on this segment ---
        mass_flow_rate = fuel_mdot / n
        Dh_i  = rev['Dh'][i]
        Aflow = channel_height * rev['w'][i]
    
        # pressure reference
        Press_ref = float(feed_press) if i == 0 else float(regen_pressures[i-1])
        Tc_loc    = float(Tc_fc_rev[i]) 
    
        # 1) provisional pressure drop then one light iterate
        fuel_ref = Fluid(FluidsList.Ethanol).with_state(Input.pressure(Press_ref), Input.temperature(Tc_loc - 273.15))
        fuel_ref = fuel_phase(Tc_loc, Press_ref, fuel_ref)
        rho_ref  = fuel_ref.density
        mu_f_ref = fuel_ref.dynamic_viscosity
        u1       = mass_flow_rate/(rho_ref*Aflow)
        Re_c     = rho_ref * u1 * Dh_i / mu_f_ref
        # Darcy with roughness (k_s ~ eps)
        fD = (-1.8*math.log10(rev['eps'][i]/(3.7*Dh_i) + (6.9/Re_c)**1.1))**-2
        dyn_head   = 0.5*rho_ref*u1**2
        dP_segment = fD * seg_len/Dh_i * dyn_head
        if i == 0 or i == (Nseg-1):
            dP_segment += 0.8*dyn_head
        regen_press = float(Press_ref - dP_segment)     # Pa
        regen_press = max(regen_press, 1e5)             # guard: avoid ≤ 0 Pa
        regen_pressures[i] = regen_press
    
        # refine once
        if abs(regen_press - Press_ref)/Press_ref > 5e-2:
            Press_ref = float(regen_press)
            fuel_ref = Fluid(FluidsList.Ethanol).with_state(Input.pressure(Press_ref), Input.temperature(Tc_loc - 273.15))
            fuel_ref = fuel_phase(Tc_loc, Press_ref, fuel_ref)
            rho_ref  = fuel_ref.density
            mu_f_ref = fuel_ref.dynamic_viscosity
            u1       = mass_flow_rate/(rho_ref*Aflow)
            Re_c     = rho_ref*u1*Dh_i/mu_f_ref
            fD       = (-1.8*math.log10(rev['eps'][i]/(3.7*Dh_i) + (6.9/Re_c)**1.1))**-2
            dyn_head = 0.5*rho_ref*u1**2
            dP_segment = fD * seg_len/Dh_i * dyn_head
            if i == 0 or i == (Nseg-1):
                dP_segment += 0.8*dyn_head
            regen_press = Press_ref - dP_segment
    
        regen_pressures[i] = regen_press
    
        # coolant props at regen_press
        fuel_st = Fluid(FluidsList.Ethanol)
        fuel_st = fuel_phase(Tc_loc, regen_press, fuel_st)
        rho     = fuel_st.density
        mu_f    = fuel_st.dynamic_viscosity
        lam_c   = fuel_st.conductivity
        cp_c    = fuel_st.specific_heat
        Pr_c    = cp_c * mu_f / lam_c
    
        # --- Mach number from area ratio at segment MIDPOINT ---
        if (i + 0.5) > throat_idx_rev:
            # upstream of throat (subsonic)
            M = ispObj.get_Chamber_MachNumber(Pc=Pc_psia, MR=OF, fac_CR=A_mid/At)
        elif (i + 0.5) < throat_idx_rev:
            # downstream (supersonic)
            M = ispObj.get_MachNumber(Pc=Pc_psia, MR=OF, eps=A_mid/At,
                                      frozen=0, frozenAtThroat=0)
        else:
            M = 1.0
        Mach_array[i] = M
        
        # --- Coolant-side HTC (Dittus-Boelter) ---
        u1   = mass_flow_rate / (rho * Aflow)
        Re_c = rho * u1 * Dh_i / mu_f
        Nu   = Nusselt_Number(Re_c, Pr_c, fD)
        alpha_c = Nu * lam_c / Dh_i
    
        # iterative wall solve (with cap + under-relax)
        Taw     = Taw_fc_array_rev[i]
        Twg_0   = Taw - 50.0
        tol     = 1e-4
        max_it  = 200
        
        # guard values
        alpha_c_eff = max(alpha_c, 1e-9)
        lambda_w_min = 1.0
        tw_eff = max(tw, 1e-4)
        base2 = max(1.0 + 0.5*(gamma - 1.0)*M*M, 1e-9)
        
        if isinstance(conductivity, np.ndarray):
            lambda_w = np.interp((Twg_0+Twc)/2.0, conductivity_temps, conductivity)
        else:
            lambda_w = conductivity
        lambda_w = max(lambda_w, lambda_w_min)
    
        h   = h_fc_array_rev[i] 
        qg_i  = (Taw_fc_array_rev[i] - Tc_loc)/(1/h + 1/alpha_c_eff + tw/lambda_w)
        Twc = qg_i / alpha_c_eff + Tc_loc   
        Twg_1 = Taw_fc_array_rev[i] - qg_i/h
        
        # store segment results (still reversed order)
        qg_fc_rev[i]       = qg_i
        Twg_fc_rev[i]      = Twg_1
        Twc_fc_rev[i]      = Twc
    
        Ahot_seg = 2.0 * math.pi * R_mid_m * seg_len          # m^2
        Q_seg    = qg_i * Ahot_seg                               # W (J/s)
        Tc_fc_rev[i+1] = Tc_fc_rev[i] + Q_seg / (fuel_mdot * cp_c)
        
    Tc_max = np.max(Tc_fc_rev)
    # After the for-loop that fills qg_fc_rev, Twg_fc_rev, Twc_fc_rev
    Twg_fc_rev[-1] = Twg_fc_rev[-2]
    Twc_fc_rev[-1] = Twc_fc_rev[-2]
    qg_fc_rev[-1]  = qg_fc_rev[-2]
    
    iter_count+=1

#---------------------------[FILTER OUT SPIKES DUE TO NANS/ZEROS]----------------------
# Tc_fc_array    = flip_full(median_filter(Tc_fc_rev,3, mode='reflect'))
# Twg_fc_array   = flip_full(median_filter(Twg_fc_rev, 3, mode='reflect'))
# Twc_fc_array   = flip_full(median_filter(Twc_fc_rev, 3, mode='reflect'))
# qg_fc_array    = flip_full(median_filter(qg_fc_rev, 3, mode='reflect'))
Tc_fc_array    = flip_full(Tc_fc_rev)
Twg_fc_array   = flip_full(Twg_fc_rev)
Twc_fc_array   = flip_full(Twc_fc_rev)
qg_fc_array    = flip_full(qg_fc_rev)
#%%==========================[PLOTTING]=========================

# x-axis (segment midpoints) + throat
x = x_seg_mm                              # length = len(x_full) - 1
x_throat = x_nodes_mm[throat_node_fwd]

# Forward (gas-flow) arrays
Twg   = np.asarray(Twg_fc_array).squeeze()
Twc   = np.asarray(Twc_fc_array).squeeze()
qg    = np.asarray(qg_fc_array).squeeze()
aT    = np.asarray(alphaT_fwd).squeeze()
Mach  = np.asarray(Mach_fwd).squeeze()
Tc_s  = np.asarray(Tc_fc_array).squeeze()
Pcool = np.asarray(Pcool_fwd).squeeze()

# Safety trim to the same length
N = x.size
def trim(y): return y[:N]
Twg, Twc, qg, aT, Mach, Tc_s, Pcool = map(trim, [Twg, Twc, qg, aT, Mach, Tc_s, Pcool])


# ======= Combined Temps (+Tsat) & Heat Flux with Cleaner Colours =======


# Colors (RGB -> matplotlib normalized 0–1)
RED    = (1.0, 0.0, 0.0)       # (255,0,0)
GREEN  = (0.0, 1.0, 0.0)       # (0,255,0)
TEAL   = (0.0, 0.7, 0.7)        # teal
PINK   = (1.0, 0.0, 1.0)       # (255,0,255)
BLUE   = (0.0, 0.0, 1.0)       # (0,0,255)
GREY   = (0.4, 0.4, 0.4)
ORANGE = (1.0, 0.5, 0.0)

# Boiling curve (pressure-dependent if valid; else 1 atm)
tsat_label = r'Ethanol $T_\mathrm{sat}(P)$'
if np.all(np.isfinite(Pcool)) and Pcool.size == x.size:
    Tsat_curve = ethanol_Tsat_from_P(Pcool)
else:
    Tsat_curve = np.full_like(x, 351.52)  # K
    tsat_label = r'Ethanol $T_\mathrm{sat}$ @1 atm'

if Complete_Thermal_Analysis == True:
    fig, ax1 = plt.subplots(figsize=(8.0, 4.8))
    ax2 = ax1.twinx()
    # --- Left axis (Temps + Tsat) ---
    l_wg,  = ax1.plot(x, Twg,  label=r'$T_{w,g}$',  color=RED,   linewidth=1.6, alpha=0.95)
    l_wc,  = ax1.plot(x, Twc,  label=r'$T_{w,c}$',  color=TEAL, linewidth=1.4, alpha=0.9,  linestyle='--')
    l_tc,  = ax1.plot(x, Tc_s, label=r'$T_c$',      color=BLUE,  linewidth=1.4, alpha=0.9,  linestyle='-.')
    l_sat, = ax1.plot(x, Tsat_curve, label=tsat_label, color=PINK, linewidth=1.4, alpha=0.85, linestyle=':')
    
    # --- Right axis (Heat flux) ---
    r_qg,  = ax2.plot(x, qg,   label=r'$q_g$',       color=ORANGE, linewidth=1.6, alpha=0.8)
    
    # --- Nozzle contour overlay (scaled into temp axis range) ---
    try:
        Tmin = np.nanmin([Twg.min(), Twc.min(), Tc_s.min(), Tsat_curve.min()])
        Tmax = np.nanmax([Twg.max(), Twc.max(), Tc_s.max(), Tsat_curve.max()])
        dr = (r_seg_mm - np.nanmin(r_seg_mm)) / max(1e-12, (np.nanmax(r_seg_mm) - np.nanmin(r_seg_mm)))
        band = 0.25*(Tmax - Tmin)
        baseline = Tmin - 0.15*(Tmax - Tmin)
        contour_scaled = baseline + band * dr
        l_cnt, = ax1.plot(x, contour_scaled, color=GREY, linewidth=1.0, alpha=0.5,
                          linestyle='-', label='Nozzle contour (scaled)')
    except Exception:
        l_cnt = None
    
    # Throat marker
    ax1.axvline(x=x_throat, color='k', linestyle=':', linewidth=1.0, label='Throat')
    
    # Labels, title, grid
    ax1.set_xlabel('Axial position [mm]')
    ax1.set_ylabel('Temperature [K]')
    ax2.set_ylabel(r'Heat flux [W/m$^2$]')
    ax1.set_title('Temperatures + Boiling Point (left) & Heat Flux (right)')
    ax1.grid(True, alpha=0.25)
    
    # Combined legend
    handles = [l_wg, l_wc, l_tc, l_sat, r_qg]
    if l_cnt is not None: handles.append(l_cnt)
    labels = [h.get_label() for h in handles]
    ax1.legend(handles, labels, loc='upper left', frameon=True)
    
    plt.tight_layout()
    plt.show()


# ===== Diagnostic 3×3 with Distinct Colours =====
Te = T0 * (1.0 + 0.5*(gamma-1.0)*Mach**2 * (Pr_g**(1/3))) / (1.0 + 0.5*(gamma-1.0)*Mach**2)
dT = Te - Twg
sigma = (0.5*(Twg/T0)*(1 + 0.5*(gamma-1)*Mach**2) + 0.5)**(-0.68) * (1 + 0.5*(gamma-1)*Mach**2)**(-0.12)
At_over_A_09 = (At / (np.pi*(r_seg_mm*1e-3)**2))**0.9
Dt_over_R_01 = ((2.0*Rt_SI) / (r_seg_mm*1e-3))**0.1
At_over_A_09 = trim(At_over_A_09); Dt_over_R_01 = trim(Dt_over_R_01)

# Define a palette of 9 distinct colours
colors = [
    (1.0, 0.0, 0.0),    # red
    (0.0, 0.6, 0.0),    # green
    (0.0, 0.0, 1.0),    # blue
    (1.0, 0.0, 1.0),    # magenta
    (1.0, 0.5, 0.0),    # orange
    (0.0, 0.7, 0.7),    # teal
    (0.6, 0.0, 0.6),    # purple
    (0.3, 0.3, 0.3),    # grey
    (0.6, 0.4, 0.0)     # brownish gold
]

if Thermal_Diagnostic_3x3 == True:
    fig, axs = plt.subplots(3, 3, figsize=(11, 8), sharex=True)
    (ax1, ax2, ax3), (ax4, ax5, ax6), (ax7, ax8, ax9) = axs
    
    ax1.plot(x, qg, color=colors[0]);      ax1.set_title(r'$q_g$  [W/m$^2$]')
    ax2.plot(x, aT, color=colors[1]);      ax2.set_title(r'$\alpha_T$  [W/m$^2$K]')
    ax3.plot(x, Mach, color=colors[2]);    ax3.set_title('Mach')
    ax4.plot(x, Te, color=colors[3]);      ax4.set_title(r'$T_e$  [K]')
    ax5.plot(x, Twg, color=colors[4]);     ax5.set_title(r'$T_{w,g}$  [K]')
    ax6.plot(x, dT, color=colors[5]);      ax6.set_title(r'$\Delta T$  [K]')
    ax7.plot(x, sigma, color=colors[6]);   ax7.set_title(r'$\sigma$  [–]')
    ax8.plot(x, At_over_A_09, color=colors[7]); ax8.set_title(r'$(A_t/A)^{0.9}$')
    ax9.plot(x, Dt_over_R_01, color=colors[8]); ax9.set_title(r'$(D_t/R)^{0.1}$')
    
    for ax in axs.flat:
        ax.grid(True, alpha=0.3)
        ax.axvline(x=x_throat, color='k', linestyle=':', linewidth=1.0)
    
    axs[-1,0].set_xlabel('Axial position [mm]')
    axs[-1,1].set_xlabel('Axial position [mm]')
    axs[-1,2].set_xlabel('Axial position [mm]')
    
    plt.tight_layout(rect=[0,0,1,0.96])
    plt.show()


if Film_Cooling_vs_No_FC== True: 
    # ===== Film Cooling Comparison Graphs =====
    def get_color(name, idx):
        if name in globals():
            return globals()[name]
        if 'colors' in globals() and len(colors) > idx:
            return colors[idx]  # your 9-color palette
        return None  # let mpl cycle
    
    c_Twg_no   = get_color('RED',    0)
    c_Twg_film = get_color('BLUE',   2)
    c_Twc_no   = get_color('GREY',   7)
    c_Twc_film = get_color('TEAL',   5)
    c_Tc_no    = get_color('GREEN',  1)
    c_Tc_film  = get_color('PINK',   3)
    c_qg_no    = get_color('ORANGE', 4)
    c_qg_film  = get_color('PURPLE', 6) or (0.6, 0.0, 0.6)
    
    # ---- optional: show qg in MW/m² (set scale=1 for W/m²) ----
    q_scale = 1e-6
    q_label = 'qg [MW/m²]' if q_scale == 1e-6 else 'qg [W/m²]'
    
    fig, axs = plt.subplots(2, 2, figsize=(12, 8), sharex=True)
    
    # (1) Twg: film vs no-film
    axs[0, 0].plot(x_seg_mm, Twg_fwd,       label='Twg (no film)',
                   color=c_Twg_no,   linewidth=1.8)
    axs[0, 0].plot(x_seg_mm, Twg_fc_array,  label='Twg (film)',
                   color=c_Twg_film, linewidth=1.8, linestyle='--')
    axs[0, 0].set_ylabel('Temperature [K]')
    axs[0, 0].set_title('Gas-side wall temperature (Twg)')
    axs[0, 0].grid(True, alpha=0.3)
    axs[0, 0].legend()
    
    # (2) Twc: film vs no-film
    axs[0, 1].plot(x_seg_mm, Twc_fwd,       label='Twc (no film)',
                   color=c_Twc_no,   linewidth=1.8)
    axs[0, 1].plot(x_seg_mm, Twc_fc_array,  label='Twc (film)',
                   color=c_Twc_film, linewidth=1.8, linestyle='--')
    axs[0, 1].set_ylabel('Temperature [K]')
    axs[0, 1].set_title('Coolant-side wall temperature (Twc)')
    axs[0, 1].grid(True, alpha=0.3)
    axs[0, 1].legend()
    
    # (3) Tc: film vs no-film
    axs[1, 0].plot(x_seg_mm, Tc_fwd_nodes[:-1], label='Tc (no film)',
                   color=c_Tc_no,   linewidth=1.8)
    axs[1, 0].plot(x_seg_mm, Tc_fc_array,       label='Tc (film)',
                   color=c_Tc_film, linewidth=1.8, linestyle='--')
    axs[1, 0].set_ylabel('Temperature [K]')
    axs[1, 0].set_title('Coolant bulk temperature (Tc)')
    axs[1, 0].set_xlabel('Axial position x [mm]')
    axs[1, 0].grid(True, alpha=0.3)
    axs[1, 0].legend()
    
    # (4) qg: film vs no-film
    axs[1, 1].plot(x_seg_mm, qg_fwd * q_scale,      label='qg (no film)',
                   color=c_qg_no,   linewidth=1.8)
    axs[1, 1].plot(x_seg_mm, qg_fc_array * q_scale, label='qg (film)',
                   color=c_qg_film, linewidth=1.8, linestyle='--')
    axs[1, 1].set_ylabel(q_label)
    axs[1, 1].set_title('Hot-gas heat flux')
    axs[1, 1].set_xlabel('Axial position x [mm]')
    axs[1, 1].grid(True, alpha=0.3)
    axs[1, 1].legend()
    
    # throat marker if you have x_throat defined
    try:
        for ax in axs.flat:
            ax.axvline(x=x_throat, color='k', linestyle=':', linewidth=1.0)
    except Exception:
        pass
    
    plt.tight_layout()
    plt.show()





#%%==========================[STRESS CALCULATIONS AND PLOTTING]=====================================



contour   = r_seg_mm * 1e-3
ax_pos    = x_seg_mm * 1e-3
fuel_temp = Tc_fc_rev
regen_press = flip_full(regen_pressures)

#=========================== Conduct Temperature and Pressure Calculations ==============================================
stagnation_pressure = Pc_SI
radii = r_seg_mm * 1e-3
throat_radius = np.min(radii)
area_ratios = (radii/throat_radius)**2
mach_numbers = np.zeros_like(area_ratios)
for i in range(len(area_ratios)):
    gamma = 1.1674
    area_ratio = area_ratios[i]
    if i==0:
        machfunc = lambda M, area_ratio = area_ratio: (1/area_ratio)*(1 + (gamma-1)*M**2/2)**((gamma+1)/(2*(gamma-1))) - M * (1 + (gamma - 1)/2)**((gamma+1)/(2*(gamma-1)))
        sol = sp.optimize.root_scalar(machfunc, method = 'brentq',bracket=[0,1])
        mach_numbers[i] = sol.root if sol.converged else np.nan
    
    elif radii[i] <= radii[i-1]:
        machfunc = lambda M, area_ratio = area_ratio: (1/area_ratio)*(1 + (gamma-1)*M**2/2)**((gamma+1)/(2*(gamma-1))) - M * (1 + (gamma - 1)/2)**((gamma+1)/(2*(gamma-1)))
        sol = sp.optimize.root_scalar(machfunc, method = 'brentq',bracket=[0,1])
        mach_numbers[i] = sol.root if sol.converged else np.nan
    
    elif radii[i] >= radii[i-1]:
        machfunc = lambda M, area_ratio = area_ratio: (1/area_ratio)*(1 + (gamma-1)*M**2/2)**((gamma+1)/(2*(gamma-1))) - M * (1 + (gamma - 1)/2)**((gamma+1)/(2*(gamma-1)))
        sol = sp.optimize.root_scalar(machfunc, method = 'brentq',bracket=[1.00001,20])
        mach_numbers[i] = sol.root if sol.converged else np.nan

stagnation_pressure = stagnation_pressure*np.ones_like(mach_numbers)
pressures = stagnation_pressure*(1+(gamma-1)/2 * mach_numbers**2)**((gamma-1)/gamma)
pressures = np.divide(stagnation_pressure, (1+(gamma-1)*mach_numbers**2/2)**(gamma/(gamma-1)))

del area_ratio, area_ratios, i, sol, stagnation_pressure

#=========================== Conduct Stress Calculations =================================================================
longitudinal_thermal_stress = np.zeros_like(pressures)
avg_innerwall_temp = (Twg_fc_array + Twc_fc_array)/2
E = np.interp(avg_innerwall_temp, modulus_temps, modulus)
yield_strength = np.interp(avg_innerwall_temp, yield_temps, yield_stress)
dT = (Twg_fc_array - Twc_fc_array)

channel_dP = regen_press - pressures
if isinstance(modulus, np.ndarray):
    E = np.interp(avg_innerwall_temp, modulus_temps, modulus)
else:
    E = modulus
if isinstance(yield_stress, np.ndarray):
    yield_strength = np.interp(avg_innerwall_temp, yield_temps, yield_stress)
else:   
    yield_strength = yield_stress
if isinstance(cte, np.ndarray):
    coeff_thermal_expansion = np.interp(avg_innerwall_temp, cte_temps, cte)
else:
    coeff_thermal_expansion = cte

if isinstance(conductivity, np.ndarray):
    thermal_conductivity = np.interp(avg_innerwall_temp, conductivity_temps, conductivity)
else:
    thermal_conductivity = conductivity
    

longitudinal_thermal_stress = E*coeff_thermal_expansion*dT
tangential_thermal_stress = (E*coeff_thermal_expansion*qg_fc_array*tw)/(2*(1-v)*thermal_conductivity)
tangential_pressure_stress = channel_dP*(channel_width[:-1]/tw)**2 * 0.5
crit_longitudinal_buckling_stress = E*tw/(np.sqrt(3*(1-v**2))*(radii))
tot_tangential_stress = tangential_pressure_stress + tangential_thermal_stress
von_mises_stress = np.sqrt(tot_tangential_stress**2 + longitudinal_thermal_stress**2  - tot_tangential_stress*longitudinal_thermal_stress)
yield_sf = yield_strength/von_mises_stress
# ============================ PLOTTING (FAST, NO-LaTeX) =============================== Make single plotting func
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

# Hard-disable any LaTeX usage (must be before plotting)
mpl.rcParams.update({
    "text.usetex": False,
    "text.latex.preamble": "",
    "font.family": "serif",   # pick any
})

# -------- Helpers --------
def setup_3d_subplot(fig, position, title, xlabel='X (mm)', ylabel='Y (mm)', zlabel='Axial Position (mm)'):
    ax = fig.add_subplot(position, projection='3d')
    ax.set_xlabel(xlabel); ax.set_ylabel(ylabel); ax.set_zlabel(zlabel)
    ax.set_title(title)
    return ax

def set_equal_axes(ax, X, Y, Z):
    max_range = np.array([X.max()-X.min(), Y.max()-Y.min(), Z.max()-Z.min()]).max() / 2.0
    mid_x = (X.max() + X.min()) * 0.5
    mid_y = (Y.max() + Y.min()) * 0.5
    mid_z = (Z.max() + Z.min()) * 0.5
    eps = 1e-9 if max_range == 0 else 0
    ax.set_xlim(mid_x - max_range - eps, mid_x + max_range + eps)
    ax.set_ylim(mid_y - max_range - eps, mid_y + max_range + eps)
    ax.set_zlim(mid_z - max_range - eps, mid_z + max_range + eps)

def rotate_and_plot_surfaces_fast(ax, X, Y, Z, facecolors, num_channels_to_plot):
    phis = np.linspace(0, 2*np.pi, num_channels_to_plot, endpoint=False)
    c = np.cos(phis); s = np.sin(phis)
    for ci, si in zip(c, s):
        Xr = X*ci - Y*si
        Yr = X*si + Y*ci
        ax.plot_surface(Xr, Yr, Z, facecolors=facecolors, rstride=1, cstride=1,
                        linewidth=0, antialiased=False, shade=False, alpha=1.0)

def annotate_extreme_point_fast(ax, X, Y, Z, target_array, label_coords=None,
                                text_prefix="Value", is_max=True):
    if np.all(np.isnan(target_array)):  # nothing to show
        return
    idx = np.unravel_index((np.nanargmax if is_max else np.nanargmin)(target_array), target_array.shape)
    x0, y0, z0 = float(X[idx]), float(Y[idx]), float(Z[idx])

    if label_coords is None:
        r_plot = float(np.hypot(X, Y).max())
        lx = 1.15 * r_plot
        ly = -0.60 * r_plot
        lz = float(Z.min() + 0.35 * (Z.max() - Z.min()))
        label_coords = (lx, ly, lz)

    lx, ly, lz = label_coords
    ang_point = np.arctan2(y0, x0)
    ang_label = np.arctan2(ly, lx)
    phi = ang_label - ang_point
    c, s = np.cos(phi), np.sin(phi)
    xt = x0*c - y0*s
    yt = x0*s + y0*c

    val = float(target_array[idx])
    ax.text(lx, ly, lz, f"{text_prefix}: {val:.2f}", color='black',
            fontsize=12, fontweight='bold')

if SF_and_Temps_3D == True:
    # -------- Common mesh (make shapes consistent and light) --------
    theta_min = 0.0
    theta_max = np.deg2rad(3.8)
    n_theta   = 30
    thetas    = np.linspace(theta_min, theta_max, n_theta)
    
    ax_pos = np.asarray(ax_pos)
    radii  = np.asarray(radii)
    Nr = radii.size; Nt = n_theta
    assert ax_pos.size == Nr, "ax_pos must have same length as radii"
    
    Theta, Radius = np.meshgrid(thetas, radii)      # (Nr, Nt)
    X = Radius * np.cos(Theta)
    Y = Radius * np.sin(Theta)
    Z = np.tile(ax_pos[:, None], (1, Nt))
    
    # Downsample for rendering speed (tune as needed)
    DS_R = max(1, Nr // 220)     # keep ~≤220 radial samples
    DS_T = max(1, Nt // 48)      # keep ≤48 theta samples
    Xs = X[::DS_R, ::DS_T]; Ys = Y[::DS_R, ::DS_T]; Zs = Z[::DS_R, ::DS_T]
    
    # -------- Data fields (ensure 1D length Nr, then tile and downsample) --------
    yield_sf = np.asarray(yield_sf);           assert yield_sf.size == Nr
    Yield_SF = np.tile(yield_sf[:, None], (1, Nt))
    Yield_SF_s = Yield_SF[::DS_R, ::DS_T]
    Yield_SF_capped_s = np.clip(Yield_SF_s, 0, 12)
    
    firewall_temp = np.asarray(Twg_fc_array);  assert firewall_temp.size == Nr
    Firewall_Temp = np.tile(firewall_temp[:, None], (1, Nt))
    Firewall_Temp_s = Firewall_Temp[::DS_R, ::DS_T]
    
    # Colormaps on downsampled grids
    cmap_sf  = plt.get_cmap('jet_r')
    norm_sf  = plt.Normalize(vmin=0, vmax=12)
    faces_sf = cmap_sf(norm_sf(Yield_SF_capped_s))
    
    vmin_t = float(np.nanmin(Firewall_Temp_s))
    vmax_t = float(np.nanmax(Firewall_Temp_s))
    cmap_t  = plt.get_cmap('hot_r')
    norm_t  = plt.Normalize(vmin=vmin_t, vmax=vmax_t)
    faces_t = cmap_t(norm_t(Firewall_Temp_s))
    
    # How many channel copies to draw (visual, not physical)
    n_channels = int(n) if "n" in globals() or "n" in locals() else 8
    # num_channels_to_plot = max(4, min(n_channels, 12))   # 4–12 looks good & fast
    num_channels_to_plot = n
    # -------- Figure --------
    fig = plt.figure(figsize=(16, 8))
    
    # Plot 1: Yield Safety Factor
    ax1 = setup_3d_subplot(fig, 121, "Yield Safety Factor Contours")
    fig.colorbar(plt.cm.ScalarMappable(cmap=cmap_sf, norm=norm_sf),
                 ax=ax1, shrink=0.6, label='Yield Safety Factor (capped at 12)')
    set_equal_axes(ax1, Xs, Ys, Zs)
    ax1.invert_zaxis()     # flip vertical orientation
    rotate_and_plot_surfaces_fast(ax1, Xs, Ys, Zs, faces_sf, num_channels_to_plot)
    annotate_extreme_point_fast(ax1, Xs, Ys, Zs, Yield_SF_s, text_prefix="Minimum SF", is_max=False)
    ax1.view_init(elev=10, azim=210)
    
    # Plot 2: Firewall Temperature
    ax2 = setup_3d_subplot(fig, 122, "Firewall Temperature Contours")
    fig.colorbar(plt.cm.ScalarMappable(cmap=cmap_t, norm=norm_t),
                 ax=ax2, shrink=0.6, label='Firewall Temperature (K)')
    set_equal_axes(ax2, Xs, Ys, Zs)
    ax2.invert_zaxis()
    
    rotate_and_plot_surfaces_fast(ax2, Xs, Ys, Zs, faces_t, num_channels_to_plot)
    annotate_extreme_point_fast(ax2, Xs, Ys, Zs, Firewall_Temp_s, text_prefix="Max Temp. (K)", is_max=True)
    ax2.view_init(elev=10, azim=210)
    
    plt.tight_layout()
    plt.show()


if Stress_Plot == True:
    # -------- Other (2D) plots --------
    plt.figure()
    plt.plot(ax_pos, tangential_pressure_stress, label='Tangential Pressure Stress')
    plt.plot(ax_pos, tangential_thermal_stress,  label='Tangential Thermal Stress')
    plt.plot(ax_pos, radii * 0.5e9,linestyle='--', label='Contour')
    plt.legend()
    plt.xlabel("Axial Position (mm)")
    plt.ylabel("Value (units)")
    plt.title("Stress & Contour")
    plt.grid(alpha=0.3)
    plt.show()

