# AGNIS

## Advanced Gas Sensing Nanocomposite Integrated Sensor

AGNIS is a research project investigating the functionalisation of a commercial **MiCS-4514 metal-oxide gas sensor** using a **polyaniline-based nanocomposite coating** for multi-gas sensing.

The work combines nanocomposite synthesis, material characterisation, commercial sensor functionalisation, embedded data acquisition, and control-referenced gas-sensing evaluation.

> **Research Work — Under Review**
>
> This repository currently provides a high-level technical overview of the project. Detailed datasets, experimental artifacts, and additional research results may be released following completion of the review process and subject to applicable research and institutional guidelines.

---

## 📌 Overview

Commercial metal-oxide gas sensors provide a low-cost and robust sensing platform, but their selectivity across different gas species can be limited.

AGNIS explores whether a secondary functional coating based on **polyaniline (PANI)** and an intended silver-vanadate precursor can modify the sensing behaviour of an existing commercial sensor without redesigning the transducer.

The coated sensor was benchmarked against a nominally identical **uncoated MiCS-4514 control** under matched experimental conditions.

The study investigated four analytes:

- Carbon monoxide (CO)
- Ammonia (NH₃)
- Nitrogen dioxide (NO₂)
- Ethanol vapour

---

## 🎯 Research Objectives

The project was designed to:

1. Synthesize the intended β-AgVO₃ precursor and integrate it with PANI.
2. Characterise the resulting material using XRD, FESEM, EDS/EDAX, and FTIR.
3. Integrate the composite onto a commercial MiCS-4514 sensing platform.
4. Compare coated and uncoated sensors under controlled gas exposure.
5. Evaluate response magnitude, selectivity, and concentration dependence rather than assuming an improvement.

---

## 🏗️ System Architecture

```text
        Chemical Precursors
               │
               ▼
      Hydrothermal Synthesis
               │
               ▼
       Inorganic Precursor
               │
               ▼
    In-Situ PANI Polymerisation
               │
               ▼
       Composite Powder
               │
               ▼
      Chitosan-Based Ink
               │
               ▼
      Drop-Cast on MiCS-4514
               │
               ▼
        22–24 h Burn-In
               │
               ▼
      ┌───────────────────┐
      │     MiCS-4514     │
      │                   │
      │  RED       OX     │
      └─────┬───────┬─────┘
            │       │
            └───┬───┘
                ▼
              ESP32
                │
                ▼
       Resistance Extraction
                │
                ▼
       Gas Response Analysis
                │
                ▼
     Coated vs Uncoated Control
```

---

## 🧪 Material Synthesis

### Step 1 — Hydrothermal Precursor Synthesis

Ammonium vanadate and silver nitrate were used as precursor materials.

The synthesis involved:

- NH₄VO₃
- AgNO₃
- Deionised water
- HNO₃ pH adjustment
- Teflon-lined autoclave
- Hydrothermal treatment at approximately 140 °C

The synthesis was intended to produce β-AgVO₃.

### Step 2 — In-Situ PANI Polymerisation

The hydrothermal product was dispersed in 1 M HCl followed by oxidative polymerisation of aniline using ammonium persulfate (APS).

The resulting material was formulated as a chitosan-stabilised coating ink.

### Step 3 — Sensor Integration

The coating was deposited onto the sensing window of a commercial MiCS-4514 using a controlled drop-casting process.

The coated sensor was subsequently dried and electrically conditioned before gas testing.

---

## 🔬 Material Characterisation

The composite was characterised using multiple complementary techniques.

| Technique | Purpose |
|---|---|
| XRD | Crystal phase identification |
| FESEM | Surface morphology |
| EDS/EDAX | Elemental composition and mapping |
| FTIR | Chemical bonding and PANI identification |

The FESEM analysis showed granular, cauliflower-like PANI agglomerates with occasional faceted crystallites.

FTIR confirmed the formation of protonated, conducting PANI through characteristic quinoid, benzenoid, C–N, and C–H bands.

### ⚠️ Important Phase-Identification Finding

A significant finding of the study was that the crystalline inorganic phase obtained in this batch could not be verified as β-AgVO₃.

XRD indexed the observed crystalline reflections to face-centred-cubic AgCl, while EDS detected chlorine and did not detect vanadium above its measurement detection limit.

The study identifies the HCl polymerisation step as a probable source of chloride incorporation and therefore an important synthesis variable requiring revision.

Accordingly, **the project does not claim verified β-AgVO₃ formation or superior sensing performance for the current batch.**

---

## 🛰️ Sensor Platform

The sensing platform uses the commercially available MiCS-4514 dual-element metal-oxide sensor.

The two sensing elements provide:

- **RED** — reducing-gas response
- **OX** — oxidising-gas response

An ESP32 was used for sensor biasing, analogue acquisition, and data logging.

Measurements were recorded at approximately 2-second intervals.

---

## 📊 Gas-Sensing Evaluation

Testing was performed at approximately:

- 50% relative humidity
- 22–28 °C

The investigated concentration ranges were:

| Gas | Concentration Range |
|---|---|
| CO | 0.5–13 ppm |
| NH₃ | 0.01–2 ppm |
| NO₂ | 0.05–1 ppm |
| Ethanol | 0.01–0.3 ppm |

The coated device was evaluated alongside a nominally identical uncoated MiCS-4514 control.

### Response Definition

Sensor responses were calculated relative to a clean-air baseline.

For the RED element:

```
S_RED = (R0 - Rs) / R0
```

For the OX element:

```
S_OX = (Rs - R0) / R0
```

This sign convention allows the physically expected response direction to be represented as positive.

---

## 🔑 Key Findings

