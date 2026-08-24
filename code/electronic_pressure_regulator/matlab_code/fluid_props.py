import numpy as np
import scipy.io
from pathlib import Path
from thermo import Chemical
from rocketprops.rocket_prop import get_prop


# -----------------------------------------------------------------------------
# Unit conversions
# -----------------------------------------------------------------------------
PA_PER_BAR = 1.0e5
PA_PER_PSIA = 6894.757293168
PSIA_PER_BAR = PA_PER_BAR / PA_PER_PSIA
BTU_LBM_R_TO_KJ_KG_K = 4.1868
POISE_TO_PA_S = 0.1
BTU_HR_FT_R_TO_W_M_K = 1.730734666

# N2O solver-padding settings.  Simscape Thermal Liquid requires the valid
# pressure region to include atmospheric pressure even when the intended
# operating pressure is much higher.  Cells outside the physical liquid
# region are therefore populated with liquid-side surrogate data.
N2O_SOLVER_PADDING = True
N2O_INTENDED_MIN_PRESSURE_BAR = 20.0


def bar_to_pa(value_bar):
    """Convert bar to Pa. Works with scalars or NumPy arrays."""
    return np.asarray(value_bar, dtype=float) * PA_PER_BAR


def require_finite(value, label):
    """Return a finite float or raise an informative error."""
    if value is None:
        raise RuntimeError(f"{label} returned None")
    value = float(value)
    if not np.isfinite(value):
        raise RuntimeError(f"{label} returned non-finite value: {value}")
    return value


def output_directory():
    """Use the script directory, or the current directory in notebooks/REPLs."""
    if "__file__" in globals():
        return Path(__file__).resolve().parent
    return Path.cwd()


# -----------------------------------------------------------------------------
# Thermodynamic derivative helpers
# -----------------------------------------------------------------------------
def bulk_modulus_from_density(
    rho_func,
    pressure_pa,
    min_pressure_pa=1.0,
    pressure_step_pa=1.0e3,
    relative_step=1.0e-4,
):
    """Calculate isothermal bulk modulus K_T = rho/(drho/dP)_T [Pa].

    ``pressure_step_pa`` sets the minimum finite-difference interval.  A very
    small interval is suitable for smooth EOS correlations, but tabulated/fitted
    correlations (notably RocketProps N2O ``SG_compressed``) should be
    differentiated over a grid-scale interval to avoid interpolation-derivative
    artefacts.
    """
    p = float(pressure_pa)
    dp = max(float(pressure_step_pa), abs(p) * float(relative_step))

    if p - dp > min_pressure_pa:
        rho_minus = require_finite(rho_func(p - dp), "density(P-dP)")
        rho_plus = require_finite(rho_func(p + dp), "density(P+dP)")
        drho_dp = (rho_plus - rho_minus) / (2.0 * dp)
    else:
        rho_0 = require_finite(rho_func(p), "density(P)")
        rho_plus = require_finite(rho_func(p + dp), "density(P+dP)")
        drho_dp = (rho_plus - rho_0) / dp

    rho_0 = require_finite(rho_func(p), "density(P)")
    if drho_dp <= 0.0:
        raise RuntimeError(
            f"Non-positive density pressure derivative at P={p:g} Pa: {drho_dp:g}"
        )
    return rho_0 / drho_dp


