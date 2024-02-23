import streamlit as st
import pandas as pd

st.title("Leader RLM Production Calculator")
st.write("This app calculates the RLM production rate and team size for different leaders in the game 'REALM NFT'.")
st.write("Select a leader from the dropdown menu and adjust the level to see the RLM production rate and team size.")
# Load leader data from the text file into a dataframe


def load_leader_data():
    # Read leader data from the text file
    leader_data = pd.read_csv('leaders_data.txt')
    return leader_data


# Load leader data and images
leader_data = load_leader_data()

# Remove duplicates and keep only unique leader names
unique_leader_names = leader_data["Name"].unique()

selected_leader_name = st.selectbox("Select Leader", unique_leader_names)

# Filter the data for the selected leader
selected_star_rating = st.selectbox(f"Select Star Rating for {selected_leader_name}",
                                    leader_data[leader_data["Name"] == selected_leader_name]["Star Rating"].unique().tolist())

selected_leader_data = leader_data[(leader_data["Name"] == selected_leader_name) & (
    leader_data["Star Rating"] == selected_star_rating)].iloc[0]

# Display additional information for the selected leader
st.subheader(f"Additional Information for {selected_leader_name}:")
st.write(f"Region Bonus: {selected_leader_data['Region Bonus']}")
st.write(f"Bonus Amount: {selected_leader_data['Bonus Amt']}")
st.write("---")

level = st.slider(f"Level of {selected_leader_name}", 0, 100, 0)

team_size_base = selected_leader_data["Team Size"]
rlm_per_hour_base = selected_leader_data["RLM/HR"]

rlm_production = rlm_per_hour_base * (1 + 0.10 * (level - 1))
team_size = team_size_base * (1 * (level - 1))

# Display image for the selected leader
st.subheader("Image for the selected leader:")
image_path = selected_leader_data['img_path']
if image_path:
    # Display the image using the file path
    st.image(image_path, caption="Leader Image", use_column_width=False)
else:
    st.write("No image available for this leader.")

st.write(f"RLM Production Rate: {rlm_production:.2f} RLM per hour")
st.write(f"Team Size: {team_size}")
