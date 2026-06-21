
## Sugarcane Bagasse Pasteurization Model

From Agricultural Waste to Engineered Thermal System

> A computational and thermodynamic study of wet bagasse pasteurization using first-principles modeling, experimental characterization, and process simulation.




---

### Project Overview

Sugarcane bagasse is a widely available agricultural by-product often treated as waste despite its potential in bioenergy, materials, and sustainable industrial applications. However, its high moisture content (~75%) leads to rapid microbial degradation, limiting its usability without stabilization.

This project develops a digital twin of the bagasse pasteurization process, transforming it from an empirical heating operation into a predictable, model-based thermal system.

The study integrates:

Experimental material characterization

Thermodynamic and heat transfer modeling

Steam–solid energy interaction analysis

Biot number validation

Computational simulation using Python and DWSIM


The goal is to understand, predict, and optimize the thermal stabilization process of wet bagasse.


---

### Objectives

Experimentally determine thermophysical properties of wet bagasse

Develop a transient heat transfer model for pasteurization

Analyze steam–bagasse energy interaction using enthalpy balances

Validate lumped capacitance assumption using Biot number analysis

Simulate system behavior using Python and DWSIM

Estimate optimal operating conditions for industrial-scale operation



---

### Material Characterization

The following properties were experimentally determined:

Property	Value

Thermal Conductivity	0.2344 W/m·K
Specific Heat Capacity	2510.1 J/kg·K
Bulk Density	330.6 kg/m³
Moisture Content (wet basis)	75%


These properties define bagasse as a high-moisture, low-conductivity porous thermal medium, strongly influencing its heating behavior.


---

### Governing Model

The transient thermal behavior of bagasse is described using a lumped energy balance, refer technical paper for the governing equation.

This formulation treats the system as a flow-driven thermal reactor, where heating is controlled by steam energy input.


---

### Steam Modeling Approach

Steam is modeled as the primary energy carrier responsible for:

Convective heat transfer

Latent heat release during condensation

Enthalpy-driven energy exchange


#### Two limiting cases were considered:

- Condensation with moisture deposition

- Condensation without deposition


These define operational bounds for realistic industrial behavior.


---

### Biot Number Analysis

To validate the lumped capacitance assumption.

### Result:

Bi ≤ 1 (conservative approach: Bi ≤ 0.01)


### Interpretation:

a. Internal conduction resistance is negligible

b. Temperature gradients inside bagasse are minimal

c. Lumped system modeling is valid



---

### Computational Implementation

The model was implemented using:

#### Python

Numerical evaluation

Parameter calculations

Sensitivity analysis

Energy balance verification


#### DWSIM

Process simulation

Steam–solid interaction modeling

Energy balance visualization

Temperature profile generation


Together, they form a digital twin simulation framework.


---

### Key Results

Parameter	Result

Pasteurization Temperature	75°C
Estimated Processing Time	~5 hours
Steam Flow Rate	~10 kg/hr
Batch Capacity	~1000 kg


Key Insight:

Process performance is highly sensitive to steam flow rate and enthalpy conditions, confirming the importance of dynamic modeling over fixed-time assumptions.


---

### Batch Design Considerations

The proposed batch capacity was validated based on:

Thermal penetration limits

Biot number analysis

Steam energy availability

Bulk density and heat capacity

Transient heating response


This ensures physically realistic scaling for industrial application.


---

### Engineering Significance

This project demonstrates the transition from:

Empirical heating practice → Predictive thermal system design

It highlights how agricultural waste can be transformed into a modeled, controllable, and optimizable engineering system using:

Thermodynamics

Heat transfer

Process simulation

Computational modeling



---

### Tools & Technologies

Python (IronPython)

DWSIM Process Simulator

Thermodynamic property analysis(Steam Tables Property Package)

Heat transfer modeling

Energy balance formulation

Biot number analysis



---

### Repository Structure

├── README.md
├── /python-model/
│   ├── energy_balance.py
│   ├── parameter_analysis.py
│   └── sensitivity_analysis.py
├── /dwsim/
│   ├── bagasse_pasteurization.xml
├── /docs/
│   ├── methodology.pdf
│   ├── results.pdf
└── /figures/
    ├── process_flow_diagram.png
    ├── temperature_profile.png


---

### Future Work

Dynamic (time-dependent) steam modeling

CFD-based heat penetration analysis

Optimization of steam consumption

Scale-up to continuous processing systems

Integration into full biomass processing digital twin



---

### Authors

Blaise Atambo
BSc Chemical Engineering
Dedan Kimathi University of Technology

Collaborator: Moses Chai
Supervisor: Dr. Godfrey Gakingo 

---

### Acknowledgment

This work was inspired by real-world challenges in biomass utilization and industrial process systems engineering, aiming to bridge experimental characterization with computational modeling.


---

### Key Insight

> Engineering value is created when observation is transformed into prediction.

