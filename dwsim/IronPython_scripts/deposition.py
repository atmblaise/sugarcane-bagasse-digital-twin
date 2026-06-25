# ----------------------------------------------------------------------------------
# Pasteurizer model — sensible + condensation (deposition)
# ----------------------------------------------------------------------------------

import System
import math

# -------------------------
# helper functions
# -------------------------
def convert_mass_frac_to_molar_frac(x_vap, x_wat):
    m_vap = x_vap * 10000.0
    m_wat = x_wat * 10000.0
    n_vap = m_vap / 18.01528
    n_wat = m_wat / 18.01528
    n_tot = n_vap + n_wat
    y_vap = n_vap / n_tot
    y_wat = 1.0 - y_vap
    return [y_vap, y_wat]

def invert_2x2(m11, m12, m21, m22):
    det = m11*m22 - m12*m21
    if abs(det) < 1e-18:
        return None
    return (m22/det, -m12/det, -m21/det, m11/det)

def calc_enthalpy(Temp_steam, Temp_sat, Temp_steam_in, enthalpy_in):
    # returns J/kg
    hg_100 = 2675.8 * 1000.0
    cp_sat_steam = 2.05 * 1000.0
    if Temp_steam > Temp_sat:
        if Temp_steam == Temp_steam_in:
            return enthalpy_in
        else:
            return hg_100 + cp_sat_steam * (Temp_steam - Temp_sat)
    else:
        return hg_100

def calc_rate_cond(Temp_bagasse, Temp_sat, Area, Length_bagasse):
    # Nusselt-based h_coeff (laminar flat plate)
    Re_no = 500000.0
    Pr_no = visc_steam * cp_steam / therm_cond_steam
    Nu_no = 0.664 * (Re_no ** 0.5) * (Pr_no ** (1.0/3.0))
    h_coeff_cond = Nu_no * therm_cond_steam / Length_bagasse_block

    rate_cond = h_coeff_cond * Area * (Temp_sat - Temp_bagasse) / hfg_100
    if rate_cond < 0.0:
        return 0.0
    return rate_cond

# -------------------------
# call flowsheet objects
# -------------------------
stream = Flowsheet.GetFlowsheetSimulationObject('inlet_stream')
outlet = Flowsheet.GetFlowsheetSimulationObject('outlet_stream')
obj = Flowsheet.GetFlowsheetSimulationObject('pasteurizer')
phase = stream.GetPhase('Vapor')
Spreadsheet = Flowsheet.FormSpreadsheet

# -------------------------
# read inlet steam properties (mass flow constant)
# -------------------------
mass_flowrate_in = stream.GetMassFlow()            # kg/s (constant)
enthalpy_in = stream.GetMassEnthalpy() * 1000      # convert to J/kg
pressure_steam_in = stream.GetPressure()           # Pa
Temp_steam_in = stream.GetTemperature() - 273.15   # convert to °C
density_steam = phase.Properties.density           # kg/m3
cv_steam = phase.Properties.heatCapacityCv * 1000  # convert to J/kg K
cp_steam = phase.Properties.heatCapacityCp * 1000  # convert to J/kg K
therm_cond_steam = phase.Properties.thermalConductivity  # W/m K
visc_steam = phase.Properties.viscosity            # kg/m s

# -------------------------
# read pasteurizer input variables
# -------------------------
value = obj.InputVariables
m_bagasse_init = value['Mass_bagasse (kg)']
cp_bagasse = value['Cp_bagasse (J/kg oC)']    # J/kg.K
run_time = value['run_time (hrs)'] * 3600.0
Temp_init = value['T_init(oC)']
Length_bagasse_block = value['Length of bagasse block (m)']
Width_bagasse_block = value['Width of bagasse block (m)']
Thickness_bagasse_block = value['Thickness of bagasse block (m)']
No_bagasse_blocks = value['Number of bagasse blocks']

# -------------------------
# derived geometry and params
# -------------------------
Temp_sat = 100.0  # °C
hfg_100 = 2256.7 * 1000.0  # J/kg
Temp_past = 75  # target pasteurization temperature

Vol_unit = 1.5 * (Length_bagasse_block * Width_bagasse_block * Thickness_bagasse_block * No_bagasse_blocks)
Area_heat_transfer = Length_bagasse_block * Width_bagasse_block * No_bagasse_blocks
m_steam = density_steam * Vol_unit

# Nusselt-based h_coeff (laminar flat plate)
Re_no = 500000.0
Pr_no = visc_steam * cp_steam / therm_cond_steam
Nu_no = 0.664 * (Re_no ** 0.5) * (Pr_no ** (1.0/3.0))
h_coeff = Nu_no * therm_cond_steam / Length_bagasse_block

