# UC Portal Signal AP Statistics Analysis

This project studies whether informal UC applicant portal signals are statistically aligned with applicant profile strength and with an AP Statistics-style expected-admission model.

The project does not claim that portal behavior causes admission outcomes or that any portal state is an official decision. The purpose is narrower: quantify whether observed portal states behave like noisy admission signals in this self-reported sample.

## Project Structure

```text
.
|-- data/
|   |-- processed/
|   |   |-- uc_application_data_cleaned.csv
|   |   `-- uc_applications_ai_major_categories.csv
|   `-- raw_public_gpa_bins/
|       |-- uc_berkeley_2025_applicant_gpa_bins.csv
|       |-- uc_irvine_2025_applicant_gpa_bins.csv
|       `-- uc_san_diego_2025_applicant_gpa_bins.csv
|-- outputs/
|   |-- figures/
|   |   |-- gpa_distributions_micro_bins.png
|   |   |-- piq_ec_self_rating_distributions.png
|   |   `-- top_major_categories_by_campus.png
|   |-- logs/
|   |   `-- analysis_results.txt
|   `-- scored_probabilities/
|       |-- uc_berkeley_apstats_expected_probabilities.csv
|       |-- uc_irvine_apstats_expected_probabilities.csv
|       `-- uc_san_diego_apstats_expected_probabilities.csv
|-- src/
|   |-- 01_clean_application_data.py
|   |-- 02_categorize_majors.py
|   |-- 03_describe_sample.py
|   |-- 04_compare_portal_signals.py
|   `-- 05_apstats_expected_admits.py
`-- README.md
```

File naming convention:

- `data/raw_public_gpa_bins/`: external public GPA-bin inputs used by the AP Stats model.
- `data/processed/`: cleaned applicant-level sample data.
- `src/`: numbered scripts in execution order.
- `outputs/figures/`: generated visual summaries.
- `outputs/scored_probabilities/`: applicant-level expected probabilities from the AP Stats model.
- `outputs/logs/`: captured text output from analysis runs.

## Research Questions

1. Do applicants with a favorable portal state have stronger GPA, PIQ, or EC profiles than applicants with an unfavorable portal state?
2. If admissions are modeled using public GPA-bin distributions and major-category admit-rate assumptions, how close are expected admits to the observed favorable portal counts?
3. For UCI, how accurate is the login-related portal signal in a manually checked outcome subset?

## Data Sources

### Applicant Sample

Primary cleaned file:

- `data/processed/uc_applications_ai_major_categories.csv`

Sample summary:

| Variable | n | Mean | Median | SD | Min | Max |
|---|---:|---:|---:|---:|---:|---:|
| UC unweighted GPA | 277 | 3.865 | 3.940 | 0.287 | 0.58 | 4.20 |
| UC weighted GPA | 272 | 4.352 | 4.400 | 0.448 | 0.61 | 5.35 |
| UC weighted capped GPA | 268 | 4.118 | 4.180 | 0.348 | 0.61 | 4.90 |
| PIQ self-rating | 277 | 7.307 | 8.000 | 1.529 | 1 | 10 |
| EC self-rating | 277 | 7.130 | 7.000 | 1.670 | 1 | 10 |

The sample is self-reported. It is not a random sample of all UC applicants.

### Public GPA-Bin Inputs

The AP Stats model uses 2025 public applicant GPA-bin files:

- `data/raw_public_gpa_bins/uc_berkeley_2025_applicant_gpa_bins.csv`
- `data/raw_public_gpa_bins/uc_san_diego_2025_applicant_gpa_bins.csv`
- `data/raw_public_gpa_bins/uc_irvine_2025_applicant_gpa_bins.csv`

These files contain grouped HS weighted capped GPA counts. Since the data are binned, the model approximates the underlying applicant GPA distribution rather than observing it directly.

## Portal Signal Definitions

| Campus | Portal field | Favorable signal | Unfavorable signal | Excluded from comparison |
|---|---|---:|---:|---:|
| UC Berkeley | `Berkeley id or email?` | `Id` | `Email` | `Didn't Apply` |
| UC San Diego | `Is your UCSD #3 prestige banner there?` | `No` | `Yes` | `Didn't Apply` |
| UC Irvine | `Can you log in to the UCI link?` | `Yes` | `No` | `Didn't Apply` |

Observed counts:

| Campus | Favorable n | Unfavorable n | Did not apply n |
|---|---:|---:|---:|
| UC Berkeley | 176 | 67 | 34 |
| UC San Diego | 142 | 106 | 29 |
| UC Irvine | 116 | 86 | 75 |

These definitions reflect the working hypotheses used in the analysis. They should not be interpreted as official UC definitions.

## Methodology

### 1. Descriptive Sample Analysis

Script:

```bash
python src/03_describe_sample.py
```

This script summarizes GPA, PIQ, EC, and major-category distributions. It also generates:

