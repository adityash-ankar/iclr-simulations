import numpy as np
def run_rocket_cea(ox,fuel,OF,Chamber_Pressure,eta_cstar,eta_Cf,Thrust_req):
    """
    Estimate rocket engine performance and throat sizing using RocketCEA.
    
    Parameters
    ----------
    ox : str        Oxidizer name (RocketCEA format, e.g. "LOX").
    fuel : str      Fuel name (e.g. "RP-1").
    OF : float      Oxidizer-to-fuel ratio by mass.
    Chamber_Pressure : float
        Chamber pressure in bar.
    eta_cstar : float
        c* efficiency (0–1).
    eta_Cf : float
        Thrust coefficient efficiency (0–1).
    Thrust_req : float
        Required sea-level thrust in N.
    
    Returns
    -------
    ISP_vac_ideal : float   Ideal vacuum Isp (s).
    ISP_SL_act    : float   Sea-level Isp with efficiencies (s).
    Rt_SI         : float   Throat radius (m).
    mdot_act      : float   Mass flow rate (kg/s).
    ISP_SL_act    : float   (duplicate of above).
    F_check_SL    : float   Calculated SL thrust (N).
    """
    from rocketcea.cea_obj import CEA_Obj
    import math
    ispObj = CEA_Obj(oxName=ox, fuelName=fuel)
    
    Pc_SI   = Chamber_Pressure * 1e5       # Pa
    Pc_psia = Chamber_Pressure * 14.5038   # psia
    g0      = 9.80665
    
    # Area ratio ~ Pe = 1 atm
    Area_Ratio = ispObj.get_eps_at_PcOvPe(Pc=Pc_psia, MR=OF,
                                          PcOvPe=Chamber_Pressure/1.013,
                                          frozen=0, frozenAtThroat=0)
    
    # Ideal Isp & c*
    ISP_vac_ideal = ispObj.get_Isp(Pc=Pc_psia, MR=OF, eps=Area_Ratio, frozen=0, frozenAtThroat=0)     # s
    cstar_ideal   = ispObj.get_Cstar(Pc=Pc_psia, MR=OF) / 3.28                                        # m/s
    
    # Ideal Cf at SL
    Cf_list_SL   = ispObj.get_PambCf(Pamb=14.7, Pc=Pc_psia, MR=OF, eps=Area_Ratio)
    Cf_SL_ideal  = float(Cf_list_SL[0])
    
    # Apply efficiencies
    cstar_act = eta_cstar * cstar_ideal
    Cf_SL_act = eta_Cf    * Cf_SL_ideal
    
    # Throat area from thrust target (SL)
    At_SI = Thrust_req / (Cf_SL_act * Pc_SI)   # m²
    Rt_SI = math.sqrt(At_SI / math.pi)         # m
    
    # Mass flow & check
    mdot_act   = Pc_SI * At_SI / cstar_act
    ISP_SL_act = Cf_SL_act * cstar_act / g0
    F_check_SL = Cf_SL_act * Pc_SI * At_SI

    return(ISP_vac_ideal,ISP_SL_act,Rt_SI, mdot_act, ISP_SL_act, F_check_SL, Area_Ratio)
def initialise_thermal_arrays(Nseg):
    """
    Allocate zero-filled per-segment arrays for a 1-D thermal/flow march.

    Parameters
    ----------
    Nseg : int
        Number of axial segments.

    Returns
    -------
    qg_array : (Nseg,) float
        Gas-side heat flux [W/m²].
    alpha_t_array : (Nseg,) float
        Gas-side convection coefficient h [W/m²·K].
    twg_array : (Nseg,) float
        Inner wall temperature (gas side) Tw,g [K].
    twc_array : (Nseg,) float
        Outer wall temperature (coolant side) Tw,c [K].
    te_array : (Nseg,) float
        Gas static temperature [K].
    tc_array : (Nseg+1,) float
        Coolant bulk temperature nodes [K]; tc_array[0] = 300 K.
    Mach_array : (Nseg,) float
        Local Mach number [–].
    regen_pressures : (Nseg,) float
        Coolant/channel pressure [Pa].
    Nu_array : (Nseg,) float
        Nusselt number [–].
    Re_array : (Nseg,) float
        Reynolds number [–].
    """
    import numpy as np
    qg_array       = np.zeros(Nseg, dtype=float)
    alpha_t_array  = np.zeros(Nseg, dtype=float)
    twg_array      = np.zeros(Nseg, dtype=float)
    twc_array      = np.zeros(Nseg, dtype=float)
    te_array       = np.zeros(Nseg, dtype=float)
    Mach_array     = np.zeros(Nseg, dtype=float)
    regen_pressures= np.zeros(Nseg, dtype=float)
    Nu_array       = np.zeros(Nseg, dtype=float)
    Re_array       = np.zeros(Nseg, dtype=float)
    
    tc_array       = np.zeros(Nseg+1, dtype=float)
    tc_array[0]    = 300.0  # K
    
    
    return(qg_array,alpha_t_array, twg_array, twc_array, te_array, tc_array, Mach_array, regen_pressures, Nu_array, Re_array)
