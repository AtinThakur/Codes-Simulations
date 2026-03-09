# ---------------------------------------
# PARAMETERS AND THEIR WEIGHTS
# ---------------------------------------
parameters = [
"Binding Energy",
"Met318 Hinge Bond",
"RMSD Stability",
"BBB Permeability",
"Molecular Weight",
"Solubility",
"hERG Toxicity",
"c-Abl Selectivity",
"Off-target Hits",
"Half-life"
]

weights = [4,2,3,5,1,1.5,-10,2.5,-2,2]

# ---------------------------------------
# NORMALIZE WEIGHTS TO SEE IMPORTANCE
# ---------------------------------------
total_weight = sum(abs(w) for w in weights)

print("Parameter Importance Based on Assigned Weights\n")

for i in range(len(parameters)):

    importance = abs(weights[i]) / total_weight * 100

    print(f"{parameters[i]:<20}  Weight = {weights[i]:<5}  Importance ≈ {importance:.1f}%")# ---------------------------------------
# THEORY USED IN THE MODEL
# ---------------------------------------
print("""
Study Reference: https://doi.org/10.1016/j.bbrc.2025.153175
Theory implemented: Weighted Multi-Parameter Drug Ranking Model

This script ranks c-Abl inhibitors using a weighted scoring approach.
Each parameter comes from common in-silico drug discovery metrics.

1. Binding Energy
   From molecular docking (AutoDock/Vina).
   Strong inhibitors usually show −11 to −12 kcal/mol.

2. Met318 Hinge Bond
   Kinase inhibitors often require a hinge interaction with Met318
   for stable binding.

3. RMSD Stability
   From molecular dynamics simulation.
   RMSD < 2 Å indicates a stable ligand-protein complex.

4. BBB Permeability
   CNS drugs must cross the blood-brain barrier.

5. Molecular Weight
   Lipinski Rule: ideal < 500 Da for good drug-likeness.

6. Solubility (LogS)
   Ideal range: −1 to −5 for good absorption.

7. hERG Toxicity
   Cardiotoxicity predictor. Positive values are penalized.

8. c-Abl Selectivity
   Higher probability indicates more specific inhibition.

9. Off-target Hits
   Fewer off-targets means fewer side effects.

10. Half-life
    Longer half-life improves drug exposure.

Each parameter is multiplied by a weight and summed to give a final score.
The drug with the highest score is ranked first.
""")

# ---------------------------------------
# DATA : parameters for each drug
# ---------------------------------------
drugs = {
    "PD180970": [-11.35,1,1.2,1,429,-3,0,0.95,2,9],
    "Ponatinib": [-10.54,1,2.3,0,532,-4,0,0.90,5,10],
    "Imatinib": [-10.10,1,2.8,0,493,-4,0,0.70,12,18],
    "Risvodetinib": [-9.97,1,3.1,0,574,-3,0,0.60,10,6],
    "Nilotinib": [-9.18,1,3.5,0,529,-5,0,0.65,11,12]
}

# Parameter order
# [Energy, Met318, RMSD, BBB, MW, LogS, hERG, Selectivity, OffTargets, HalfLife]

# ---------------------------------------
# WEIGHTS
# ---------------------------------------
weights = [4,2,3,5,1,1.5,-10,2.5,-2,2]

# ---------------------------------------
# SCORE FUNCTION
# ---------------------------------------
def score(values):

    energy,met,rmsd,bbb,mw,logs,herg,sel,off,half = values

    s = 0
    s += weights[0]*abs(energy)/12
    s += weights[1]*met
    s += weights[2]*(1-rmsd/4)
    s += weights[3]*bbb
    s += weights[4]*(1 if mw<500 else 0.5)
    s += weights[5]*(1 if -5<=logs<=-1 else 0.5)
    s += weights[6]*herg
    s += weights[7]*sel
    s += weights[8]*off
    s += weights[9]*min(1,half/8)

    return s

# ---------------------------------------
# SCORING
# ---------------------------------------
results = {drug:score(values) for drug,values in drugs.items()}

# ---------------------------------------
# RANKING
# ---------------------------------------
ranking = sorted(results.items(), key=lambda x:x[1], reverse=True)

print("\nDrug Ranking Based on 10-Parameter Model\n")

for i,(drug,sc) in enumerate(ranking,1):
    print(i, drug, "| Score:", round(sc,2))


