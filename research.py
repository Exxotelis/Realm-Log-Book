class Research:
    def __init__(self):
        pass

    # Define the function to calculate RLM increase based on research level
    def calculate_rlm_increase(self, rlm_production, research_lvl):
        total_increase = rlm_production * (research_lvl / 100)
        return total_increase

    # Calculate RLM increase based on leader research level
    def calculate_leader_rlm_increase(self, rlm_production, leader_research_lvl):
        leader_increase = rlm_production * (leader_research_lvl / 100)
        return leader_increase

    # Calculate RLM increase based on investment level
    def calculate_investment_rlm_increase(self, rlm_production, investment_lvl):
        investment_increase = rlm_production * (investment_lvl / 100)
        return investment_increase
