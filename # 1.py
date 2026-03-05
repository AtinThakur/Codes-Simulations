# Create a dictionary where each key holds a list of data
abl_data = {
    "inhibitor": ["PD180970", "Ponatinib", "Imatinib", "Risvodetinib", "Nilotinib"],
    "energy": [-11.35, -10.54, -10.10, -9.97, -9.18],  # Numbers only, no ± symbols
    "bbb_permeable": [True, False, False, False, False] # Boolean values for logic
}

# To see the energy of the lead candidate (PD180970):
print(f"Lead Candidate Energy: {abl_data['energy'][0]} kcal/mol")

# Instruction: Find the drug with the best (lowest) energy
min_energy = min(abl_data["energy"])
index = abl_data["energy"].index(min_energy)
best_drug = abl_data["inhibitor"][index]

print(f"The simulation identified {best_drug} as the most potent binder.")
# 1. THE DATA (Dictionary)
# We use 1 for 'Yes' (BBB Permeable) and 0 for 'No' to allow for math
study_data = {
    'Inhibitor': ['PD180970', 'Ponatinib', 'Imatinib', 'Risvodetinib', 'Nilotinib'],
    'Binding_Energy': [-11.35, -10.54, -10.10, -9.97, -9.18],
    'BBB_Access': [1, 0, 0, 0, 0] 
}

# 2. THE MANIPULATION (Scoring Logic)
# We calculate a 'Final Score'. 
# Formula: (Absolute Binding Energy) + (BBB Bonus)
print("--- Calculating Therapeutic Potential ---")

results = []
for i in range(len(study_data['Inhibitor'])):
    name = study_data['Inhibitor'][i]
    energy = study_data['Binding_Energy'][i]
    bbb = study_data['BBB_Access'][i]
    
    # Logic: If it can't reach the brain (BBB=0), the score stays low
    score = abs(energy) + (bbb * 5) 
    results.append((name, score))

# 3. THE INTERPRETATION (Sorting)
results.sort(key=lambda x: x[1], reverse=True)

for drug in results:
    print(f"Drug: {drug[0]:<12} | Score: {drug[1]:.2f}")
