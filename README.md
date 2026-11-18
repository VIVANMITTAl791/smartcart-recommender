# smartcart-recommender
A Streamlit app that recommends five similar Amazon products based on customer ratings using item-based KNN and cosine similarity.
# SmartCart – Product Recommendation System

SmartCart is a Streamlit app that recommends up to five products for a selected
Amazon product ID. It uses item-based KNN with cosine distance to find products
with similar customer rating patterns.

## Dataset and preparation

I used the [Amazon Product Reviews dataset](https://www.kaggle.com/datasets/arhamrumi/amazon-product-reviews).
I checked missing values and selected UserId, ProductId, Score and Time.
For repeated user-product pairs, I kept the latest rating.

After cleaning, I used 480,209 ratings for training and held out 80,595 ratings
for testing. I built a sparse product-user matrix from the training data.

## Evaluation

I tested both methods on the same random sample of 100 eligible users.
A hit means the user's held-out liked product appeared in the top five suggestions.

| Method | Hits out of 100 | Hit Rate@5 |
|---|---:|---:|
| Popular products | 1 | 1% |
| Item-based KNN | 52 | 52% |

The evaluation sample came from 55,562 eligible users.

## Run locally

```bash
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

Select a product ID and click **Find similar products**.
Product photos can be added as `images/PRODUCT_ID.jpg`.
