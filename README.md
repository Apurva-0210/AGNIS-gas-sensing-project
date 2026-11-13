# AGNIS

## Advanced Gas Sensing Nanocomposite Integrated Sensor

AGNIS is a research project investigating the functionalisation of a commercial **MiCS-4514 metal-oxide gas sensor** using a **polyaniline-based nanocomposite coating** for multi-gas sensing.

The work combines nanocomposite synthesis, material characterisation, commercial sensor functionalisation, embedded data acquisition, and control-referenced gas-sensing evaluation.

> **Research Work: Under Review**
>
> Manuscript: *Polyaniline–Silver Metavanadate Nanocomposite Coating for Multi-Gas Detection on a Commercial Metal-Oxide Sensor Platform*, prepared for *Chemical Engineering Journal*. This repository holds the raw data, firmware, analysis code, figures and manuscript files that support it.

**Repository DOI:** to be added after the Zenodo release (see [Licence and Citation](#-licence-and-citation)).

---

## 📌 Overview

Commercial metal-oxide gas sensors provide a low-cost and robust sensing platform, but their selectivity across different gas species can be limited.

AGNIS explores whether a secondary functional coating based on **polyaniline (PANI)** and an intended silver-vanadate precursor can modify the sensing behaviour of an existing commercial sensor without redesigning the transducer.

The coated sensor was benchmarked against a nominally identical **uncoated MiCS-4514 control** under matched experimental conditions.

The study investigated four analytes:

- Carbon monoxide (CO)
- Ammonia (NH₃)
- Nitrogen dioxide (NO₂)
- Volatile organic compound (VOC) vapour (logged as `ETH` in the raw files)

---

## 🎯 Research Objectives

The project was designed to:

1. Synthesise the intended β-AgVO₃ precursor hydrothermally and integrate it with PANI.
2. Characterise the precursor and the composite using XRD, FESEM and FTIR.
3. Integrate the composite onto a commercial MiCS-4514 sensing platform.
4. Compare coated and uncoated sensors under controlled gas exposure.
5. Evaluate response magnitude, selectivity and concentration dependence against the uncoated control rather than assuming an improvement.

---

## 🏗️ System Architecture

```text
        Chemical Precursors (NH4VO3, AgNO3)
               │
               ▼
      Hydrothermal Synthesis (140 °C)
               │
               ▼
       Inorganic Precursor
               │
               ▼
    In-Situ PANI Polymerisation (1 M HCl)
               │
               ▼
       Composite Powder
               │
               ▼
      Chitosan-Based Ink
               │
               ▼
      Drop-Cast on MiCS-4514 (1 µL)
               │
               ▼
        24–28 h Burn-In at 5 V DC
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

### Step 1: Hydrothermal Precursor Synthesis

Ammonium vanadate and silver nitrate were used as precursor materials.

The synthesis involved:

- NH₄VO₃
- AgNO₃
- Deionised water, pH about 4.5 adjusted with HNO₃
- Sonication for 10 min
- Teflon-lined autoclave
- Hydrothermal treatment at approximately 140 °C for 12–18 h
- Centrifugation, washing and drying at 60 °C

The synthesis was intended to produce β-AgVO₃.

### Step 2: In-Situ PANI Polymerisation

The hydrothermal product was dispersed in 1 M HCl at 0–5 °C, followed by oxidative polymerisation of aniline using ammonium persulfate (APS) for 3–4 h. The product was washed and dried at 50 °C.

### Step 3: Ink Formulation and Sensor Integration

The composite (5 mg) was dispersed in an ethanol–water mixture containing 1 % chitosan and sonicated for 20 min to give a chitosan-stabilised coating ink.

One microlitre of the ink was deposited onto the sensing window of a commercial MiCS-4514 by drop-casting. The coated sensor was dried at 50–60 °C and electrically conditioned (burn-in of 24–28 h at 5 V DC) before gas testing.

---

## 🔬 Material Characterisation

The composite was characterised using complementary techniques.

| Technique | Purpose |
|---|---|
| XRD | Crystal phase identification |
| FESEM | Particle morphology |
| FTIR | Chemical bonding; identification of PANI and of the precursor bands |

FESEM showed rod-like particles for the precursor and granular, agglomerated PANI for the composite.

FTIR confirmed the formation of protonated, conducting PANI through the quinoid and benzenoid bands (1571 and 1472 cm⁻¹) and the C–N and C–H bands. The precursor showed bands at 926, 908, 761 and 625 cm⁻¹.

### ⚠️ Important Phase-Identification Finding

A significant finding of the study was that the crystalline inorganic phase in the composite prepared in HCl is not β-AgVO₃.

XRD indexes the observed crystalline reflections of the composite to face-centred-cubic **AgCl** (lattice parameter 5.5544 ± 0.0003 Å), and no vanadate reflection or infrared band is found in it. The silver of the vanadate most likely precipitates as AgCl in the 1 M HCl polymerisation step, which makes that step an important synthesis variable to revise.

Accordingly, the name PANI–AgVO₃ is kept for the intended material and for its precursor, and **the project does not claim verified β-AgVO₃ in the composite**. Indexing the full precursor pattern and testing other acid media are the next steps.

---

## 🛰️ Sensor Platform

The sensing platform uses the commercially available MiCS-4514 dual-element metal-oxide sensor.

The two sensing elements provide:

- **RED**: reducing-gas response
- **OX**: oxidising-gas response

An ESP32 was used for sensor biasing, analogue acquisition and data logging.

Measurements were recorded at approximately 2-second intervals.

---

## 📊 Gas-Sensing Evaluation

Testing was performed at approximately:

- 50 % relative humidity (nominal; the value held in the logger)
- 22–28 °C (operator-entered chamber temperature)

The investigated concentration ranges were:

| Gas | Concentration range | Main element |
|---|---|---|
| CO | 0.5–13 ppm | RED |
| NH₃ | 0.01–2 ppm | OX |
| NO₂ | 0.05–1 ppm | OX |
| VOC vapour | 0.01–0.3 ppm | RED |

The coated device was evaluated alongside a nominally identical uncoated MiCS-4514 control.

### Response Definition

Responses use the data-sheet sensitivity factors, each referred to the clean-air baseline R0 of its own run.

For the RED element:

```
S_RED = R0 / Rs
```

For the OX element:

```
S_OX = Rs / R0
```

Both factors rise above 1 for the physically expected response direction. Enhancement of the coating is E = (S_coated − S_uncoated) / S_uncoated × 100 %, and the enhancement factor is EF = S_coated / S_uncoated.

(The sketch in `firmware/` carries an earlier on-board definition, S = (R0 − Rs)/R0, with fixed R0 constants. The analysis does not use it.)

---

## 🔑 Key Findings

| Gas | Coated S<sub>max</sub> | Uncoated S<sub>max</sub> | Result against the uncoated control |
|---|---|---|---|
| NO₂ | 44.46 at 1 ppm | 1.06 (0.93 at 1 ppm) | Threshold-like onset above 0.4 ppm; EF = 47.8 at 1 ppm; fit S = 44.06 C<sup>7.457</sup>, R² = 0.993 |
| VOC vapour | 5.31 at 0.3 ppm | 4.67 | Higher at all 9 concentrations (+11 to +47 %) |
| NH₃ | 1.79 at 0.8 ppm | 1.66 | Higher from 0.5 to 2 ppm (+6 to +40 %); indicative |
| CO | 2.32 at 13 ppm | 2.92 | Higher up to 7 ppm (+3 to +9 %); lower from 8.5 to 13 ppm |

**CO.** The coated device showed a monotonic response to increasing CO concentration. The gain over the uncoated control is small (3–9 % up to 7 ppm) and reverses at 8.5–13 ppm, where the uncoated sensor is higher by 20–22 %.

**NO₂.** The coated OX element showed a much larger NO₂ response than the uncoated control, which stayed near S = 1 over 0.05–1 ppm. The fitted exponent (7.457) describes one run over a narrow window, so replicate devices are needed before it is used quantitatively.

**VOC vapour.** The coated RED element responded more strongly than the uncoated one at every concentration. In the logged data the OX element behaved differently on the two sensors: its resistance rose with concentration on the coated sensor and fell on the uncoated one.

**NH₃.** The coated sensor was higher from 0.5 to 2 ppm and lower below 0.5 ppm (−12 to −19 %). The result is indicative because the uncoated OX baseline in that run was unusually low (see Limitations below).

**Selectivity.** The NO₂ response of the coated sensor is at least eight times larger than its response to each of the other three gases within the tested windows.

**Overall.** The work establishes:

- A reproducible synthesis-to-integration workflow
- Commercial sensor functionalisation
- Control-referenced multi-gas measurements
- Material characterisation methodology
- Identification of AgCl as the crystalline phase formed in the acid step, an important synthesis issue
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

This provides an embedded bridge between the material-level sensing experiment and quantitative data analysis. Settings are listed under "Firmware and Measurement Set-up" below.

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
- FTIR

**Embedded Systems**
- ESP32
- Analogue sensor acquisition
- Resistance-based gas sensing
- Data logging

**Data Analysis**
- Python (NumPy, SciPy, Matplotlib, Pillow)
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

The current study has several experimental limitations. They are stated so that the files are read correctly.

**Device Replication.** Only one coated device and one uncoated control were tested, and each gas was run once on each, so device-to-device reproducibility cannot yet be established.

**Material Characterisation.** TEM and surface-area measurements were not performed, which limits conclusions on nanoscale interfaces. The Ag:V and Ag:Cl ratios and the PANI-to-inorganic loading were not independently quantified.

**Experimental Repetition.** Gas exposure concentrations were not repeated, and the staircase protocol did not include complete gas-off or purge segments, which prevents a rigorous response and recovery-time analysis.

**Humidity and Temperature.** Testing was performed at a single nominal relative humidity (50 %, value held in the logger), and temperature was entered by the operator, so humidity cross-sensitivity remains unresolved.

**Coating Effects.** A chitosan-only control was not evaluated, so the individual contribution of the binder cannot be isolated.

**NH₃ Comparison.** The uncoated OX baseline in the NH₃ run (88 Ω) is far below its baselines in the NO₂ and VOC runs (3.8–4.4 kΩ) and close to the coated values, so the NH₃ enhancement is indicative. The zero-gas segments of that run are short.

**Layer Power.** With the 3.3 V bias and the 220 Ω load, the OX element dissipates about 11–12 mW at the coated baseline (107–373 Ω), above the 8 mW rating of the data sheet. The power falls as the resistance rises during NO₂ exposure.

**Data Files.** In `CO_UNCOATED_Elsevier_Clean.csv` the OX channel records ADC = 0 throughout. The `Rs_OX_ohm` value of 72,380 Ω and the OX ratio columns of that file are clamp artefacts of the zero counts and carry no information. CO is analysed from the RED element, so no result uses them.

---

## 🔮 Future Work

Future iterations can focus on:

- Revising the polymerisation chemistry to avoid chloride-related phase conversion
- Characterising the hydrothermal product before polymerisation
- Indexing the full precursor pattern and adding elemental analysis (for example ICP-OES)
- Fabricating multiple coated and uncoated devices
- Repeating gas-exposure cycles
- Adding gas-off or purge intervals
- Evaluating humidity dependence
- Adding chitosan-only controls
- Performing TEM and surface-area analysis
- Investigating long-term stability and sensor drift
- Testing mixed-gas environments

The most informative next material-level experiment identified by the study is characterisation of the bare hydrothermal product before exposure to HCl, which would help distinguish whether the intended vanadate failed to form initially or was transformed during polymerisation.

---

## 📄 Research Status

**Status: Under Review / Experimental Research**

This repository presents the research methodology, the raw data and the findings of the manuscript. Experimental conclusions are reported with their limits, particularly regarding material phase identity and the size of the sensing enhancement.

---

## 📁 Repository Contents

| Path | Content |
|---|---|
| `data/sensing/clean_csv/` | Eight logged runs: CO, NH₃, NO₂ and VOC vapour, each on the coated and the uncoated sensor |
| `data/sensing/derived/` | Step means, fits, enhancement and selectivity tables: `results.json`, `step_means_all_gases.csv`, `FitResults_Elsevier.csv`, `EnhancementResults_Elsevier.csv`, `SelectivityResults_Elsevier.csv`, and a combined `.xlsx` |
| `data/xrd/` | XRD of AgVO3 (precursor) and PA-HCl (composite): `.xrdml`, `.rd` and `.csv` |
| `data/ftir/` | FTIR spectra of AgVO3 and PA-HCl (text files) |
| `data/fesem/` | FESEM images and instrument headers for AgVO3 and PA-HCl (one sub-folder each) |
| `firmware/` | ESP32 logger and calibration-helper sketch `mics4514_logger_calibration_helper.ino` |
| `code/` | Python scripts that reproduce the derived tables and all data-driven figures |
| `figures/` | Manuscript figures `Figure_1` to `Figure_11`, the graphical abstract, and the individual figure files written by the scripts |
| `manuscript/` | Final submission set: `main.tex`, `refs.bib`, `Manuscript.pdf`, `Figures/` (Figure_1 to Figure_11), `Tables/` (Table_1 to Table_8 as `.tex` and `.pdf`), `Cover_Letter.docx`, `Highlights.docx`, `Graphical_Abstract.png` |
| `CITATION.cff` | Citation metadata |

### Sample names

- **AgVO3**: precursor prepared by the hydrothermal route.
- **PA-HCl**: polyaniline–AgVO₃ composite prepared in hydrochloric acid and used as the sensor coating.
- **COATED / UNCOATED**: MiCS-4514 with and without the PA-HCl coating (chitosan binder).

---

## 🗂️ Sensing Data: Column Dictionary and Definitions

| Column | Meaning |
|---|---|
| `time_s` | Logger time stamp, s (interval about 2 s) |
| `sensor` | `COATED` or `UNCOATED` |
| `gas` | Label written by the logger. `ETH` marks the runs reported in the paper as VOC vapour |
| `cert_ppm` | Certified concentration set point, ppm (0 = clean air) |
| `temp_C`, `hum_pct` | Operator-entered chamber temperature (°C) and humidity (%). Humidity is the nominal 50 in every row; temperature has 1–5 distinct values per run |
| `adc_red`, `adc_ox` | Raw 12-bit ADC counts (0–4095) of the RED and OX channels |
| `Rs_RED_ohm`, `Rs_OX_ohm` | Sensing resistance, R<sub>s</sub> = R<sub>L</sub> (4095/ADC − 1) |
| `R0_RED_clean_air_ohm`, `R0_OX_clean_air_ohm` | Clean-air baseline of the same run |
| `Rs_R0_RED`, `Rs_R0_OX` | R<sub>s</sub> / R0 |
| `Sensitivity_RED_SGX`, `Sensitivity_OX_SGX` | S<sub>RED</sub> = R0/R<sub>s</sub>, S<sub>OX</sub> = R<sub>s</sub>/R0 |
| `Ratio_*`, `S_RED`, `S_OX` | Earlier logger-side ratios kept for completeness; not used in the paper |

Definitions used in the paper:

- Main element per gas: OX for NO₂ and NH₃, RED for VOC vapour and CO.
- Step values are the mean of S over each concentration step (clean-air segments excluded); standard deviations are in the derived tables.
- Enhancement E = (S<sub>coated</sub> − S<sub>uncoated</sub>) / S<sub>uncoated</sub> × 100 %; enhancement factor EF = S<sub>coated</sub> / S<sub>uncoated</sub>.
- Calibration: power law S = A·C<sup>B</sup> and quadratic fits over the step means.

---

## 🔁 Reproducing the Results

Python 3.9 or later is enough.

```bash
pip install numpy scipy matplotlib pillow
python code/analyse_sensing.py                  # data/sensing/derived/results.json and step_means_all_gases.csv
python code/make_figures.py                     # sensing figures and the graphical abstract -> figures/
python code/make_characterisation_figures.py    # XRD, FTIR (vector) and FESEM panel from the raw files -> figures/
python code/make_schematics.py                  # synthesis and mechanism schematics (vector) -> figures/
```

Run the commands from the repository root. The scripts read only the files in `data/`.

To compile the manuscript, open the `manuscript/` folder in a LaTeX editor (for example Overleaf) with `main.tex` as the main file. It needs the `elsarticle` class, which Overleaf and TeX Live provide.

### Figure provenance

- Figures 1 and 11 (synthesis route and sensing mechanism) are vector redrawings, made with `code/make_schematics.py`, of draft schematics first produced with Google Gemini.
- Figure 2 (experimental set-up) is a vector block diagram.
- Figures 3 to 5 (XRD, FESEM, FTIR) are produced from the files in `data/xrd`, `data/fesem` and `data/ftir`. The FESEM panel is built at the native 768-pixel width of the instrument exports.
- Figures 6 to 10 are produced from the sensing CSV files.

---

## 🖥️ Firmware and Measurement Set-up

`firmware/mics4514_logger_calibration_helper.ino` is the ESP32 sketch used with the sensors.

- Supply: 3.3 V divider bias; 12-bit ADC (4095 counts) with 11 dB attenuation.
- Load resistors: 100 kΩ (RED element) and 220 Ω (OX element).
- Logging: 2 s interval after a 3 min warm-up.
- The certified concentration, temperature and humidity are typed in by the operator (commands `P`, `T`, `H`) and are written to each logged line. The humidity field defaults to 50.0 %.
- R<sub>s</sub> = R<sub>L</sub> (4095/ADC − 1) reproduces the `Rs_*_ohm` columns from the raw `adc_*` counts.
- The sketch carries fixed R0 constants and a different on-board ratio definition. The analysis does not use them: R0 is recomputed from the clean-air segment of each run.
- The start-up banner prints "GPIO 27 = NOX", while the code reads pin 14 (`NOX_PIN`).

Measurement conditions: MiCS-4514 dual-element sensor read by an ESP32 board; 5 V DC heater supply; burn-in of 24–28 h at 5 V DC before testing; nominal 50 % relative humidity; chamber temperature 22–28 °C (operator-entered). Each gas was run once on each sensor.

The manufacturer's data sheet is third-party material and is not redistributed here.

---

## 📜 Licence and Citation

Suggested licence: CC BY 4.0 for data and figures, MIT for code. Confirm the choice before the release and add a `LICENSE` file (GitHub's "Add file → Create new file → LICENSE" offers templates).

To obtain a DOI, link this repository to [Zenodo](https://zenodo.org), create a GitHub release, and Zenodo will mint the DOI. Then add the DOI here and in the Data Availability statement of the paper.

Suggested citation until the DOI exists:

> Kale, G., Kumar, A., Kokate, K., Nath, D. *Data, code and firmware for the polyaniline–silver metavanadate nanocomposite coating on a MiCS-4514 sensor* (GitHub repository), 2026.

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

**Deepa Nath** (corresponding author, deepa.nath@mitwpu.edu.in)
Department of Electrical and Electronics Engineering
Dr. Vishwanath Karad MIT World Peace University, Pune

---

## 🙏 Acknowledgements

The authors thank the Indian Institute of Tropical Meteorology (IITM), Pune, the Centre for Materials for Electronics Technology (C-MET), Pune, and the Central Research Laboratory, MIT World Peace University, Pune, for providing access to their facilities. This work received no specific grant from funding agencies in the public, commercial or not-for-profit sectors.

---

## ⚠️ Disclaimer

This project is an experimental research prototype for gas sensing and sensor functionalisation.

The reported results should not be interpreted as evidence of a production-ready gas detection system. Further device replication, calibration, environmental testing, and long-term validation are required before practical deployment.

---

## 🏷️ Keywords

`Gas Sensor` `Gas Sensing` `PANI` `Polyaniline` `MiCS-4514` `ESP32` `Nanocomposite` `Chemiresistor` `NO2` `NH3` `CO` `VOC` `Embedded Systems` `Material Characterisation` `XRD` `FESEM` `FTIR` `Sensor Functionalisation`
