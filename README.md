# Steam Pasteurization Process Design for Sugarcane Bagasse Using Experimental Property Characterization and Dual-Regime DWSIM Simulation

## Project Summary

This repository contains a steam pasteurization process design study for sugarcane bagasse developed as a chemical engineering final year project. The work integrates experimental characterization, heat-transfer modeling, process simulation, and sensitivity analysis to evaluate steam-based pasteurization of bagasse intended for use as a mushroom cultivation substrate.

An initial literature review identified significant variability in published thermophysical properties of bagasse, making direct use of literature data unsuitable for process design. Consequently, an experimental program was conducted to determine thermal conductivity, specific heat capacity, moisture content, and bulk density under multiple material conditions.

Following experimental evaluation and statistical comparison, wet uncompacted bagasse was selected as the process design basis because it most closely represents industrial substrate preparation and utilization practices.

The experimentally determined properties were incorporated into a transient mathematical model describing sensible heat transfer, steam condensation, and biomass heating behavior. The model was implemented in DWSIM using custom unit operations and IronPython scripts.

Two separate condensation scenarios were developed:

* Condensation without condensate deposition.
* Condensation with condensate deposition and moisture accumulation.

Steam flowrate sensitivity analysis was performed to evaluate process performance and identify suitable operating conditions for steam pasteurization.

The repository should be viewed as a process-design and engineering-analysis artifact rather than a validated industrial pasteurization system.

---

## Current Status

The repository includes:

* Experimental characterization data.
* Process design basis documentation.
* Mathematical model development notes.
* DWSIM simulation files.
* Custom IronPython unit-operation scripts.
* Flowrate sensitivity study results.
* Reference simulation outputs.
* Supporting engineering documentation.

The repository represents the final project state submitted for academic review.

Additional experimental validation and industrial-scale testing would be required before operational implementation.

---

## Repository Structure

Bagasse_Steam_Pasteurization/

Bagasse_Steam_Pasteurization/
│
├── README.md
│
├── data/
│   ├── experimental/
│   │   ├── thermal_conductivity/
│   │   ├── specific_heat_capacity/
│   │   ├── moisture_content/
│   │   └── bulk_density/
│   │
│   └── processed/
│       └── design_basis_properties.xlsx
│
├── mathematical_model/
│   ├── governing_equations.pdf
│   ├── model_assumptions.pdf
│   ├── biot_number_analysis.pdf
│   └── derivations/
│
├── dwsim/
│   ├── deposition_model/
│   │   ├── deposition_model.dwxmz
│   │   └── deposition_script.py
│   │
│   └── no_deposition_model/
│       ├── no_deposition_model.dwxmz
│       └── no_deposition_script.py
│
├── results/
│   ├── flowrate_sensitivity/
│   │   ├── flowrate_sensitivity_summary.xlsx
│   │   └── pasteurization_time_table.xlsx
│   │
│   ├── reference_outputs/
│   │   ├── run_0_5kgph.xlsx
│   │   ├── run_10kgph.xlsx
│   │   ├── run_20kgph.xlsx
│   │   └── run_100kgph.xlsx
│   │
│   └── figures/
│       ├── flowrate_vs_pasteurization_time.png
│       ├── model_comparison.png
│   
│
└── documentation/
    ├── Technical_Report.pdf

---

## Engineering Workflow

The project was executed through five major engineering phases:

### Phase 1 – Literature Review and Experimental Planning

Published bagasse thermophysical properties were reviewed and assessed for suitability in process design applications.

Due to inconsistent literature values, an experimental program was developed to determine process-relevant material properties.

### Phase 2 – Experimental Characterization

Custom experimental rigs were designed and fabricated.

Experiments were conducted to determine:

* Thermal conductivity
* Specific heat capacity
* Moisture content
* Bulk density

Material characterization was performed under multiple conditions:

* Wet uncompacted bagasse
* Wet compacted bagasse
* Dry uncompacted bagasse
* Dry compacted bagasse

Wet bagasse moisture content was approximately 70–75%.