# -------------------------
# numerical settings and logging
# -------------------------
time_step = 0.05

# -----------------------------------------------------------
# TIME AND ARRAY INITIALIZATION
# -----------------------------------------------------------
time = [i * time_step for i in range(int(run_time / time_step) + 1)]
Temp_bagasse = []
Temp_steam = []
mass_flowrate_out = []
rate_cond = []
m_bagasse = []
quality_inst = []
cond_mass = []

# -----------------------------------------------------------
# CHECK MASS FLOW CONDITION
# -----------------------------------------------------------
rate_cond_max = h_coeff * Area_heat_transfer * (Temp_sat - Temp_init) / hfg_100
if (mass_flowrate_in <= rate_cond_max):
    print('Warning: Mass flowrate in needs to be adjusted upwards to be greater than rate of condensation')

# -----------------------------------------------------------
# MAIN SIMULATION LOOP
# -----------------------------------------------------------
for i in range(len(time)):

    if i == 0:
        # --- INITIAL CONDITIONS ---
        rate_cond.append(0.0)
        mass_flowrate_out.append(mass_flowrate_in)
        Temp_bagasse.append(Temp_init)
        Temp_steam.append(Temp_steam_in)
        m_bagasse.append(m_bagasse_init)
        log_counter = 0

    else:
        # --- READ PREVIOUS STEP VALUES ---
        Ts_prev = Temp_steam[i - 1]
        Tb_prev = Temp_bagasse[i - 1]

        # ============================================================
        # SENSIBLE HEATING PHASE
        # ============================================================
        if Ts_prev > Temp_sat:
            rate_cond.append(0.0)
            mass_flowrate_out.append(mass_flowrate_in)

            enthalpy_out = calc_enthalpy(Ts_prev, Temp_sat, Temp_steam_in, enthalpy_in)

            H_A = h_coeff * Area_heat_transfer
            A11 = - H_A / (m_steam * cv_steam)
            A12 =   H_A / (m_steam * cv_steam)
            A21 =   H_A / (m_bagasse_init * cp_bagasse)
            A22 = - H_A / (m_bagasse_init * cp_bagasse)

            B1 = (mass_flowrate_in * (enthalpy_in - enthalpy_out)) / (m_steam * cv_steam)
            B2 = 0.0

            AT1 = A11 * Ts_prev + A12 * Tb_prev + B1
            AT2 = A21 * Ts_prev + A22 * Tb_prev + B2

            T_s_pred = Ts_prev + time_step * AT1
            T_b_pred = Tb_prev + time_step * AT2

            # --- ONE-STEP CORRECTOR ---
            m11 = 1.0 - time_step * A11
            m12 = - time_step * A12
            m21 = - time_step * A21
            m22 = 1.0 - time_step * A22
            inv = invert_2x2(m11, m12, m21, m22)

            if inv is not None:
                inv11, inv12, inv21, inv22 = inv
                rhs1 = Ts_prev + time_step * B1
                rhs2 = Tb_prev + time_step * B2
                T_s_new = inv11 * rhs1 + inv12 * rhs2
                T_b_new = inv21 * rhs1 + inv22 * rhs2
            else:
                T_s_new = T_s_pred
                T_b_new = T_b_pred

            Temp_steam.append(T_s_new)
            Temp_bagasse.append(T_b_new)

        # ============================================================
        # CONDENSATION PHASE (WITH DEPOSITION)
        # ============================================================
        else:
            # --- Condensation rate ---
            rc = min(mass_flowrate_in, calc_rate_cond(Tb_prev, Temp_sat, Area_heat_transfer, Length_bagasse_block))
            rate_cond.append(rc)

            # --- Previous bagasse mass ---
            if i == 1:
                m_b_prev = m_bagasse_init
            else:
                m_b_prev = m_bagasse[-1]

            # --- New bagasse mass after condensation (deposition) ---
            m_b_new = m_b_prev + rc * time_step
            m_bagasse.append(m_b_new)

            # --- Outlet mass flowrate (uncondensed part) ---
            m_out = mass_flowrate_in - rc
            mass_flowrate_out.append(m_out)

            # --- Enthalpy balance ---
            if rc == mass_flowrate_in:
                enthalpy_out = 0.0
            else:
                enthalpy_out = calc_enthalpy(Ts_prev, Temp_sat, Temp_steam_in, enthalpy_in)

            Temp_steam.append(Temp_sat)

            # --- Energy balance for bagasse ---
            numerator = (mass_flowrate_in * (enthalpy_in - enthalpy_out) + rc * (enthalpy_out - cp_bagasse * Tb_prev))

            T_b_new = Tb_prev + time_step * numerator / (m_b_new * cp_bagasse)
            Temp_bagasse.append(T_b_new)

    # -----------------------------------------------------------
    # QUALITY AND CONDENSATE MASS UPDATES
    # -----------------------------------------------------------
    if i > 0:
        qi = 1  
        quality_inst.append(qi)
        cond_mass.append(rate_cond[i - 1] * time_step)

    # -----------------------------------------------------------
    # SANITY CHECKS
    # -----------------------------------------------------------
    if Temp_steam[i] + 2.0 < Temp_sat:
        print('Warning: Temp of outlet steam below accepted value. Check timestep.')

    # -----------------------------------------------------------
    # EARLY STOP CONDITION
    # -----------------------------------------------------------
    if Temp_bagasse[i] > 75.0:
        break