**CO**
The coated device showed a monotonic response to increasing CO concentration. However, the coating did not improve CO response magnitude compared with the uncoated control.

**NO₂**
The coated OX element exhibited a substantially larger NO₂ response than the uncoated control. However, the study explicitly treats the fitted concentration-response exponent as a curve-fitting artefact because of the narrow and unreplicated concentration window. Therefore, this result should not be interpreted as definitive evidence of enhanced sensing performance.

**Ethanol**
Ethanol produced monotonic responses with different response directions on the coated and uncoated OX elements.

**Overall Finding**

The primary outcome of the current work is not a claim of superior sensing performance. Instead, the study establishes:

- A reproducible synthesis-to-integration workflow
- Commercial sensor functionalisation
- Control-referenced multi-gas measurements
- Material characterisation methodology
- Identification of an important chloride-related synthesis issue
- A basis for improving the next experimental iteration

---

## 🔁 Experimental Workflow

```text
Material Preparation
        ↓
Hydrothermal Synthesis
        ↓
PANI Polymerisation
        ↓
Material Characterisation
        ↓
Coating Ink Preparation
        ↓
MiCS-4514 Functionalisation
        ↓
ESP32 Integration
        ↓
Sensor Burn-In
        ↓
Controlled Gas Exposure
        ↓
Resistance Acquisition
        ↓
Response Normalisation
        ↓
Coated vs Uncoated Analysis
```

---

## 🖥️ Embedded System

The ESP32-based readout system was used to:

- Supply the sensor heater network
- Acquire RED sensing-element measurements
- Acquire OX sensing-element measurements
- Convert analogue measurements into sensing resistance
- Log gas-response data
- Maintain the same acquisition configuration for coated and uncoated devices

This provides an embedded bridge between the material-level sensing experiment and quantitative data analysis.

---

## 💻 Technology Stack

**Materials & Sensor**
- Polyaniline (PANI)
- Intended β-AgVO₃ precursor
- MiCS-4514
- Chitosan
- AgNO₃
- NH₄VO₃
- Aniline
- APS

**Characterisation**
- XRD
- FESEM
- EDS/EDAX
- FTIR

**Embedded Systems**
- ESP32
- Analog sensor acquisition
- Resistance-based gas sensing
- Data logging

**Data Analysis**
- Python
- Numerical analysis
- Concentration-response modelling
- Control-referenced comparison

---

## 🧩 Engineering Highlights

This project demonstrates experience across multiple layers of an experimental sensing system:

- Nanocomposite material preparation
- Sensor functionalisation
- Semiconductor gas-sensing platforms
- Embedded data acquisition
- Sensor calibration and baseline measurement
- Gas-response characterisation
- Experimental control design
- Quantitative data analysis
- Material phase identification
- Hardware–software integration

---

## ⚠️ Limitations

The current study has several important experimental limitations.

**Device Replication**
Only one coated device and one uncoated control were tested, so device-to-device reproducibility cannot yet be established.

**Material Characterisation**
TEM and BET measurements were not performed, limiting conclusions regarding nanoscale interfaces and surface area.

**Experimental Repetition**
Gas exposure concentrations were not repeated, and the staircase protocol did not include complete gas-off/purge segments, preventing rigorous response/recovery-time analysis.

**Humidity**
Testing was performed at a single relative humidity condition, so humidity cross-sensitivity remains unresolved.

**Coating Effects**
A chitosan-only control was not evaluated, so the individual contribution of the binder cannot be isolated.

**Material Composition**
The PANI-to-inorganic-phase loading was not independently quantified.

---

## 🔮 Future Work

Future iterations can focus on:

- Revising the polymerisation chemistry to avoid chloride-related phase conversion
- Characterising the hydrothermal product before polymerisation
- Re-quantifying EDS with explicit Ag analysis
- Fabricating multiple coated and uncoated devices
- Repeating gas-exposure cycles
- Adding gas-off/purge intervals
- Evaluating humidity dependence
- Adding chitosan-only controls
- Performing TEM and BET analysis
- Investigating long-term stability and sensor drift
- Testing mixed-gas environments

The most informative next material-level experiment identified by the study is characterisation of the bare hydrothermal product before exposure to HCl, which would help distinguish whether the intended vanadate failed to form initially or was transformed during polymerisation.

---

## 📄 Research Status

**Status: Under Review / Experimental Research**

This repository presents the current research methodology and high-level findings.

Experimental conclusions are intentionally reported conservatively, particularly regarding material phase identity and sensing enhancement.

---

## 👥 Authors

**Apurva Kumar**
Department of Electrical and Electronics Engineering
Dr. Vishwanath Karad MIT World Peace University, Pune

**Gayatri Kale**
Department of Electrical and Electronics Engineering
Dr. Vishwanath Karad MIT World Peace University, Pune

**Kiran Kokate**
Department of Chemistry, School of Science and Environmental Studies
Dr. Vishwanath Karad MIT World Peace University, Pune

**Deepa Nath**
Department of Electrical and Electronics Engineering
Dr. Vishwanath Karad MIT World Peace University, Pune

---

## ⚠️ Disclaimer

This project is an experimental research prototype for gas sensing and sensor functionalisation.

The reported results should not be interpreted as evidence of a production-ready gas detection system. Further device replication, calibration, environmental testing, and long-term validation are required before practical deployment.

---

## 🏷️ Keywords

`Gas Sensor` `Gas Sensing` `PANI` `Polyaniline` `MiCS-4514` `ESP32` `Nanocomposite` `Chemiresistor` `NO2` `NH3` `CO` `Ethanol` `Embedded Systems` `Material Characterisation` `XRD` `FESEM` `EDS` `FTIR` `Sensor Functionalisation`