Dry bagasse moisture content was approximately 10%.

Following statistical evaluation of results, wet uncompacted bagasse was selected as the process design basis.

### Phase 3 – Heat Transfer Analysis

A Biot number analysis was performed to assess internal thermal resistance relative to external convective resistance.

The analysis informed:

* Modeling assumptions
* Heat-transfer treatment
* Representative bagasse dimensions
* Process design considerations

### Phase 4 – Mathematical Modeling

Transient mass and energy balances were developed for steam–bagasse interaction.

The model incorporated:

* Sensible heat transfer between steam and bagasse.
* Latent heat transfer from steam condensation.
* Dynamic steam quality behavior.
* Condensation-rate estimation.
* Time-dependent bagasse temperature prediction.

### Phase 5 – Process Simulation and Design

The governing equations were implemented in DWSIM through custom unit operations and IronPython scripting.

Sensitivity analysis was conducted across a range of steam flowrates to evaluate process performance and establish preliminary design parameters.

---

## Experimental Characterization

Experimental data are stored under:

data/experimental/

The experimental program generated:

| Property               | Purpose                      |
| ---------------------- | ---------------------------- |
| Thermal Conductivity   | Heat-transfer modeling input |
| Specific Heat Capacity | Energy balance input         |
| Moisture Content       | Material characterization    |
| Bulk Density           | Process design calculations  |

Processed design-basis properties are stored under:

data/processed/

Only wet uncompacted bagasse properties were used in the final process model.

---

## Biot Number Analysis

Supporting calculations and documentation are stored under:

mathematical_model/

The Biot number analysis was used to evaluate the relative significance of internal conduction resistance and external convection resistance during steam heating.

The analysis supported the thermal modeling assumptions adopted within the simulation framework.

---

## Mathematical Model

The process was modeled as a transient steam-heating system.

Two heat-transfer mechanisms were considered:

### Sensible Heat Transfer

At steam introduction, energy transfer occurs due to the temperature difference between steam and bagasse.

The model accounts for transient heating of both phases through coupled energy balances.

### Latent Heat Transfer

As steam approaches saturation conditions, condensation occurs.

The model calculates condensation rates using heat-transfer correlations and incorporates latent heat release into the bagasse energy balance.

---

## Condensation Regime Development

Two separate model formulations were developed to investigate uncertainty associated with condensate behavior.

### Scenario 1 – Condensation Without Deposition

Implemented in:

dwsim/no_deposition_model/

Assumptions:

* Steam condenses.
* Latent heat is transferred to the bagasse.
* Condensed water does not accumulate within the biomass bed.
* Bagasse mass remains constant.

Outputs include:

* Bagasse temperature
* Steam temperature
* Condensation rate
* Steam quality
* Condensed mass

### Scenario 2 – Condensation With Deposition

Implemented in:

dwsim/deposition_model/

Assumptions:

* Steam condenses.
* Condensed water deposits onto the bagasse.
* Bagasse mass increases during operation.
* Heat and mass transfer are coupled.

Additional outputs include:

* Dynamic bagasse mass accumulation
* Outlet steam reduction due to condensation

---

## DWSIM Implementation

The repository contains DWSIM flowsheets and custom IronPython scripts.

Simulation components include:

| Component             | Purpose                           |
| --------------------- | --------------------------------- |
| DWSIM Flowsheet       | Process representation            |
| Custom Unit Operation | Mathematical model implementation |
| IronPython Scripts    | Dynamic calculations              |
| Spreadsheet Interface | Result export and visualization   |

The simulation tracks:

* Bagasse temperature
* Steam temperature
* Condensation rate
* Steam outlet flowrate
* Steam quality
* Condensed mass
* Bagasse mass accumulation (deposition model)

---

## Sensitivity Analysis

Steam flowrate sensitivity analysis was performed between approximately:

0.1 kg/h and 200 kg/h

For each simulation run:

* Steam flowrate was specified.
* Simulation was executed until the bagasse reached 75°C.
* Pasteurization time was recorded.
* Results were exported to spreadsheets for analysis.