- `outputs/figures/gpa_distributions_micro_bins.png`
- `outputs/figures/piq_ec_self_rating_distributions.png`
- `outputs/figures/top_major_categories_by_campus.png`

Purpose:

- Establish whether the sample is academically strong or skewed.
- Identify major-category concentration.
- Provide context before interpreting portal-signal comparisons.

### 2. Favorable vs Unfavorable Portal Group Comparison

Script:

```bash
python src/04_compare_portal_signals.py
```

For each campus, the script compares favorable and unfavorable portal groups on:

- UC unweighted GPA
- UC weighted GPA
- PIQ self-rating
- EC self-rating

Reported statistics:

- Mean difference: `mean(favorable) - mean(unfavorable)`
- Welch two-sample t-test p-value
- Cohen's d
- Simulation-based probability that the favorable-group mean is larger
- Propensity-score-matched GPA difference using PIQ and EC as matching covariates

Interpretation rules:

- A positive GPA difference means the favorable portal group has higher average GPA.
- A low p-value means the observed mean difference is less compatible with a zero-difference null model.
- Cohen's d measures standardized effect size; values around 0.2 are small, around 0.5 are moderate.
- The simulation probability is descriptive and depends on normal approximation of mean uncertainty.
- PSM adjustment is not causal; it only checks whether GPA differences persist after balancing on two self-rated non-GPA variables.

### 3. AP Stats Expected-Admit Model

Script:

```bash
python src/05_apstats_expected_admits.py
```

The model estimates applicant-level admission probabilities using:

```text
P(Admit | GPA) = P(Admit) * P(GPA | Admit) / P(GPA)
```

Model components:

- `P(Admit)` is a broad campus-major-category admit-rate assumption.
- `P(GPA | Admit)` is approximated as a normal distribution inferred from admitted-student GPA Q1 and Q3.
- `P(GPA)` is approximated as a normal distribution fitted from public applicant GPA bins.
- Applicant GPA is represented by UC weighted capped GPA.
- Individual probabilities are capped at 0.85 because real admissions are holistic and should not be modeled as certain from GPA alone.

The model then sums applicant-level probabilities:

```text
Expected admits = sum(P_i(Admit | GPA_i, major_category_i))
```

This produces an expected-admit count for the sample, which is compared with the observed favorable portal count.

Important caveat:

The AP Stats model is a structured approximation, not a production admissions model. It intentionally uses limited public information so that the reasoning is transparent and reproducible.

## Results

### Favorable vs Unfavorable Portal Groups

| Campus | Metric | Favorable mean | Unfavorable mean | Difference | p-value | Cohen's d | P(favorable > unfavorable) | PSM diff |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| UC Berkeley | GPA_UW | 3.899 | 3.828 | +0.071 | 0.1880 | 0.267 | 90.8% | +0.101 |
| UC Berkeley | GPA_W | 4.426 | 4.241 | +0.185 | 0.0139 | 0.440 | 99.4% | +0.094 |
| UC Berkeley | PIQ | 7.449 | 7.493 | -0.044 | 0.8106 | -0.032 | 40.6% | N/A |
| UC Berkeley | EC | 7.318 | 7.239 | +0.079 | 0.7264 | 0.050 | 63.8% | N/A |
| UC San Diego | GPA_UW | 3.913 | 3.812 | +0.102 | 0.0143 | 0.354 | 99.3% | +0.063 |
| UC San Diego | GPA_W | 4.426 | 4.283 | +0.142 | 0.0201 | 0.321 | 99.1% | +0.133 |
| UC San Diego | PIQ | 7.359 | 7.368 | -0.009 | 0.9631 | -0.006 | 48.0% | N/A |
| UC San Diego | EC | 7.282 | 7.066 | +0.216 | 0.3174 | 0.132 | 84.2% | N/A |
| UC Irvine | GPA_UW | 3.900 | 3.805 | +0.095 | 0.0587 | 0.303 | 97.1% | +0.066 |
| UC Irvine | GPA_W | 4.405 | 4.283 | +0.123 | 0.0795 | 0.263 | 96.2% | +0.099 |
| UC Irvine | PIQ | 7.405 | 7.384 | +0.021 | 0.9128 | 0.015 | 54.2% | N/A |
| UC Irvine | EC | 7.190 | 7.035 | +0.155 | 0.5157 | 0.095 | 74.0% | N/A |

Main interpretation:

- Favorable portal groups have higher average GPA across all three campuses.
- UC Berkeley and UC San Diego show statistically clearer weighted-GPA separation.
- UCI shows the same direction, but with weaker statistical evidence in this sample.
- PIQ and EC differences are small and statistically weak, which suggests the portal signal is more aligned with GPA than with self-rated qualitative strength.

### AP Stats Expected vs Observed Favorable Signals

