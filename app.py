from pathlib import Path
import sqlite3

import joblib
import streamlit as st


st.set_page_config(page_title="SmartCart", page_icon="🛒")
folder = Path(__file__).resolve().parent


@st.cache_resource
def load_smartcart():
    saved = joblib.load(folder / "smartcart.pkl")

    with sqlite3.connect(folder / "catalog.db") as db:
        rows = db.execute(
            "SELECT product_id, name, photo FROM products ORDER BY name"
        ).fetchall()

    catalog = {}
    for product_id, name, photo in rows:
        catalog[product_id] = {"name": name, "photo": photo}

    return saved, catalog


def recommend(selected_id, saved, catalog):
    ids = saved["product_ids"]
    matrix = saved["rating_matrix"]
    model = saved["model"]
    selected_row = ids.get_loc(selected_id)

    # Ek selected product ko baaki products se compare karo
    distances, rows = model.kneighbors(
        matrix[selected_row],
        n_neighbors=len(ids)
    )

    results = []
    for distance, row in zip(distances[0], rows[0]):
        if distance >= 1:
            break

        product_id = ids[row]
        if product_id != selected_id and product_id in catalog:
            results.append(product_id)

        if len(results) == 5:
            break

    return results


st.title("🛒 SmartCart")
st.write("Search for a grocery product to see recommendations based on customer ratings.")

if not (folder / "catalog.db").is_file() or not (folder / "smartcart.pkl").is_file():
    st.error("Place catalog.db and smartcart.pkl in the same folder as app.py.")
    st.stop()

saved, catalog = load_smartcart()
available_ids = [pid for pid in catalog if pid in saved["product_ids"]]

if not available_ids:
    st.error("The catalog has no products matching this model.")
    st.stop()

selected_id = st.selectbox(
    "Search by product name",
    options=available_ids,
    format_func=lambda pid: catalog[pid]["name"]
)

selected = catalog[selected_id]
photo_column, name_column = st.columns([1, 2])

with photo_column:
    st.image(selected["photo"], width=160)

with name_column:
    st.subheader(selected["name"])
    st.caption(f"Product ID: {selected_id}")

st.subheader("Recommended for you")
suggestions = recommend(selected_id, saved, catalog)

if not suggestions:
    st.info("This product has no matching rating pattern in the photo catalog. Try another product.")

for product_id in suggestions:
    product = catalog[product_id]
    photo_column, name_column = st.columns([1, 2])

    with photo_column:
        st.image(product["photo"], width=130)

    with name_column:
        st.write(product["name"])
        st.caption(f"Product ID: {product_id}")

    st.divider()
