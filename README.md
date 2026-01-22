# Compliance Matrix

An AI-powered compliance identification system that helps companies identify applicable compliances based on their company type.

## Features

- **Smart Prediction**: ML-based compliance matching using company type
- **Minimalist UI**: Professional dark mode design with a technical dotted background
- **Search & Filter**: Quickly find specific compliances
- **Detailed Information**: Complete compliance details including:
  - Obligation ID and Title
  - Description
  - Regulation Name and Type
  - Issuing Authority
  - Jurisdiction Level
  - Mandatory/Optional status
- **Export Functionality**: Download results as CSV
- **Real-time Statistics**: View compliance counts and breakdowns

## Quick Start

### 1. Install Dependencies

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # On Linux/Mac
# or
venv\Scripts\activate  # On Windows

# Install packages
pip install -r requirements.txt
```

### 2. Train the Model

```bash
python train_model.py
```

This will:
- Load data from `mop_updated.xlsx`
- Extract company types from obligation IDs
- Create compliance mappings
- Generate model files (`.pkl` files)

### 3. Run the Streamlit App

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

## How It Works

### Data Structure

The system extracts company types from the `obligation_id` field in the Excel file:
- Format: `MOP-{COMPANY_TYPE}-{NUMBER}`
- Example: `MOP-BIO-001` -> Company Type: `BIO`

### Model Training

1. Loads compliance data from Excel
2. Extracts company types using regex pattern matching
3. Creates a mapping: `Company Type -> List of Compliances`
4. Saves the mapping and metadata as pickle files

### Prediction

When a user selects a company type:
1. System retrieves all compliances for that type
2. Displays them in an organized, searchable format
3. Shows statistics and breakdowns
4. Allows filtering and export

## UI Features

- **Dark Mode**: Pure black background for high contrast and focus
- **Dotted Background**: Subtle technical grid pattern for a professional aesthetic
- **Glassmorphism**: Sophisticated frosted glass effects on cards
- **Responsive Design**: Works on all screen sizes
- **Space Grotesk Font**: Modern technical typography for clarity

## Project Structure

```
compliance/
├── mop_updated.xlsx          # Source data
├── train_model.py            # Model training script
├── app.py                    # Streamlit application
├── requirements.txt          # Python dependencies
├── compliance_model.pkl      # Trained model (generated)
├── company_metadata.pkl      # Company metadata (generated)
├── company_types.pkl         # List of company types (generated)
└── README.md                 # This file
```

## Statistics

- **Total Company Types**: 73
- **Total Compliances**: 134
- **Regulation Types**: 25 different types
- **Coverage**: All major energy sector company types

## Company Types Supported

The system supports 73 company types including:
- BIO (Biomass) - 7 compliances
- COAL - 6 compliances
- ROC, LPS - 5 compliances each
- TBCB, RPO, GEOA - 4 compliances each
- And many more...

## Usage Tips

1. **Select Company Type**: Choose from the dropdown in the sidebar
2. **View Statistics**: Check the quick stats for overview
3. **Search**: Use the search box to filter specific compliances
4. **Export**: Download results as CSV for offline use
5. **Explore Details**: Each card shows complete compliance information

## Technical Stack

- **Backend**: Python 3.x
- **ML Framework**: scikit-learn
- **Data Processing**: pandas, openpyxl
- **UI Framework**: Streamlit
- **Styling**: Custom CSS with modern design principles

## Notes

- All compliances are extracted from the official MOP (Ministry of Power) data
- The system uses pattern matching to categorize compliances
- Model can be retrained with updated Excel data
- Export functionality preserves all compliance details

## Future Enhancements

- Multi-company type selection
- Compliance timeline view
- Notification system for updates
- Integration with compliance tracking tools
- Advanced filtering options
- Compliance comparison between company types

## License

This project is created for compliance management and identification purposes.

---

**Built using Streamlit and ML**
