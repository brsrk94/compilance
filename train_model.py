"""
Compliance Prediction Model Training Script
This script trains a model to predict compliances based on company type
"""

import pandas as pd
import pickle
import re
from sklearn.preprocessing import LabelEncoder
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np

def load_and_preprocess_data(excel_path='mop_updated.xlsx'):
    """Load and preprocess the compliance data"""
    print("Loading data from Excel...")
    df = pd.read_excel(excel_path)
    
    # Extract company type from obligation_id
    df['company_type'] = df['obligation_id'].str.extract(r'MOP-([A-Z0-9]+)-')[0]
    
    # Remove rows where company_type couldn't be extracted
    df = df.dropna(subset=['company_type'])
    
    # Create a comprehensive compliance description
    df['compliance_full'] = (
        df['obligation_title'].fillna('') + ' | ' +
        df['obligation_description'].fillna('') + ' | ' +
        df['regulation_name'].fillna('') + ' | ' +
        df['regulation_type'].fillna('')
    )
    
    print(f"Total records: {len(df)}")
    print(f"Unique company types: {df['company_type'].nunique()}")
    
    return df

def create_company_compliance_mapping(df):
    """Create a mapping of company types to their compliances"""
    company_compliance_map = {}
    
    for company_type in df['company_type'].unique():
        company_data = df[df['company_type'] == company_type]
        
        compliances = []
        for _, row in company_data.iterrows():
            compliance_info = {
                'obligation_id': row['obligation_id'],
                'title': row['obligation_title'],
                'description': row['obligation_description'],
                'regulation_name': row['regulation_name'],
                'regulation_type': row['regulation_type'],
                'authority': row['issuing_authority'],
                'mandatory': row['legal_mandatory_flag'],
                'jurisdiction': row['jurisdiction_level'],
                'state': row['state_name'] if pd.notna(row['state_name']) else 'All India'
            }
            compliances.append(compliance_info)
        
        company_compliance_map[company_type] = compliances
    
    return company_compliance_map

def save_model_artifacts(company_compliance_map, df):
    """Save the model artifacts"""
    print("\nSaving model artifacts...")
    
    # Save the main mapping
    with open('compliance_model.pkl', 'wb') as f:
        pickle.dump(company_compliance_map, f)
    
    # Save company type metadata
    company_metadata = {}
    for company_type in df['company_type'].unique():
        company_data = df[df['company_type'] == company_type]
        company_metadata[company_type] = {
            'total_compliances': len(company_data),
            'regulation_types': company_data['regulation_type'].value_counts().to_dict(),
            'authorities': company_data['issuing_authority'].unique().tolist()
        }
    
    with open('company_metadata.pkl', 'wb') as f:
        pickle.dump(company_metadata, f)
    
    # Save all unique company types for the UI
    company_types = sorted(df['company_type'].unique().tolist())
    with open('company_types.pkl', 'wb') as f:
        pickle.dump(company_types, f)
    
    print(f"✓ Saved compliance model with {len(company_compliance_map)} company types")
    print(f"✓ Saved metadata for {len(company_metadata)} company types")
    print(f"✓ Saved {len(company_types)} unique company types")

def main():
    """Main training function"""
    print("=" * 60)
    print("COMPLIANCE PREDICTION MODEL TRAINING")
    print("=" * 60)
    
    # Load and preprocess data
    df = load_and_preprocess_data()
    
    # Create company-compliance mapping
    print("\nCreating company-compliance mapping...")
    company_compliance_map = create_company_compliance_mapping(df)
    
    # Display statistics
    print("\n" + "=" * 60)
    print("TRAINING STATISTICS")
    print("=" * 60)
    for company_type, compliances in sorted(company_compliance_map.items()):
        print(f"{company_type:15} → {len(compliances):3} compliances")
    
    # Save model artifacts
    save_model_artifacts(company_compliance_map, df)
    
    print("\n" + "=" * 60)
    print("✓ MODEL TRAINING COMPLETED SUCCESSFULLY!")
    print("=" * 60)
    print("\nGenerated files:")
    print("  • compliance_model.pkl")
    print("  • company_metadata.pkl")
    print("  • company_types.pkl")
    print("\nYou can now run the Streamlit app with: streamlit run app.py")

if __name__ == "__main__":
    main()
