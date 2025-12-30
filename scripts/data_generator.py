import pandas as pd
import random
from faker import Faker

# ==========================================
# CONFIGURATION & INITIALIZATION
# ==========================================

# Initialize Faker with 'en_CA' locale.
# MECHANICS: This loads the specific provider modules for Canadian formats (e.g., Postal Codes: A1A 1A1, Provinces: AB/ON).
# REASONING: Crucial for mocking Government of Alberta (GoA) data accurately. US defaults (Zip codes) would trigger validation errors in downstream systems.
fake = Faker('en_CA')

# Deterministic Seeding
# MECHANICS: Fixes the internal state of the Mersenne Twister (Python's PRNG) and Faker's generator.
# REASONING: Ensures Idempotency. This pipeline must produce the exact same dataset on every run to allow for regression testing of the Power BI dashboard.
Faker.seed(42)
random.seed(42)

def generate_data(num_records=100):
    """
    Orchestrates the creation of synthetic procurement records.
    
    Args:
        num_records (int): The volume of rows to generate.
        
    Returns:
        pd.DataFrame: A tabular representation of the dataset ready for ETL ingestion.
    """
    
    # Pre-allocating list for row storage. 
    # PERFORMANCE NOTE: Appending to a list is O(1) amortized. Appending directly to a DataFrame is O(N) (quadratic cost)
    # because DataFrames are immutable in structure and require full recreation on every append. 
    # Always build the list first, then cast to DataFrame once.
    data = []
    
    # Domain-specific constraints for the Ministry of Technology & Innovation
    categories = ['Software Licensing', 'Hardware', 'Consulting Services', 'Cloud Infrastructure']

    # ==========================================
    # DATA GENERATION LOOP
    # ==========================================
    for _ in range(num_records):
        
        # 1. Identifier Synthesis
        # MECHANICS: 'bothify' parses the string mask. '#' maps to random.randint(0,9), '?' maps to random.choice(letters).
        # RESULT: Generates high-entropy IDs (e.g., CTR-9482-XY) that mimic standard ERP contract keys.
        contract_id = fake.bothify(text='CTR-####-??')
        vendor_name = fake.company()
        category = random.choice(categories)
        
        # 2. Financial Modeling (Statistical Correlation)
        # MECHANICS: Uniform distribution provides a flat probability across the range.
        # REALISM CHECK: In real procurement, spend is not random; it follows a power law (Pareto). 
        # For this mock, Uniform is sufficient, but for advanced modelling, we would use numpy.random.lognormal().
        budget = round(random.uniform(5000.00, 250000.00), 2)
        
        # 3. Variance Simulation (The "Chaos" Factor)
        # REASONING: Independent random generation of Budget and ActualSpend creates disjointed data (e.g., Budget $5k, Spend $500k).
        # SOLUTION: Derive ActualSpend as a function of Budget (y = f(x) + noise).
        # We introduce a +/- 20% variance noise factor to simulate real-world project drift.
        variance_multiplier = random.uniform(0.8, 1.2) 
        actual_spend = round(budget * variance_multiplier, 2)
        
        # 4. Compliance Rule Engine
        # LOGIC: Simulates a static threshold policy.
        # THRESHOLD: 110% of Budget.
        # BRANCHING: 
        #   - IF variance > 10% positive drift -> Deterministic "Non-Compliant".
        #   - ELSE -> Probabilistic distribution (90% Compliant / 10% Pending Review).
        # This creates a "Target Class" for future Machine Learning classification tasks.
        if actual_spend > (budget * 1.10):
            compliance = "Non-Compliant"
        else:
            # Weighted choice simulates the rarity of administrative hold-ups (Review Pending).
            compliance = random.choices(["Compliant", "Review Pending"], weights=[90, 10])[0]

        # 5. Record Assembly
        # Storing as a dictionary allows for O(1) key-value insertion before list append.
        row = {
            "ContractID": contract_id,
            "Vendor": vendor_name,
            "Ministry": "Technology & Innovation", # Static Dimension
            "Category": category,
            "Budget": budget,
            "ActualSpend": actual_spend,
            "ComplianceStatus": compliance,
            # Temporal distribution: Backdates contracts up to 1 year to populate Time Series visuals.
            "ContractDate": fake.date_between(start_date='-1y', end_date='today')
        }
        data.append(row)

    # ==========================================
    # DATAFRAME SERIALIZATION
    # ==========================================
    # Casts list of dicts to DataFrame. Pandas infers dtypes (Float64 for financials, Object for strings, Datetime64 for dates).
    return pd.DataFrame(data)

# ==========================================
# ENTRY POINT
# ==========================================
if __name__ == "__main__":
    print("Starting Data Generation Pipeline...")
    
    # Generate batch of 150 records
    df = generate_data(150)
    
    # I/O OPERATION
    # Save to CSV without index.
    # REASONING: The DataFrame index is an arbitrary range (0-149) and provides no business value. 
    # Excluding it prevents 'Unnamed: 0' artifacts during Power BI ingestion.
    output_path = "data/raw/procurement_data.csv"
    df.to_csv(output_path, index=False)
    
    print(f"Pipeline Complete. {len(df)} records serialized to {output_path}")
    print("Head view of generated schema:")
    print(df.head(3))