| Campus | Applicant-pool GPA mean | Applicant-pool GPA SD | Public GPA-bin N | Valid sample n | Expected admits | Favorable portal count | Difference | Ratio |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| UC Berkeley | 3.972 | 0.432 | 118,869 | 243 | 81.14 | 176 | +94.86 | 2.17x |
| UC San Diego | 3.901 | 0.495 | 129,373 | 248 | 136.04 | 142 | +5.96 | 1.04x |
| UC Irvine | 3.872 | 0.514 | 118,252 | 202 | 121.11 | 116 | -5.11 | 0.96x |

Main interpretation:

- UC San Diego and UC Irvine favorable portal counts are close to model expectations.
- UC Berkeley has far more `Id` observations than expected admits under this model.
- Therefore, the Berkeley `Id` state may be a weaker or broader signal than the UCSD and UCI favorable states, or the model may substantially underestimate Berkeley competitiveness in this sample.

### UCI Manual Outcome Check

Manual UCI classification counts:

| Category | Meaning | Count |
|---|---|---:|
| TP | Can log in and admitted | 75 |
| FP | Can log in but rejected/waitlisted | 22 |
| FN | Cannot log in but admitted | 20 |
| TN | Cannot log in and rejected/waitlisted | 33 |

Derived metrics:

| Metric | Formula | Value |
|---|---|---:|
| Precision | TP / (TP + FP) | 77.32% |
| Recall | TP / (TP + FN) | 78.95% |
| Specificity | TN / (TN + FP) | 60.00% |
| Accuracy | (TP + TN) / total | 72.00% |

Interpretation:

- The UCI login signal is informative in the manually checked subset.
- It is not definitive: both false positives and false negatives are material.
- Precision is stronger than specificity, meaning the signal is better at supporting positive cases than ruling out non-admits.

## Meaning of the Findings

The strongest evidence is not that portal signals perfectly predict decisions. They do not. The stronger conclusion is that favorable portal states are not randomly distributed with respect to applicant strength in this sample.

The GPA pattern matters because GPA is an admissions-relevant variable and is consistently higher in favorable portal groups. The AP Stats comparison matters because it asks a different question: not whether favorable groups are stronger, but whether the count of favorable signals is plausible under a transparent expected-admission model.

UCSD and UCI are the most internally consistent cases: favorable signal counts are close to expected admits, and favorable groups have stronger GPA profiles. Berkeley is different: the `Id` count is much larger than expected admits, so it should be treated as a broader and less selective indicator unless additional validation data show otherwise.

## Limitations

1. Selection bias: the sample is self-reported and likely overrepresents applicants who are highly engaged with portal tracking.
2. Measurement error: GPA, PIQ, EC, major, portal state, and outcome labels may contain reporting mistakes.
3. Major simplification: detailed majors are reduced into broad AI-categorized groups, which loses program-level selectivity.
4. Limited covariates: the AP Stats model does not include essays, course rigor, school context, awards, residency, first-generation status, special talents, or institutional priorities.
5. Approximate public data: GPA-bin files are grouped, so applicant-pool distributions are fitted from interval midpoints rather than raw observations.
6. Normality assumption: both applicant and admit GPA distributions are approximated as normal distributions, which may not hold well near GPA ceilings.
7. Probability cap: the 0.85 cap is a modeling judgment, not an empirical UC rule.
8. Multiple comparisons: many tests are reported, so isolated p-values should not be overinterpreted.
9. Signal definition uncertainty: favorable and unfavorable portal labels are hypothesis-driven and campus-specific.
10. No causal identification: differences between portal groups do not prove that portal state causes, determines, or officially reflects an admission decision.

## Reproducibility

Required Python packages:

- `pandas`
- `numpy`
- `scipy`
- `scikit-learn`
- `matplotlib`
- `seaborn`

Run the analysis from the repository root:

```bash
python src/03_describe_sample.py
python src/04_compare_portal_signals.py
python src/05_apstats_expected_admits.py
```

Optional upstream data-preparation scripts:

```bash
python src/01_clean_application_data.py
python src/02_categorize_majors.py
```

Expected outputs:

```text
outputs/figures/gpa_distributions_micro_bins.png
outputs/figures/piq_ec_self_rating_distributions.png
outputs/figures/top_major_categories_by_campus.png
outputs/scored_probabilities/uc_berkeley_apstats_expected_probabilities.csv
outputs/scored_probabilities/uc_san_diego_apstats_expected_probabilities.csv
outputs/scored_probabilities/uc_irvine_apstats_expected_probabilities.csv
```

## Bottom Line

Favorable UC portal states are associated with stronger GPA profiles in this sample, especially for Berkeley and UCSD weighted GPA. UCSD and UCI favorable counts are close to AP Stats model expectations, while Berkeley's `Id` count is much larger than expected and should be interpreted cautiously. The evidence supports portal signals as noisy, campus-specific indicators, not as official or deterministic admission outcomes.