def expansion_coefficient_from_density(
    rho_func,
    temperature_k,
    pressure_pa,
    t_min_k=None,
    t_max_k=None,
    temperature_step_k=0.05,
):
    """Calculate alpha = -(1/rho)*(drho/dT)_P [1/K].

    ``temperature_step_k`` may be increased for fitted/tabulated density
    correlations whose very local derivatives are noisy.
    """
    t = float(temperature_k)
    dT = float(temperature_step_k)

    can_minus = t_min_k is None or (t - dT) >= t_min_k
    can_plus = t_max_k is None or (t + dT) <= t_max_k

    if can_minus and can_plus:
        rho_minus = require_finite(rho_func(t - dT, pressure_pa), "density(T-dT)")
        rho_plus = require_finite(rho_func(t + dT, pressure_pa), "density(T+dT)")
        drho_dT = (rho_plus - rho_minus) / (2.0 * dT)
    elif can_plus:
        rho_0 = require_finite(rho_func(t, pressure_pa), "density(T)")
        rho_plus = require_finite(rho_func(t + dT, pressure_pa), "density(T+dT)")
        drho_dT = (rho_plus - rho_0) / dT
    elif can_minus:
        rho_minus = require_finite(rho_func(t - dT, pressure_pa), "density(T-dT)")
        rho_0 = require_finite(rho_func(t, pressure_pa), "density(T)")
        drho_dT = (rho_0 - rho_minus) / dT
    else:
        raise RuntimeError("Cannot form a temperature derivative at this point")

    rho_0 = require_finite(rho_func(t, pressure_pa), "density(T)")
    return -drho_dT / rho_0


def internal_energy_from_cp_table(temperatures_c, pressures_pa, cp_kj_kg_k,
                                  alpha_1_k, rho_kg_m3, reference_index=0):
    """
    Build Simscape-consistent specific internal energy u(T,p) [kJ/kg].

    Simscape Thermal Liquid uses
        du/dT|p = cp - p*alpha/rho
    and allows an arbitrary reference u_R because only energy differences matter.

    All input property matrices must have shape (nT, nP).
    """
    t_k = np.asarray(temperatures_c, dtype=float) + 273.15
    p_pa = np.asarray(pressures_pa, dtype=float)
    cp = np.asarray(cp_kj_kg_k, dtype=float)
    alpha = np.asarray(alpha_1_k, dtype=float)
    rho = np.asarray(rho_kg_m3, dtype=float)

    expected = (len(t_k), len(p_pa))
    for name, arr in (("cp", cp), ("alpha", alpha), ("rho", rho)):
        if arr.shape != expected:
            raise ValueError(f"{name} table has shape {arr.shape}; expected {expected}")
    if np.any(rho <= 0.0):
        raise RuntimeError("Cannot integrate internal energy with non-positive density")

    # p*alpha/rho is J/(kg*K); convert to kJ/(kg*K).
    integrand = cp - (p_pa[np.newaxis, :] * alpha / rho) * 1.0e-3

    u = np.zeros_like(integrand)
    ref = int(reference_index)
    if not 0 <= ref < len(t_k):
        raise ValueError("reference_index is outside the temperature table")

    # Integrate upward from the reference temperature.
    for i in range(ref + 1, len(t_k)):
        dT = t_k[i] - t_k[i - 1]
        u[i, :] = u[i - 1, :] + 0.5 * (integrand[i - 1, :] + integrand[i, :]) * dT

    # Integrate downward if the reference is not the first row.
    for i in range(ref - 1, -1, -1):
        dT = t_k[i + 1] - t_k[i]
        u[i, :] = u[i + 1, :] - 0.5 * (integrand[i + 1, :] + integrand[i, :]) * dT

    return u


def validity_core_indices(validity, min_valid_per_axis=2):
    """Return row/column indices that form a Simscape-usable validity core.

    For a 2-D Thermal Liquid lookup table, each retained temperature row must
    contain at least ``min_valid_per_axis`` valid pressure points, and each
    retained pressure column must contain at least that many valid temperature
    points.  Rows/columns that fail the condition are removed iteratively,
    because removing one axis can change the count on the other axis.
    """
    valid = np.asarray(validity, dtype=float) > 0.5
    if valid.ndim != 2:
        raise ValueError("Validity matrix must be two-dimensional")

    rows = np.arange(valid.shape[0])
    cols = np.arange(valid.shape[1])

    changed = True
    while changed:
        changed = False

        row_keep = np.sum(valid, axis=1) >= min_valid_per_axis
        if not np.all(row_keep):
            valid = valid[row_keep, :]
            rows = rows[row_keep]
            changed = True

        if valid.shape[0] < min_valid_per_axis:
            raise RuntimeError(
                "Validity region contains fewer than two usable temperature rows"
            )

        col_keep = np.sum(valid, axis=0) >= min_valid_per_axis
        if not np.all(col_keep):
            valid = valid[:, col_keep]
            cols = cols[col_keep]
            changed = True

        if valid.shape[1] < min_valid_per_axis:
            raise RuntimeError(
                "Validity region contains fewer than two usable pressure columns"
            )

    if np.any(np.sum(valid, axis=1) < min_valid_per_axis):
        raise RuntimeError("A retained temperature row has fewer than two valid points")
    if np.any(np.sum(valid, axis=0) < min_valid_per_axis):
        raise RuntimeError("A retained pressure column has fewer than two valid points")

    return rows, cols


