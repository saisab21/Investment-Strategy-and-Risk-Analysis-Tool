import os
import pickle
from data_fetcher import fetch_data
from risk_profiler import risk_profile, dynamic_allocation
from goal_checker_multi import check_multi_goal_feasibility
from tax_adjustment import apply_taxes_and_fees, adjust_for_inflation
from recommendation_engine import create_summary

# Set up caching mechanism to avoid repeated fetching
CACHE_FILE = "cached_data.pkl"

def cache_data(data, filename=CACHE_FILE):
    with open(filename, "wb") as f:
        pickle.dump(data, f)

def load_cached_data(filename=CACHE_FILE):
    if os.path.exists(filename):
        with open(filename, "rb") as f:
            return pickle.load(f)
    return None

def run_pipeline(tickers, initial_investment, goals, user_data, tax_rates, fees, inflation_rate):
    # Step 1: Fetch market data (with caching)
    cached_data = load_cached_data()
    if cached_data:
        print("Using cached financial and sentiment data.")
        financial_data, sentiment_data = cached_data['financial_data'], cached_data['sentiment_data']
    else:
        print("Fetching new data...")
        data = fetch_data(tickers)
        financial_data = data['financial_data']
        sentiment_data = data['sentiment_data']
        cache_data({'financial_data': financial_data, 'sentiment_data': sentiment_data})

    # Step 2: Profile risk and dynamically allocate assets
    risk_score = risk_profile(user_data["age"], user_data["income_stability"], user_data["risk_tolerance"])
    asset_allocation = dynamic_allocation(risk_score, sentiment_data, financial_data)
    print("Dynamic Asset Allocation:", asset_allocation)

    # Step 3: Check goal feasibility for multiple goals
    feasibility_results = check_multi_goal_feasibility(
        initial_investment, goals, asset_allocation, financial_data, tax_rates, fees, inflation_rate
    )
    
    # Step 4: Generate summary and recommendations
    projections = {goal_name: [feasibility_results[goal_name]['median_projection']] for goal_name in goals}
    summary = create_summary(feasibility_results, projections)
    print("Summary:", summary)

# Example user and input data
tickers = ["RELIANCE.NS", "TCS.NS", "NSEI", "^BSESN"]  # Indian market tickers
initial_investment = 1000000  # Example starting capital
goals = {
    "House": {"goal_amount": 2000000, "timeline_years": 15, "priority": "high"},
    "Retirement": {"goal_amount": 10000000, "timeline_years": 30, "priority": "medium"},
    "Education": {"goal_amount": 1000000, "timeline_years": 10, "priority": "low"}
}
user_data = {
    "age": 30,
    "income_stability": "stable",
    "risk_tolerance": "high"
}
tax_rates = {"short_term": 0.15, "long_term": 0.10}
fees = {"stocks": 0.5, "bonds": 0.2, "real_estate": 0.3, "crypto": 0.8}
inflation_rate = 0.05  # 5% inflation

# Run the full pipeline
run_pipeline(tickers, initial_investment, goals, user_data, tax_rates, fees, inflation_rate)
