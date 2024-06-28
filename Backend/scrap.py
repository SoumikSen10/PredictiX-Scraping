import fitz  # PyMuPDF
import re
import joblib
import sys
import numpy as np
import warnings

# Path to the PDF file
pdf_path = 'HeartReport_NotSuffering.pdf'  # Update this path if necessary

try:
    # Open the PDF file
    pdf_document = fitz.open(pdf_path)
    page = pdf_document.load_page(0)
    text = page.get_text()
except Exception as e:
    print(f"Error opening or reading PDF: {e}")
    sys.exit(1)

# Function to extract values using regular expressions with error handling
def extract_value(pattern, text, default=None):
    try:
        match = re.search(pattern, text)
        if match:
            return match.group(1)
        return default
    except Exception as e:
        print(f"Error extracting value with pattern '{pattern}': {e}")
        return default

# Extract values with error handling
results = {}
try:
    results['Age'] = extract_value(r'Age:\s+(\d+)', text)
    results['Sex'] = extract_value(r'Sex:\s+(\w+)', text)
    results['Chest pain type'] = extract_value(r'Chest pain type:\s+(\d+)', text)
    results['Resting blood pressure'] = extract_value(r'Resting blood pressure:\s+(\d+)', text)
    results['Serum cholesterol in mg/dl'] = extract_value(r'Serum cholesterol in mg/dl:\s+(\d+)', text)
    results['Fasting blood sugar > 120 mg/dl'] = extract_value(r'Fasting blood sugar > 120 mg/dl:\s+(\w+)', text, 'Negative')
    results['Resting Electrocardiographic Results'] = extract_value(r'Resting Electrocardiographic Results:\s+(\d+)', text)
    results['Maximum Heart Rate Achieved'] = extract_value(r'Maximum Heart Rate Achieved:\s+(\d+)', text)
    results['Exercise Induced Angina'] = extract_value(r'Exercise Induced Angina:\s+(\d+)', text)
    results['Old peak'] = extract_value(r'Old peak:\s+(\d+\.\d+)', text)
    results['Slope of the peak exercise ST Segment'] = extract_value(r'Slope of the peak exercise ST Segment:\s+(\d+)', text)
    results['Number of major vessels (0-3) colored by fluoroscopy'] = extract_value(r'Number of major vessels \(0-3\) colored by fluoroscopy:\s+(\d+)', text)
    results['Thal (Thallium Stress Test Result)'] = extract_value(r'Thal \(Thallium Stress Test Result\):\s+(\d+)', text)
except Exception as e:
    print(f"Error extracting results: {e}")
    sys.exit(1)

# Mapping Sex to a numeric value if needed (e.g., Male=1, Female=0)
sex_mapping = {'Male': 1, 'Female': 0}
results['Sex'] = sex_mapping.get(results['Sex'], -1)  # Default to -1 if sex is not Male or Female

# Print the extracted results
for key, value in results.items():
    print(f'{key}: {value}')

print("-------------------------------------")

# Create features array in the order expected by the model
try:
    features = [
        int(results['Age']),
        int(results['Sex']),
        int(results['Chest pain type']),
        int(results['Resting blood pressure']),
        int(results['Serum cholesterol in mg/dl']),
        int(1 if results['Fasting blood sugar > 120 mg/dl'] == 'Yes' else 0),
        int(results['Resting Electrocardiographic Results']),
        int(results['Maximum Heart Rate Achieved']),
        int(1 if results['Exercise Induced Angina'] == 'Yes' else 0),
        float(results['Old peak']),  # Assuming Old peak is a float
        int(results['Slope of the peak exercise ST Segment']),
        int(results['Number of major vessels (0-3) colored by fluoroscopy']),
        int(results['Thal (Thallium Stress Test Result)'])
    ]
except Exception as e:
    print(f"Error creating features array: {e}")
    sys.exit(1)

# Print the features array
print("Features array:", features)

# Function to create feature array
def feature_create(*args):
    try:
        # Convert input arguments to a numpy array of floats
        features = np.array([args], dtype=float)
        return features
    except Exception as e:
        print(f"Error creating features: {e}")
        sys.exit(1)

# Suppress warnings for model version inconsistency
warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=DeprecationWarning)

# Load the model
try:
    model = joblib.load('heart_disease.pkl')
except Exception as e:
    print(f"Error loading model: {e}")
    sys.exit(1)

# Create features from the extracted values
try:
    features = feature_create(*features)
except Exception as e:
    print(f"Error creating features: {e}")
    sys.exit(1)

# Make prediction
try:
    prob = model.predict(features)
    print(int(prob[0]))  # Print the prediction as an integer
    if(int(prob[0]) == 1):
        print("Patient is predicted to be suffering from Heart Disease")
    elif(int(prob[0]) == 0):
        print("Patient is predicted not to be suffering from Heart Disease")
except Exception as e:
    print(f"Error in prediction: {e}")
    sys.exit(1)