---

## Key Results

The primary simulation output was pasteurization time required to achieve a bagasse temperature of 75°C.

| Steam Flowrate (kg/h) | No Deposition (h) | Deposition (h) |
| --------------------- | ----------------: | -------------: |
| 0.1                   |             32.91 |          34.00 |
| 0.5                   |             25.75 |          28.56 |
| 2                     |             16.01 |          18.00 |
| 4                     |             10.31 |          12.22 |
| 6                     |              6.88 |           8.19 |
| 8                     |              5.15 |           6.11 |
| 10                    |              4.13 |           4.86 |
| 12                    |             12.64 |           4.17 |
| 14                    |             13.53 |           3.67 |
| 16                    |             14.54 |           3.33 |
| 18                    |             15.71 |           3.06 |
| 20                    |             17.06 |           2.92 |
| 50                    |             25.63 |           2.64 |
| 100                   |             21.99 |           2.50 |
| 150                   |             18.86 |           2.36 |
| 200                   |             16.43 |           2.36 |

The results demonstrate the influence of steam flowrate and condensate behavior on predicted pasteurization performance.

The deposition model generally predicted reduced pasteurization times at higher flowrates due to additional energy and moisture accumulation within the bagasse bed.

The no-deposition model exhibited non-monotonic behavior at higher steam flowrates. The source of this behavior was not fully investigated during the project and remains an area for future study.

---

## Data Layout

Experimental data:

data/experimental/

Processed design-basis data:

data/processed/

Simulation files:

dwsim/

Model documentation:

mathematical_model/

Simulation outputs:

results/

---

## Output Files

Representative simulation outputs may include:

results/raw_simulation_outputs/

Example workbook contents:

| Sheet                | Contents                                   |
| -------------------- | ------------------------------------------ |
| Temperature Profile  | Steam and bagasse temperatures versus time |
| Condensation Profile | Condensation-rate history                  |
| Steam Quality        | Steam-quality evolution                    |
| Mass Balance         | Condensate generation and accumulation     |
| Summary              | Final pasteurization metrics               |

Summary analysis files are stored under:

results/summary_tables/

Generated figures are stored under:

results/figures/

---

## How To Run

Open the appropriate DWSIM flowsheet:

* deposition_model.dwxmz
* no_deposition_model.dwxmz

Configure:

* Bagasse properties
* Geometry
* Steam flowrate
* Initial conditions

Execute the simulation.

Review exported results through the DWSIM spreadsheet interface or saved workbook outputs.

---

## Model Assumptions

* Wet uncompacted bagasse represents the process design basis.
* Steam pressure remains constant throughout the simulation.
* Condensation occurs at saturation conditions.
* Heat-transfer coefficients are estimated using Nusselt correlations.
* Bagasse properties remain constant during each simulation.
* Steam flowrate remains constant during operation.
* The models are intended for process-design and sensitivity-analysis purposes.

---

## Known Limitations

* Experimental uncertainty exists in measured thermophysical properties.
* The model has not been validated against industrial-scale pasteurization data.
* Pressure-drop effects were not considered.
* Steam-distribution effects within the biomass bed were not considered.
* Spatial moisture gradients were not modeled.
* The no-deposition scenario exhibited unresolved non-monotonic behavior at higher steam flowrates.
* Results should be interpreted as engineering-analysis outputs rather than operational guarantees.

---

## Future Improvements

Potential future work includes:

* Industrial-scale validation.
* Additional property characterization studies.
* Investigation of the no-deposition model behavior.
* Distributed heat and moisture transfer modeling.
* Pressure-drop modeling.
* Integration with standalone Python-based simulation workflows.

---

## License

No license file is currently included.

Usage rights should be confirmed with the project authors before reuse.

---

## Project Note

Before relying on results, users should review the experimental assumptions, mathematical-model derivations, DWSIM implementation details, and simulation outputs.

The committed files represent reference engineering artifacts generated during the project and should not be interpreted as validated industrial design standards.
