import matplotlib.pyplot as plt
import numpy as np

def generate_recommendations(feasibility_data):
    """
    Generates actionable recommendations based on feasibility data.
    
    Parameters:
    - feasibility_data (dict): Data containing success probability, median projection, and goal amount.
    
    Returns:
    - recommendations (dict): Suggestions to adjust goal, timeline, or risk allocation.
    """
    recommendations = {}

    # Check if input is single goal or multiple goals
    if "success_probability" in feasibility_data:
        # Single goal recommendation
        recommendations['Goal'] = single_goal_recommendation(feasibility_data)
    else:
        # Multiple goal recommendations
        for goal_name, goal_data in feasibility_data.items():
            recommendations[goal_name] = single_goal_recommendation(goal_data)

    return recommendations

def single_goal_recommendation(goal_data):
    """
    Generates recommendations for a single goal based on feasibility.
    
    Parameters:
    - goal_data (dict): Data for a single goal.
    
    Returns:
    - recommendation (str): Text recommendation for the goal.
    """
    probability_of_success = goal_data['success_probability']
    goal_amount = goal_data['goal_amount']
    median_projection = goal_data['median_projection']

    if probability_of_success >= 75:
        return "Your goal is feasible with the current setup!"
    elif median_projection >= goal_amount:
        return ("Your median projection is above the goal, but success probability is low. "
                "Consider adjusting risk allocation slightly.")
    else:
        return ("Your goal may not be achievable with the current parameters. "
                "Consider increasing your initial investment, extending your timeline, or adjusting risk tolerance.")

def visualize_projections(projections, goal_amount, goal_name="Goal"):
    """
    Creates a histogram of projections to visually represent goal success likelihood.
    
    Parameters:
    - projections (list): Adjusted projections after applying taxes, fees, and inflation.
    - goal_amount (float): User's target amount.
    - goal_name (str): Name of the goal for visualization.
    
    Returns:
    - None (displays the plot).
    """
    plt.figure(figsize=(10, 6))
    plt.hist(projections, bins=50, color='skyblue', edgecolor='black')
    plt.axvline(goal_amount, color='red', linestyle='dashed', linewidth=1.5, label=f"{goal_name} Amount: {goal_amount}")
    plt.xlabel("Projected Value")
    plt.ylabel("Frequency")
    plt.title(f"{goal_name} Projection Distribution with Target Amount")
    plt.legend()
    plt.show()

def create_summary(feasibility_data, projections):
    """
    Prints a summary report and visualizes the projections with goal amount.
    
    Parameters:
    - feasibility_data (dict): Data containing probability of success and other key metrics.
    - projections (dict): Dictionary of projections per goal if multiple goals, otherwise a list for a single goal.
    
    Returns:
    - summary (dict): Contains key insights and recommendations for the user.
    """
    summary = {}
    
    if "success_probability" in feasibility_data:
        # Single goal summary
        recommendation = single_goal_recommendation(feasibility_data)
        visualize_projections(projections, feasibility_data['goal_amount'])
        summary = {
            "initial_investment": feasibility_data['initial_investment'],
            "goal_amount": feasibility_data['goal_amount'],
            "probability_of_success": feasibility_data['success_probability'],
            "median_projection": feasibility_data['median_projection'],
            "projection_range": feasibility_data['projection_range'],
            "recommendation": recommendation
        }
    else:
        # Multi-goal summary
        for goal_name, goal_data in feasibility_data.items():
            recommendation = single_goal_recommendation(goal_data)
            visualize_projections(projections[goal_name], goal_data['goal_amount'], goal_name)
            summary[goal_name] = {
                "initial_investment": goal_data['initial_investment'],
                "goal_amount": goal_data['goal_amount'],
                "probability_of_success": goal_data['success_probability'],
                "median_projection": goal_data['median_projection'],
                "projection_range": goal_data['projection_range'],
                "recommendation": recommendation
            }
    
    return summary

# Example usage for multiple goals
feasibility_data = {
    "House": {
        "initial_investment": 50000,
        "goal_amount": 2000000,
        "success_probability": 80,
        "median_projection": 2200000,
        "projection_range": (1800000, 2500000)
    },
    "Retirement": {
        "initial_investment": 50000,
        "goal_amount": 10000000,
        "success_probability": 60,
        "median_projection": 9000000,
        "projection_range": (8000000, 11000000)
    }
}
projections = {
    "House": [1800000, 1900000, 2000000, 2100000, 2200000, 2300000],
    "Retirement": [8000000, 8500000, 9000000, 9500000, 10000000, 10500000]
}

summary = create_summary(feasibility_data, projections)
print(summary)
