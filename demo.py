"""
Demo Script - Shows how the compliance prediction system works
"""

import pickle
import pandas as pd

print("=" * 80)
print("COMPLIANCE PREDICTION SYSTEM - DEMO")
print("=" * 80)

# Load the model
print("\n📦 Loading trained model...")
with open('compliance_model.pkl', 'rb') as f:
    model = pickle.load(f)

with open('company_metadata.pkl', 'rb') as f:
    metadata = pickle.load(f)

with open('company_types.pkl', 'rb') as f:
    company_types = pickle.load(f)

print(f"✓ Model loaded successfully!")
print(f"✓ Total company types: {len(company_types)}")

# Demo 1: Show all company types
print("\n" + "=" * 80)
print("AVAILABLE COMPANY TYPES")
print("=" * 80)
for i, ct in enumerate(company_types, 1):
    count = len(model[ct])
    print(f"{i:2}. {ct:15} → {count:3} compliances")

# Demo 2: Show detailed compliances for a specific company type
demo_company = "BIO"  # Biomass - has 7 compliances
print("\n" + "=" * 80)
print(f"DETAILED COMPLIANCES FOR: {demo_company} (Biomass)")
print("=" * 80)

compliances = model[demo_company]
for i, comp in enumerate(compliances, 1):
    print(f"\n{i}. {comp['obligation_id']}")
    print(f"   Title: {comp['title']}")
    print(f"   Description: {comp['description'][:100]}...")
    print(f"   Regulation: {comp['regulation_name']}")
    print(f"   Type: {comp['regulation_type']}")
    print(f"   Authority: {comp['authority']}")
    print(f"   Status: {comp['mandatory']}")
    print(f"   Jurisdiction: {comp['jurisdiction']} - {comp['state']}")

# Demo 3: Show another company type
demo_company2 = "COAL"
print("\n" + "=" * 80)
print(f"DETAILED COMPLIANCES FOR: {demo_company2} (Coal)")
print("=" * 80)

compliances2 = model[demo_company2]
for i, comp in enumerate(compliances2, 1):
    print(f"\n{i}. {comp['obligation_id']}")
    print(f"   Title: {comp['title']}")
    print(f"   Description: {comp['description'][:100]}...")
    print(f"   Regulation: {comp['regulation_name']}")
    print(f"   Type: {comp['regulation_type']}")

# Demo 4: Statistics
print("\n" + "=" * 80)
print("SYSTEM STATISTICS")
print("=" * 80)

total_compliances = sum(len(comps) for comps in model.values())
avg_compliances = total_compliances / len(model)

print(f"Total Company Types: {len(model)}")
print(f"Total Compliances: {total_compliances}")
print(f"Average Compliances per Type: {avg_compliances:.2f}")

# Top 10 company types by compliance count
print("\nTop 10 Company Types by Compliance Count:")
sorted_companies = sorted(model.items(), key=lambda x: len(x[1]), reverse=True)[:10]
for i, (company, comps) in enumerate(sorted_companies, 1):
    print(f"{i:2}. {company:15} → {len(comps):3} compliances")

print("\n" + "=" * 80)
print("✨ DEMO COMPLETED!")
print("=" * 80)
print("\n💡 To use the interactive web interface:")
print("   Run: streamlit run app.py")
print("   Then open: http://localhost:8501")
print("\n" + "=" * 80)