# -----------------------------------------------------------------------------
# thermo liquid-density helper
# -----------------------------------------------------------------------------
def thermo_liquid_density(chemical, temperature_k, pressure_pa):
    """Liquid density [kg/m^3] from Chemical.VolumeLiquid, irrespective of equilibrium phase."""
    v_molar = chemical.VolumeLiquid(float(temperature_k), float(pressure_pa))
    v_molar = require_finite(v_molar, f"{chemical.name} liquid molar volume")
    if v_molar <= 0.0:
        raise RuntimeError(f"Non-positive liquid molar volume for {chemical.name}")
    # Chemical.MW is numerically g/mol; multiply by 1e-3 for kg/mol.
    return chemical.MW * 1.0e-3 / v_molar


if __name__ == "__main__":

    # =========================================================================
    # 1. NITROGEN -- GAS PROPERTIES
    # =========================================================================
    print("Fluid: Nitrogen processing using thermo...")

    n2_temperatures = np.arange(-100.0, 101.0, 1.0)  # degC

    n2_spec_enthalpy = np.empty_like(n2_temperatures)
    n2_spec_heat = np.empty_like(n2_temperatures)
    n2_dyn_visc = np.empty_like(n2_temperatures)
    n2_thermal_conductivity = np.empty_like(n2_temperatures)

    eval_pressure_pa = float(bar_to_pa(1.01325))
    n2 = Chemical("nitrogen", T=n2_temperatures[0] + 273.15, P=eval_pressure_pa)

    for i, temperature_c in enumerate(n2_temperatures):
        temperature_k = temperature_c + 273.15
        n2.calculate(T=temperature_k, P=eval_pressure_pa)

        # thermo.Chemical uses H, Cp, mu, k on a mass/SI basis here.
        n2_spec_enthalpy[i] = require_finite(n2.H, "N2 H") * 1.0e-3  # kJ/kg
        n2_spec_heat[i] = require_finite(n2.Cp, "N2 Cp") * 1.0e-3  # kJ/(kg*K)
        n2_dyn_visc[i] = require_finite(n2.mu, "N2 mu") * 1.0e6  # microPa*s
        n2_thermal_conductivity[i] = require_finite(n2.k, "N2 k") * 1.0e3  # mW/(m*K)

    # =========================================================================
    # 2. ETHANOL -- THERMAL LIQUID PROPERTIES
    # =========================================================================
    print("Fluid: Ethanol processing using thermo...")

    eth_temperatures_c = np.arange(0.0, 101.0, 2.0)  # 0 ... 100 degC
    eth_pressures_bar = np.arange(1.0, 101.0, 1.0)   # 1 ... 100 bar inclusive
    eth_pressures_pa = bar_to_pa(eth_pressures_bar)

    eth_shape = (len(eth_temperatures_c), len(eth_pressures_bar))
    eth_density = np.empty(eth_shape)
    eth_bulkmodulus = np.empty(eth_shape)
    eth_cte = np.empty(eth_shape)
    eth_spec_internal_energy = np.empty(eth_shape)
    eth_spec_heat = np.empty(eth_shape)
    eth_kin_visc = np.empty(eth_shape)
    eth_thermal_conductivity = np.empty(eth_shape)
    eth_validity = np.zeros(eth_shape, dtype=float)

    for i, temperature_c in enumerate(eth_temperatures_c):
        temperature_k = temperature_c + 273.15

        # Psat is temperature-only. Use a temporary Chemical state to obtain it.
        eth_t = Chemical("ethanol", T=temperature_k, P=101325.0)
        psat_pa = require_finite(eth_t.Psat, "ethanol Psat")
        tc_k = require_finite(eth_t.Tc, "ethanol Tc")
        tm_k = require_finite(eth_t.Tm, "ethanol Tm")

        for j, pressure_pa in enumerate(eth_pressures_pa):
            pressure_pa = float(pressure_pa)

            # Stable single-phase liquid region. Keep a small margin off saturation.
            is_valid_liquid = (
                temperature_k > tm_k
                and temperature_k < tc_k
                and pressure_pa >= 1.001 * psat_pa
            )
            eth_validity[i, j] = 1 if is_valid_liquid else 0

            # Invalid cells still need finite table entries for Simscape. Evaluate
            # them just inside the liquid side of the saturation boundary; the
            # validity matrix prevents those cells from being used as valid states.
            p_eval_pa = max(pressure_pa, 1.01 * psat_pa)

            state = Chemical("ethanol", T=temperature_k, P=p_eval_pa)
            if state.phase != "l":
                # Extra guard against phase-identification tolerance near Psat.
                p_eval_pa = max(p_eval_pa, 1.05 * psat_pa)
                state = Chemical("ethanol", T=temperature_k, P=p_eval_pa)
            if state.phase != "l":
                raise RuntimeError(
                    f"Could not create liquid ethanol state at T={temperature_c} C, "
                    f"P_eval={p_eval_pa/1e5:.4g} bar"
                )

            def eth_rho_at_p(p):
                return thermo_liquid_density(state, temperature_k, p)

            def eth_rho_at_t(t, p):
                return thermo_liquid_density(state, t, p)

            rho = require_finite(eth_rho_at_p(p_eval_pa), "ethanol density")
            eth_density[i, j] = rho  # kg/m^3

            k_bulk_pa = bulk_modulus_from_density(
                eth_rho_at_p,
                p_eval_pa,
                min_pressure_pa=max(1.0, psat_pa),
            )
            eth_bulkmodulus[i, j] = k_bulk_pa * 1.0e-9  # GPa

            eth_cte[i, j] = expansion_coefficient_from_density(
                eth_rho_at_t,
                temperature_k,
                p_eval_pa,
                t_min_k=tm_k,
                t_max_k=tc_k,
            )  # 1/K

            eth_spec_heat[i, j] = require_finite(state.Cpl, "ethanol Cpl") * 1.0e-3  # kJ/(kg*K)

            mu = require_finite(state.mul, "ethanol liquid viscosity")  # Pa*s
            eth_kin_visc[i, j] = mu / rho  # m^2/s

            eth_thermal_conductivity[i, j] = require_finite(
                state.kl, "ethanol liquid thermal conductivity"
            )  # W/(m*K)

    # Ensure the validity matrix is usable by Simscape's 2-D lookup-table
    # interpolation. This normally leaves the ethanol grid unchanged, but makes
    # the script robust if the chosen T/P ranges are changed later.
    eth_rows, eth_cols = validity_core_indices(eth_validity, min_valid_per_axis=2)
    if len(eth_rows) != eth_shape[0] or len(eth_cols) != eth_shape[1]:
        old_t_range = (eth_temperatures_c[0], eth_temperatures_c[-1])
        old_p_range = (eth_pressures_bar[0], eth_pressures_bar[-1])
        idx = np.ix_(eth_rows, eth_cols)
        eth_temperatures_c = eth_temperatures_c[eth_rows]
        eth_pressures_bar = eth_pressures_bar[eth_cols]
        eth_pressures_pa = eth_pressures_pa[eth_cols]
        eth_density = eth_density[idx]
        eth_bulkmodulus = eth_bulkmodulus[idx]
        eth_cte = eth_cte[idx]
        eth_spec_heat = eth_spec_heat[idx]
        eth_kin_visc = eth_kin_visc[idx]
        eth_thermal_conductivity = eth_thermal_conductivity[idx]
        eth_validity = eth_validity[idx]
        print(
            "Ethanol Simscape validity grid trimmed: "
            f"T {old_t_range[0]:g}..{old_t_range[1]:g} C -> "
            f"{eth_temperatures_c[0]:g}..{eth_temperatures_c[-1]:g} C; "
            f"P {old_p_range[0]:g}..{old_p_range[1]:g} bar -> "
            f"{eth_pressures_bar[0]:g}..{eth_pressures_bar[-1]:g} bar"
        )

    # Do not rely on Chemical.H/U here. In current thermo releases those
    # attributes are only created when Chemical.set_thermo() succeeds, and for
    # some fluids/states they can be absent. Build u from the same rho, alpha,
    # and cp tables that Simscape will use. Reference u=0 at the first T row.
    eth_spec_internal_energy = internal_energy_from_cp_table(
        eth_temperatures_c,
        eth_pressures_pa,
        eth_spec_heat,
        eth_cte,
        eth_density,
        reference_index=0,
    )

    # =========================================================================
    # 3. NITROUS OXIDE -- ROCKETPROPS
    # =========================================================================
    fluid_n2o = get_prop("N2O")
    if fluid_n2o is None:
        raise RuntimeError("RocketProps could not load N2O")

    print("Fluid: N2O processing using RocketProps...")

    # RocketProps' N2O saturated-liquid data terminate at Tc. Do not include a
    # supercritical row in a Thermal Liquid table. A 1 K margin also avoids the
    # Cp singularity immediately next to the critical point.
    n2o_tc_k = fluid_n2o.Tc / 1.8
    n2o_tc_c = n2o_tc_k - 273.15
    n2o_upper_exclusive_c = n2o_tc_c - 1.0
    n2o_temperatures_c = np.arange(-20.0, n2o_upper_exclusive_c, 2.0)

    n2o_pressures_bar = np.arange(1.0, 101.0, 1.0)  # 1 ... 100 bar inclusive
    n2o_pressures_pa = bar_to_pa(n2o_pressures_bar)
    n2o_pressures_psia = n2o_pressures_bar * PSIA_PER_BAR

    n2o_shape = (len(n2o_temperatures_c), len(n2o_pressures_bar))
    n2o_density = np.empty(n2o_shape)
    n2o_bulkmodulus = np.empty(n2o_shape)
    n2o_cte = np.empty(n2o_shape)
    n2o_spec_internal_energy = np.empty(n2o_shape)
    n2o_spec_heat = np.empty(n2o_shape)
    n2o_kin_visc = np.empty(n2o_shape)
    n2o_thermal_conductivity = np.empty(n2o_shape)
    # physical_validity records the real single-phase liquid region.
    # n2o_validity is the matrix supplied to Simscape; in solver-padding mode
    # it is deliberately set to ones after the table has been generated.
    n2o_physical_validity = np.zeros(n2o_shape, dtype=float)
    n2o_validity = np.zeros(n2o_shape, dtype=float)

    n2o_t_min_r, n2o_t_max_r = fluid_n2o.T_data_range()
    n2o_t_min_k = n2o_t_min_r / 1.8
    n2o_t_max_k = n2o_t_max_r / 1.8

    def n2o_rho_si(temperature_k, pressure_pa):
        t_r = float(temperature_k) * 1.8
        p_psia = float(pressure_pa) / PA_PER_PSIA
        sg = require_finite(fluid_n2o.SG_compressed(t_r, p_psia), "N2O SG_compressed")
        return sg * 1000.0  # g/mL -> kg/m^3

    for i, temperature_c in enumerate(n2o_temperatures_c):
        temperature_k = temperature_c + 273.15
        temperature_r = temperature_k * 1.8

        if not (n2o_t_min_r <= temperature_r < fluid_n2o.Tc):
            raise RuntimeError(
                f"N2O temperature {temperature_c:g} C is outside RocketProps liquid range"
            )

        psat_psia = require_finite(
            fluid_n2o.PvapAtTdegR(temperature_r), "N2O saturation pressure"
        )
        psat_pa = psat_psia * PA_PER_PSIA

        cp_kj_kg_k = (
            require_finite(fluid_n2o.CpAtTdegR(temperature_r), "N2O CpAtTdegR")
            * BTU_LBM_R_TO_KJ_KG_K
        )
        k_w_m_k = (
            require_finite(fluid_n2o.CondAtTdegR(temperature_r), "N2O CondAtTdegR")
            * BTU_HR_FT_R_TO_W_M_K
        )

        for j, (pressure_pa, pressure_psia) in enumerate(
            zip(n2o_pressures_pa, n2o_pressures_psia)
        ):
            pressure_pa = float(pressure_pa)
            pressure_psia = float(pressure_psia)

            is_valid_liquid = pressure_pa >= 1.001 * psat_pa
            n2o_physical_validity[i, j] = 1 if is_valid_liquid else 0
            n2o_validity[i, j] = n2o_physical_validity[i, j]

            # Solver padding: below the intended operating pressure, or below
            # saturation at the current temperature, evaluate the liquid-side
            # correlations at a benign surrogate pressure.  These values exist
            # only to keep the Simscape lookup tables well formed; they are not
            # physical N2O properties at the table-column pressure.
            p_floor_pa = N2O_INTENDED_MIN_PRESSURE_BAR * PA_PER_BAR
            p_eval_pa = max(pressure_pa, p_floor_pa, 1.01 * psat_pa)
            p_eval_psia = p_eval_pa / PA_PER_PSIA

            rho = require_finite(n2o_rho_si(temperature_k, p_eval_pa), "N2O density")
            n2o_density[i, j] = rho  # kg/m^3

            def n2o_rho_at_p(p):
                return n2o_rho_si(temperature_k, p)

            def n2o_rho_at_t(t, p):
                return n2o_rho_si(t, p)

            # IMPORTANT: RocketProps SG_compressed is a pressure-dependent
            # curve fit whose value is well behaved, but its *very local*
            # numerical derivative has a small interpolation artefact around
            # 76 bar for several temperatures.  Use a 1 bar secant interval,
            # matching the pressure-table resolution, rather than a 1 kPa
            # derivative interval.
            k_bulk_pa = bulk_modulus_from_density(
                n2o_rho_at_p,
                p_eval_pa,
                min_pressure_pa=max(1.0, psat_pa),
                pressure_step_pa=1.0e5,  # 1 bar
                relative_step=0.0,
            )
            n2o_bulkmodulus[i, j] = k_bulk_pa * 1.0e-9  # GPa

            # The same RocketProps fit can have noisy infinitesimal
            # temperature derivatives at high pressure.  A +/-3 K secant
            # derivative removes the interpolation artefact while retaining
            # the physical temperature trend of the compressed-liquid density.
            n2o_cte[i, j] = expansion_coefficient_from_density(
                n2o_rho_at_t,
                temperature_k,
                p_eval_pa,
                t_min_k=n2o_t_min_k,
                t_max_k=min(n2o_t_max_k, n2o_tc_k - 1.0e-6),
                temperature_step_k=3.0,
            )  # 1/K

            # RocketProps provides saturated Cp, not a compressed-liquid Cp model,
            # so Cp is temperature-only in this table.
            n2o_spec_heat[i, j] = cp_kj_kg_k

            mu_poise = require_finite(
                fluid_n2o.Visc_compressed(temperature_r, p_eval_psia),
                "N2O Visc_compressed",
            )
            mu_pa_s = mu_poise * POISE_TO_PA_S
            n2o_kin_visc[i, j] = mu_pa_s / rho  # m^2/s

            # RocketProps conductivity is saturated-liquid data and is T-only.
            n2o_thermal_conductivity[i, j] = k_w_m_k  # W/(m*K)

    # ---------------------------------------------------------------------
    # Simscape solver padding
    # ---------------------------------------------------------------------
    # Thermal Liquid requires the minimum valid pressure to be <= the
    # atmospheric pressure.  The real N2O liquid region in this T range does
    # not satisfy that requirement.  Because this model is intentionally
    # constrained to P >= N2O_INTENDED_MIN_PRESSURE_BAR, we retain the 1..100
    # bar pressure vector and mark every lookup-table node numerically valid.
    # Nonphysical nodes have already been populated from a liquid-side
    # surrogate state above.  Keep n2o_physical_validity separately for
    # diagnostics and post-run checking.
    if N2O_SOLVER_PADDING:
        n2o_validity[:, :] = 1.0
        print(
            "N2O solver padding ENABLED: Simscape validity is forced to 1 "
            f"over {n2o_pressures_bar[0]:g}..{n2o_pressures_bar[-1]:g} bar. "
            f"Intended operating pressure must remain >= "
            f"{N2O_INTENDED_MIN_PRESSURE_BAR:g} bar."
        )
        print(
            "N2O physical liquid-valid nodes: "
            f"{int(np.sum(n2o_physical_validity))}/{n2o_physical_validity.size}. "
            "Use physical_validity_n2o to identify genuinely liquid states."
        )
    else:
        # Strict mode: preserve the physically valid region and trim unusable
        # rows/columns.  This mode can again trigger Simscape's atmospheric-
        # pressure constraint, so solver-padding mode is intended for this model.
        n2o_rows, n2o_cols = validity_core_indices(
            n2o_physical_validity, min_valid_per_axis=2
        )
        idx = np.ix_(n2o_rows, n2o_cols)
        n2o_temperatures_c = n2o_temperatures_c[n2o_rows]
        n2o_pressures_bar = n2o_pressures_bar[n2o_cols]
        n2o_pressures_pa = n2o_pressures_pa[n2o_cols]
        n2o_pressures_psia = n2o_pressures_psia[n2o_cols]
        n2o_density = n2o_density[idx]
        n2o_bulkmodulus = n2o_bulkmodulus[idx]
        n2o_cte = n2o_cte[idx]
        n2o_spec_heat = n2o_spec_heat[idx]
        n2o_kin_visc = n2o_kin_visc[idx]
        n2o_thermal_conductivity = n2o_thermal_conductivity[idx]
        n2o_physical_validity = n2o_physical_validity[idx]
        n2o_validity = n2o_physical_validity.copy()

    # RocketProps has no internal-energy correlation. Rather than mixing a
    # RocketProps liquid state with thermo.Chemical enthalpy (which can be
    # unavailable and can use a different EOS/reference), construct u directly
    # from cp, alpha, and rho using the equation implemented by Simscape.
    n2o_spec_internal_energy = internal_energy_from_cp_table(
        n2o_temperatures_c,
        n2o_pressures_pa,
        n2o_spec_heat,
        n2o_cte,
        n2o_density,
        reference_index=0,
    )

    # =========================================================================
    # 4. SANITY CHECKS AND EXPORT TO MATLAB
    # =========================================================================
    tables_to_check = {
        "n2_enthalpy": n2_spec_enthalpy,
        "n2_Cp": n2_spec_heat,
        "n2_mu": n2_dyn_visc,
        "n2_k": n2_thermal_conductivity,
        "ethanol_rho": eth_density,
        "ethanol_bulk_modulus": eth_bulkmodulus,
        "ethanol_alpha": eth_cte,
        "ethanol_u": eth_spec_internal_energy,
        "ethanol_Cp": eth_spec_heat,
        "ethanol_nu": eth_kin_visc,
        "ethanol_k": eth_thermal_conductivity,
        "n2o_rho": n2o_density,
        "n2o_bulk_modulus": n2o_bulkmodulus,
        "n2o_alpha": n2o_cte,
        "n2o_u": n2o_spec_internal_energy,
        "n2o_Cp": n2o_spec_heat,
        "n2o_nu": n2o_kin_visc,
        "n2o_k": n2o_thermal_conductivity,
    }

    for name, array in tables_to_check.items():
        if not np.all(np.isfinite(array)):
            bad = np.argwhere(~np.isfinite(array))
            raise RuntimeError(f"{name} contains non-finite values at {bad[:10].tolist()}")

    if np.any(eth_bulkmodulus <= 0.0):
        raise RuntimeError("Ethanol bulk modulus contains non-positive values")
    if np.any(n2o_bulkmodulus <= 0.0):
        raise RuntimeError("N2O bulk modulus contains non-positive values")
    if np.any(eth_cte <= 0.0):
        raise RuntimeError("Ethanol thermal expansion table contains non-positive values")
    if np.any(n2o_cte <= 0.0):
        raise RuntimeError("N2O thermal expansion table contains non-positive values")
    if np.any(eth_density <= 0.0) or np.any(n2o_density <= 0.0):
        raise RuntimeError("A liquid density table contains non-positive values")

    for fluid_name, validity in (("ethanol", eth_validity), ("N2O", n2o_validity)):
        row_counts = np.sum(validity > 0.5, axis=1)
        col_counts = np.sum(validity > 0.5, axis=0)
        if np.any(row_counts < 2) or np.any(col_counts < 2):
            raise RuntimeError(
                f"{fluid_name} validity matrix is not Simscape-safe: "
                f"minimum row count={row_counts.min()}, "
                f"minimum column count={col_counts.min()}"
            )

    matlab_workspace_vars = {
        # Nitrogen gas
        "T_prop_n2": n2_temperatures,
        "enthalpy_n2": n2_spec_enthalpy,
        "spec_heat_n2": n2_spec_heat,
        "dyn_visc_n2": n2_dyn_visc,
        "thermal_cond_n2": n2_thermal_conductivity,

        # Ethanol thermal liquid
        "T_prop_ethanol": eth_temperatures_c,
        "P_prop_ethanol": eth_pressures_bar,
        "rho_ethanol": eth_density,
        "bulk_modulus_ethanol": eth_bulkmodulus,
        "cte_ethanol": eth_cte,
        "internal_energy_ethanol": eth_spec_internal_energy,
        "spec_heat_ethanol": eth_spec_heat,
        "kin_visc_ethanol": eth_kin_visc,
        "thermal_cond_ethanol": eth_thermal_conductivity,
        "validity_ethanol": eth_validity,

        # Nitrous oxide thermal liquid
        "T_prop_n2o": n2o_temperatures_c,
        "P_prop_n2o": n2o_pressures_bar,
        "rho_n2o": n2o_density,
        "bulk_modulus_n2o": n2o_bulkmodulus,
        "cte_n2o": n2o_cte,
        "internal_energy_n2o": n2o_spec_internal_energy,
        "spec_heat_n2o": n2o_spec_heat,
        "kin_visc_n2o": n2o_kin_visc,
        "thermal_cond_n2o": n2o_thermal_conductivity,
        "validity_n2o": n2o_validity,
        "physical_validity_n2o": n2o_physical_validity,
        "n2o_intended_min_pressure_bar": np.array([[N2O_INTENDED_MIN_PRESSURE_BAR]], dtype=float),
    }

    output_path = output_directory() / "simscape_fluids_data.mat"
    scipy.io.savemat(str(output_path), matlab_workspace_vars, do_compression=True)

    print(f"Export complete: {output_path}")
    print(
        f"Ethanol valid liquid cells: {int(eth_validity.sum())}/{eth_validity.size}; "
        f"N2O Simscape-valid cells: {int(n2o_validity.sum())}/{n2o_validity.size}; "
        f"N2O physically liquid cells: "
        f"{int(n2o_physical_validity.sum())}/{n2o_physical_validity.size}"
    )
    print(
        "IMPORTANT: N2O solver padding deliberately makes nonphysical states "
        "available to Simscape. Do not trust N2O results below the intended "
        f"{N2O_INTENDED_MIN_PRESSURE_BAR:g} bar operating floor, and also check "
        "physical_validity_n2o for the temperature/pressure operating region."
    )