class GasProps:
    """RocketCEA wrapper: chamber props at (Pc [bar], OF) → SI.
    Sets: T0 [K], cp [J/kg·K], mu [Pa·s], k [W/m·K], Pr [–], c_star [m/s].
    (Conv: °R→K 5/9, ft/s→m/s 0.3048, BTU/lbm·°R→J/kg·K 4186.8, mP→Pa·s 1e-4, mcal/cm·K·s→W/m·K 0.4184)
    """
    def __init__(self, ox, fuel, Pc, OF):
        self.Pc = Pc
        self.ox = ox
        self.fuel = fuel
        self.OF = OF
        """Init with ox, fuel, Pc [bar], OF; cache chamber properties."""
        _degR_to_K         = 5.0/9.0
        _ftps_to_mps       = 0.3048
        _BTUlbmR_to_JkgK   = 4186.8
        _millipoise_to_Pas = 1e-4
        _mcalcmKs_to_WmK   = 0.4184

        from rocketcea.cea_obj import CEA_Obj
        self.ispObj = CEA_Obj(oxName=ox, fuelName=fuel)

        Pc_psia = Pc * 14.5038
        self.T0 = self.ispObj.get_Tcomb(Pc=Pc_psia, MR=OF) * _degR_to_K

        cp, mu, k_mcalcmKs, Pr = self.ispObj.get_Chamber_Transport(Pc=Pc_psia, MR=OF, frozen=0)
        self.cp  = cp * _BTUlbmR_to_JkgK
        self.mu  = mu * _millipoise_to_Pas
        self.thermal_conductivity = k_mcalcmKs * _mcalcmKs_to_WmK
        self.Pr  = Pr

        self.c_star = self.ispObj.get_Cstar(Pc=Pc_psia, MR=OF) * _ftps_to_mps

    def gamma(self, Area_Ratio):
        """Return γ at Ae/At."""
        Pc_psia = self.Pc * 14.5038
        _, k = self.ispObj.get_Chamber_MolWt_gamma(Pc=Pc_psia, MR=self.OF, eps=Area_Ratio)
        return k

    def molwt(self, Area_Ratio):
        """Return chamber molecular weight."""
        Pc_psia = self.Pc * 14.5038
        mw, _ = self.ispObj.get_Chamber_MolWt_gamma(Pc=Pc_psia, MR=self.OF, eps=Area_Ratio)
        return mw

    def densities(self, Area_Ratio):
        """Return (ρc, ρt, ρe) in kg/m³ at Ae/At."""
        Pc_psia = self.Pc * 14.5038
        _lbft3_to_kgm3 = 16.018463
        dens = np.array(self.ispObj.get_Densities(Pc=Pc_psia, MR=self.OF, eps=Area_Ratio), float) * _lbft3_to_kgm3
        return tuple(dens.tolist())
def fuel_phase(Tc_loc_K, regen_press, fuel_st, *, pressure_in_pa=True):

    """
    Robust ethanol state chooser for PyFluids:
    - Lets EOS decide from (P,T) first.
    - If that fails, picks phase by Tsat(P), then retries.
    - Adds tiny nudges near saturation to avoid singularities.
    - Expects Tc_loc_K in Kelvin. 'regen_press' in Pa if pressure_in_pa=True, else bar.
    Returns: a PyFluids Fluid(FluidsList.Ethanol) at the requested state.
    """
    
    from pyfluids import Fluid, FluidsList, Input, Phases
    from CoolProp.CoolProp import PropsSI
    # Ethanol critical point (CoolProp values)
    _ETH_Tc = 514.0        # K (approx)
    _ETH_Pc = 6.38e6       # Pa (approx)

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
def get_mach_number(Area_Ratio, ox, fuel, Pc, OF, Throat_Downstream):
    import scipy.optimize as opt
    gas_props = GasProps(ox, fuel, Pc, OF)
    gamma = gas_props.gamma(Area_Ratio)

    def f(M):
        return Area_Ratio - (1/M) * ((2/(gamma+1))*(1 + 0.5*(gamma-1)*M**2))**((gamma+1)/(2*(gamma-1)))

    # subsonic root in (1e-6,1), supersonic in (1,20)
    if Throat_Downstream:
        a, b = 1.0001, 20
    else:
        a, b = 1e-6, 1

    return opt.brentq(f, a, b)
        
        
        