# ---------------------------------------------------------------------------------------------------------

# write out to outlet stream (final values)
outlet.Clear()
outlet.SetPressure(101325)
outlet.SetTemperature(Temp_steam[-1] + 273.15)
outlet.SetMassFlow(mass_flowrate_out[-1])

# final steam quality (mass basis)
m_vap_remaining = m_steam - cond_mass[-1]
quality_final = m_vap_remaining / m_steam

molar_frac = convert_mass_frac_to_molar_frac(quality_final, 1.0 - quality_final)
value_arr = System.Array[System.Double]([1, molar_frac[0], molar_frac[1], 0, 0])
outlet.SetOverallComposition(value_arr)

enthalpy_out = calc_enthalpy(Temp_steam[-1], Temp_sat, Temp_steam_in, enthalpy_in)
outlet.SetMassEnthalpy(enthalpy_out / 1000.0)

# ------------------------------------------------------------------------------------------------
# Write out condensed solutions to spreadsheet
counter = 0
save_after_these_steps = 10000


# Initialize condensed logging arrays
time_condensed = []
Temp_bagasse_condensed = []
Temp_steam_condensed = []
rate_cond_condensed = []
mass_flowrate_out_condensed = []
m_bagasse_condensed = []
quality_inst_condensed = []
cond_mass_condensed = []


for i in range(len(Temp_bagasse)):
    if counter == 0 or counter == save_after_these_steps:
        time_condensed.append(time[i])
        Temp_bagasse_condensed.append(Temp_bagasse[i])
        Temp_steam_condensed.append(Temp_steam[i])
        rate_cond_condensed.append(rate_cond[i])
        mass_flowrate_out_condensed.append(mass_flowrate_out[i])
        m_bagasse_condensed.append(m_bagasse[i])
        quality_inst_condensed.append(quality_inst[i])
        cond_mass_condensed.append(cond_mass[i])
        counter = 0
    counter += 1

# write condensed solutions to spreadsheet
for row in range(65000):
    for col in range(26):
        Spreadsheet.SetCellValue(chr(65 + col) + str(row + 1), None)

Spreadsheet.SetCellValue("A1", "Time (sec)")
Spreadsheet.SetCellValue("B1", "Bagasse temperature (°C)")
Spreadsheet.SetCellValue("C1", "Steam temperature (°C)")
Spreadsheet.SetCellValue("D1", "Rate of condensation (kg/s)")
Spreadsheet.SetCellValue("E1", "Flowrate of steam at outlet (kg/s)")
Spreadsheet.SetCellValue("F1", "Mass of bagasse (kg)")
Spreadsheet.SetCellValue("G1", "Inst Quality")
Spreadsheet.SetCellValue("H1", "Condensed mass")

for i in range(len(time_condensed)):
    Spreadsheet.SetCellValue("A"+str(i+2), time_condensed[i])
    Spreadsheet.SetCellValue("B"+str(i+2), Temp_bagasse_condensed[i])
    Spreadsheet.SetCellValue("C"+str(i+2), Temp_steam_condensed[i])
    Spreadsheet.SetCellValue("D"+str(i+2), rate_cond_condensed[i])
    Spreadsheet.SetCellValue("E"+str(i+2), mass_flowrate_out_condensed[i])
    Spreadsheet.SetCellValue("F"+str(i+2), m_bagasse_condensed[i])
    Spreadsheet.SetCellValue("G"+str(i+2), quality_inst_condensed[i])
    Spreadsheet.SetCellValue("H"+str(i+2), cond_mass_condensed[i])

# End of script