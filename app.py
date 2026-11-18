from pathlib import Path

import joblib
import streamlit as st


st.set_page_config(page_title="SmartCart", page_icon="🛒")

app_folder = Path(__file__).resolve().parent


@st.cache_resource
def load_smartcart():
    return joblib.load(app_folder / "smartcart.pkl")


saved = load_smartcart()
model = saved["model"]
matrix = saved["rating_matrix"]
product_ids = saved["product_ids"]


def recommend(product_id):
    row = product_ids.get_loc(product_id)
    neighbors = model.kneighbors(
        matrix[row],
        n_neighbors=min(6, len(product_ids)),
        return_distance=False
    )

    suggestions = []
    for number in neighbors[0]:
        if number != row:
            suggestions.append(product_ids[number])

    return suggestions[:5]


st.title("🛒 SmartCart")
st.write("Choose a product to find others with similar customer rating patterns.")

with st.form("product_search"):
    selected_id = st.selectbox("Search or select a product ID", product_ids.tolist())
    search = st.form_submit_button("Find similar products")

if search:
    st.subheader(f"Recommendations for {selected_id}")

    for rank, product_id in enumerate(recommend(selected_id), start=1):
        st.write(f"**{rank}. Product {product_id}**")

        image_file = app_folder / "images" / f"{product_id}.jpg"
        if image_file.is_file():
            st.image(str(image_file), width=160)
