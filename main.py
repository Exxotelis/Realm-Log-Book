import streamlit as st
import pandas as pd
from research import Research


# Function to load leader data from the text file into a dataframe
def load_leader_data():
    try:
        # Read leader data from the text file
        leader_data = pd.read_csv('leaders_data.txt')
        return leader_data
    except FileNotFoundError:
        st.error("Leader data file not found. Please make sure the file exists.")
        return None


# Function to calculate RLM production per hour
def calculate_rlm_production(selected_leader_row, level):
    try:
        base_rlm_per_hour = selected_leader_row["RLM/HR"]
        rlm_production = base_rlm_per_hour * (1 + 0.10 * (level - 1))
        return rlm_production
    except KeyError:
        st.error("Invalid leader data format.")
        return None


# Function to display additional information for the selected leader
def display_additional_info(selected_leader_name, selected_leader_data):
    st.subheader(f"Additional Information for {selected_leader_name}:")
    st.write(f"Region Bonus: {selected_leader_data['Region Bonus']}")
    st.write(f"Bonus Amount: {selected_leader_data['Bonus Amt']}")
    st.write("---")


# Function to handle user input and calculations
def main():
    logo = "images/realm-logo.png"
    st.set_page_config(page_title="Leader RLM Production Calculator",
                       page_icon=logo, layout="wide")

    col1, col2, col3 = st.columns([1, 3, 1])

    with col2:
        st.title("Leader RLM Production Calculator")
        st.write(
            "This app calculates the RLM production rate and team size for different leaders in the game 'REALM NFT'.")
        st.write(
            "Select a leader from the dropdown menu and adjust the level to see the RLM production rate and team size.")
        leader_data = load_leader_data()
        if leader_data is not None:
            unique_leader_names = leader_data["Name"].unique()
            selected_leader_name = st.selectbox(
                "Select Leader", unique_leader_names)

            selected_leader_data = leader_data[leader_data["Name"]
                                               == selected_leader_name]

            selected_star_ratings = selected_leader_data["Star Rating"].unique(
            )
            selected_star_rating = st.selectbox(
                f"Select Star Rating for {selected_leader_name}", selected_star_ratings)

            level = st.slider(f"Level of {selected_leader_name}", 1, 100, 1)

            selected_leader_row = selected_leader_data[selected_leader_data["Star Rating"] == selected_star_rating].squeeze(
            )

            team_size = selected_leader_row["Team Size"] + \
                (selected_leader_row["Team Size"] * (level - 1))

            st.subheader("Image for the selected leader:")
            image_path = selected_leader_row['img_path']
            if image_path:
                st.image(image_path, caption="Leader Image",
                         use_column_width=False)
            else:
                st.write("No image available for this leader.")

            display_additional_info(selected_leader_name, selected_leader_row)

            rlm_production = calculate_rlm_production(
                selected_leader_row, level)
            if rlm_production is not None:
                st.markdown(f"""**RLM Production Rate:** <span style='font-size:20px'>{rlm_production:.2f} RLM per hour</span>
                            \nBase Team Size: {team_size} helpers""", unsafe_allow_html=True)

                research_lvl = st.slider(
                    "Research Level", 0, 30, 0, format="%d%%")
                leader_research_lvl = st.slider(
                    "Leader Research Level", 0, 20, 0, format="%d%%")
                investment_lvl = st.slider(
                    "Investment Level", 0, 10, 0, format="%d%%")

                research = Research()

                total_increase = research.calculate_rlm_increase(
                    rlm_production, research_lvl)
                leader_rlm_increase = research.calculate_leader_rlm_increase(
                    rlm_production, leader_research_lvl)
                investment_rlm_increase = research.calculate_investment_rlm_increase(
                    rlm_production, investment_lvl)

                total_combined_increase = rlm_production + total_increase + \
                    leader_rlm_increase + investment_rlm_increase

                st.write(f"""After Research RLM Increase: {
                         total_increase:.2f} RLM per hour""")
                st.write(f"""RLM Increase from Leader Research: {
                         leader_rlm_increase:.2f} RLM per hour""")
                st.write(f"""RLM Increase from Investment: {
                         investment_rlm_increase:.2f} RLM per hour""")
                st.write(f"""The total RLM/HR for {selected_leader_name} is: {
                         total_combined_increase:.2f} RLM per hour""")
    with col3:
        # Function to add calculator
        def add_calc():
            # Initialize additional RLM percentage
            additional_rlm_percentage = 0

            # Display the images
            image_options = {
                "Common Calculator": "images/com-calc.png",
                "Rare Calculator": "images/rare-calc.png",
                "Epic Calculator": "images/epic-calc.png",
                "Legendary Calculator": "images/leg-calc.png"
            }

            # Selectbox to choose calculator rarity
            selected_option = st.selectbox(
                "Select the rarity of the calculator", ["Common Calculator", "Rare Calculator", "Epic Calculator", "Legendary Calculator"])

            # Display selected image
            selected_image = st.empty()
            selected_image.image(
                image_options[selected_option], caption=selected_option, use_column_width=False)

            # Dictionary mapping rarity to additional percentage
            rarity_percentage = {
                "Common Calculator": 0.05,
                "Rare Calculator": 0.10,
                "Epic Calculator": 0.20,
                "Legendary Calculator": 0.50
            }

            # Checkbox to calculate RLM Production
            calculate_rlm = st.checkbox(
                "Calculate RLM Production", value=True)
            if calculate_rlm:
                # Calculate additional RLM based on the selected calculator rarity
                additional_rlm_percentage = rarity_percentage[selected_option]
                st.write(f"""Additional RLM: {
                         additional_rlm_percentage * 100:.2f}% of base RLM production""")

            return additional_rlm_percentage

        # Function to calculate total combined increase
        def calculate_total_combined_increase(rlm_production, additional_rlm_percentage):
            total_combined_increase = rlm_production + additional_rlm_percentage
            return total_combined_increase

        # Call the function to get the additional RLM percentage
        additional_rlm_percentage = add_calc()

        # Calculate total combined increase
        total_combined_increase_value = calculate_total_combined_increase(
            rlm_production, additional_rlm_percentage)

        # Display the result
        st.subheader("Calculator")
        st.write(f"""The total RLM/HR for {selected_leader_name} is: {
                 total_combined_increase_value:.2f} RLM per hour""")

        val1 = additional_rlm_percentage + total_combined_increase
        st.write(f"""The total RLM/HR for {selected_leader_name} is: {
                 val1:.2f} RLM per hour""")


# Run the main function
if __name__ == "__main__":
    main()
