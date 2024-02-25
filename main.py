import streamlit as st
import pandas as pd
from research import Research

logo = "images/realm-logo.png"
st.set_page_config(page_title="Leader RLM Production Calculator",
                   page_icon=logo)
st.title("Leader RLM Production Calculator")
st.write("This app calculates the RLM production rate and team size for different leaders in the game 'REALM NFT'.")
st.write("Select a leader from the dropdown menu and adjust the level to see the RLM production rate and team size.")


# Load leader data from the text file into a dataframe
def load_leader_data():
    # Read leader data from the text file
    leader_data = pd.read_csv('leaders_data.txt')
    return leader_data

# Function to display additional information for the selected leader


def display_additional_info(selected_leader_data):
    st.subheader(f"Additional Information for {selected_leader_name}:")
    st.write(f"Region Bonus: {selected_leader_data['Region Bonus']}")
    st.write(f"Bonus Amount: {selected_leader_data['Bonus Amt']}")
    st.write("---")


# Function to calculate RLM/HR
def calculate_rlm_per_hour(selected_leader_row, level):
    rlm_per_hour_base = selected_leader_row["RLM/HR"]
    rlm_production = rlm_per_hour_base * (1 + 0.10 * (level - 1))
    return rlm_production


# Load leader data and images
leader_data = load_leader_data()

# Remove duplicates and keep only unique leader names
unique_leader_names = leader_data["Name"].unique()

selected_leader_name = st.selectbox("Select Leader", unique_leader_names)

# Filter the data for the selected leader
selected_leader_data = leader_data[leader_data["Name"] == selected_leader_name]


selected_star_ratings = selected_leader_data["Star Rating"].unique()
selected_star_rating = st.selectbox(
    f"Select Star Rating for {selected_leader_name}", selected_star_ratings
)

level = st.slider(f"Level of {selected_leader_name}", 1, 100, 1)

selected_leader_row = selected_leader_data[selected_leader_data["Star Rating"]
                                           == selected_star_rating].squeeze()


# Calculate team size
team_size = selected_leader_row["Team Size"] + \
    (selected_leader_row["Team Size"] * (level - 1))

# Display image for the selected leader
st.subheader("Image for the selected leader:")
image_path = selected_leader_row['img_path']
if image_path:
    # Display the image using the file path
    st.image(image_path, caption="Leader Image", use_column_width=False)
else:
    st.write("No image available for this leader.")

# Calculate and display RLM Production Rate
rlm_production = calculate_rlm_per_hour(selected_leader_row, level)
st.markdown(f"""\n**RLM Production Rate:** <span style='font-size:20px'>{
            rlm_production:.2f} RLM per hour</span>\n
            Base Team Size: {team_size} helpers""", unsafe_allow_html=True)


# st.write(f"Team Size: {team_size}")


# Display the slider for research level
research_lvl = st.slider("Research Level", 0, 30, 0, format="%d")
# Display the sliders for leader research level and investment level
leader_research_lvl = st.slider("Leader Research Level", 0, 20, 0, format="%d")
investment_lvl = st.slider("Investment Level", 0, 10, 0, format="%d")

research = Research()
# Calculate the RLM increase from leader research and investment
leader_rlm_increase = research.calculate_leader_rlm_increase(
    rlm_production, leader_research_lvl)
investment_rlm_increase = research.calculate_investment_rlm_increase(
    rlm_production, investment_lvl)

# Calculate the total RLM increase
total_increase = research.calculate_rlm_increase(rlm_production, research_lvl)

# Calculate the total combined RLM increase
total_combined_increase = rlm_production + total_increase

# Display the calculated total combined RLM increase
st.write(f"""After Research RLM Increase: {
         total_increase:.2f} RLM per hour""")

# Calculate the total combined RLM increase
total_combined_increase = rlm_production + total_increase + \
    leader_rlm_increase + investment_rlm_increase

# Display the calculated RLM increases
st.write(f"""RLM Increase from Leader Research: {
         leader_rlm_increase:.2f} RLM per hour""")
st.write(f"""RLM Increase from Investment: {
         investment_rlm_increase:.2f} RLM per hour""")
st.write(f"""The total RLM/HR for the {selected_leader_name} is: {
         total_combined_increase:.2f} RLM per hour""")
st.divider()

st.markdown("<p style='font-size: 12px; position: fixed; bottom: 0; left: 50%; transform: translateX(-50%);'>© 2024 Exxotelis. All rights reserved.</p>", unsafe_allow_html=True)
