import pandas as pd
import random
from faker import Faker

# 1. SETUP
# Initialize Faker with Canadian localization (relevant for Alberta job)
fake = Faker('en_CA')

# Set seed for reproducibility (so our "random" data is the same every time we run it)
Faker.seed(42)
random.seed(42)

def generate_data(num_records=100):
    """
    Generates synthetic procurement data.
    """
    data = []
    categories = ['Software Licensing', 'Hardware', 'Consulting Services', 'Cloud Infrastructure']

    # 2. GENERATION LOOP
    for _ in range(num_records):
        
        # Basic Identifiers
        contract_id = fake.bothify(text='CTR-####-??')
        vendor_name = fake.company()
        category = random.choice(categories)
        
        # Financials with Logic
        # We generate a budget, then derive actual spend from it to keep data realistic.
        budget = round(random.uniform(5000.00, 250000.00), 2)
        
        # Simulate Variance: Spend is usually +/- 20% of budget
        variance_multiplier = random.uniform(0.8, 1.2) 
        actual_spend = round(budget * variance_multiplier, 2)
        
        # Compliance Logic (Simulating a Rule Engine)
        # If spend exceeds budget by >10%, flag as Non-Compliant
        if actual_spend > (budget * 1.10):
            compliance = "Non-Compliant"
        else:
            # Mostly Compliant, occasionally under review
            compliance = random.choices(["Compliant", "Review Pending"], weights=[90, 10])[0]

        # Create the Record
        row = {
            "ContractID": contract_id,
            "Vendor": vendor_name,
            "Ministry": "Technology & Innovation",
            "Category": category,
            "Budget": budget,
            "ActualSpend": actual_spend,
            "ComplianceStatus": compliance,
            "ContractDate": fake.date_between(start_date='-1y', end_date='today')
        }
        data.append(row)

    # 3. CONVERT TO DATAFRAME
    return pd.DataFrame(data)

# 4. EXECUTION
if __name__ == "__main__":
    print("Starting Data Generation Pipeline...")
    
    # Generate 150 mock contracts
    df = generate_data(150)
    
    # Save to the raw data folder
    output_path = "data/raw/procurement_data.csv"
    df.to_csv(output_path, index=False)
    
    print(f"✅ Success! {len(df)} records saved to {output_path}")
    print("Sample Data:")
    print(df.head(3))