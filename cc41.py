# %%
import streamlit as st
import pandas as pd
import pickle

with open("kmeans_model.pkl", "rb") as file:
    kmeans_model = pickle.load(file)
    
st.title("Customer Segmentation with K-means Clustering")

st.header("User Input:")
balance = st.slider("Balance", min_value=0.0, max_value=20000.0, step=100.0, value=1000.0)
purchases = st.slider("Purchases", min_value=0.0, max_value=50000.0, step=100.0, value=1000.0)
oneoff_purchases = st.slider("One-Off Purchases", min_value=0.0, max_value=50000.0, step=100.0, value=1000.0)
installments_purchases = st.slider("Installments Purchases", min_value=0.0, max_value=30000.0, step=100.0, value=1000.0)
cash_advance = st.slider("Cash Advance", min_value=0.0, max_value=50000.0, step=100.0, value=1000.0)
credit_limit = st.slider("Credit Limit", min_value=0.0, max_value=30000.0, step=100.0, value=10000.0)
payments = st.slider("Payments", min_value=0.0, max_value=50000.0, step=100.0, value=1000.0)
prc_full_payment = st.slider("Percentage of Full Payment", min_value=0.0, max_value=1.0, step=0.01, value=0.5)
tenure = st.slider("Tenure", min_value=0, max_value=20, step=1, value=10)
credit_utilization = st.slider("Credit Utilization", min_value=0.0, max_value=1.0, step=0.01, value=0.5)
purchases_frequency = st.slider("Purchases Frequency", min_value=0.0, max_value=1.0, step=0.01, value=0.5)
purchases_instalments_frequency = st.slider("Purchases Instalments Frequency", min_value=0.0, max_value=1.0, step=0.01, value=0.5)

user_input = {
    'BALANCE': balance,
    'PURCHASES': purchases,
    'ONEOFF_PURCHASES': oneoff_purchases,
    'INSTALLMENTS_PURCHASES': installments_purchases,
    'CASH_ADVANCE': cash_advance,
    'CREDIT_LIMIT': credit_limit,
    'PAYMENTS': payments,
    'PRC_FULL_PAYMENT': prc_full_payment,
    'TENURE': tenure,
    'CREDIT_UTILIZATION': credit_utilization,
    'PURCHASES_FREQUENCY': purchases_frequency,
    'PURCHASES_INSTALLMENTS_FREQUENCY': purchases_instalments_frequency,
}

def perform_clustering(user_input):
    def scale_user_input(user_input):
        feature_ranges = {
            'BALANCE': (0.0, 20000.0),
            'PURCHASES': (0.0, 50000.0),
            'ONEOFF_PURCHASES': (0.0, 50000.0),
            'INSTALLMENTS_PURCHASES': (0.0, 30000.0),
            'CASH_ADVANCE': (0.0, 50000.0),
            'CREDIT_LIMIT': (0.0, 30000.0),
            'PAYMENTS': (0.0, 50000.0),
            'PRC_FULL_PAYMENT': (0.0, 1.0),
            'TENURE': (0, 20),
            'CREDIT_UTILIZATION': (0.0, 1.0),    
            'PURCHASES_FREQUENCY': (0.0, 1.0) ,
            'PURCHASES_INSTALLMENTS_FREQUENCY': (0.0, 1.0) 
        }

        scaled_user_input = {feature: (user_input[feature] - min_val) / (max_val - min_val)
                              for feature, (min_val, max_val) in feature_ranges.items()}

        return pd.DataFrame(scaled_user_input, index=[0])

    user_df_scaled = scale_user_input(user_input)

    cluster = kmeans_model.predict(user_df_scaled)[0]
    return cluster

def get_segment_description(cluster):
    segment_descriptions = {
    0:  "Segment 1: (Diamond): Champions-High Payments made by the user, Best Customers,  Bought frequently, High Credit Utilization, Potential Loyalist,s are your recent customers with average frequency and who spent a good amount..",
    4:  "Segment 5: (Copper): Being the youngest customer, Low Payments,   Low frequency, Low Credit Utilization. ",
    5:  "Segment 6: (Bronze): Customers who made smaller and infrequent purchases before but haven't purchased anything in a long time. Low Payments Made good payment orders, High Balance. But frequency is low. Extremely Low Credit Utilization.",
    1:  "Segment 2: (Platinum): High Balance High Payments made by the user, Frequency not High, Low Credit Utilization, Orders regularly..",
    2:  "Segment 3: (Gold): Not high Balance, Spent reasonably good amount Bought frequently, Average Credit Utilization score. Recent customers who spent good amounts. Potential Loyalists .",
    3:  "Segment 4: (Silver): High Payments made by the user, Bought frequently, Average Credit Utilization, Extremely Low Balance.",
    }
    return segment_descriptions.get(cluster, "Undefined Segment")

def get_recommendations(cluster):
    recommendations = {
        0: "Recommendation for Segment 1: Offer membership or loyalty programs or recommend related products to upsell them and help them become your Loyalists or Champions. Reward Accelerators are effective for cardholders who are vested in your loyalty program. Bonus points or cash-back incentives encourage more frequent purchases and higher spend. For example, “Earn three times the points for all grocery purchases in the next 30 days,” or “Spend $3,000 or more and get 5% cash back”.",
        4: "Recommendation for Segment 5: Make subject lines of emails very personalized. Revive their interest by a specific discount on a specific product. Win them back via renewals or newer products, don’t lose them to competition. Talk to them if necessary. Spend time on highest possible personalization.   Use and Get Offers are best suited for cardholders that have low transaction activity. The goal is to encourage repeat usage, preferably in high-volume purchase categories such as gas, groceries, and dining. For example, “Get a promotional rate of 0% if you use your card five times or more to purchase gas or groceries.”", 
        5: "Recommendation for Segment 6: Include them in your standard email communication but regularly check if they don't flag your content as spam. Do not overspend on this segment. Cannot Lose Them But Losing Make limited time offers. Offer personalized recommendations Use and Get Offers are best suited for cardholders that have low transaction activity. The goal is to encourage repeat usage, preferably in high-volume purchase categories such as gas, groceries, and dining. For example, “Get a promotional rate of 0% if you use your card five times or more to purchase gas or groceries.”",
        1: "Recommendation for Segment 2: Responsive to promotions. Loyal Upsell higher value products. Ask for reviews.  Spend and Get Offers are appropriate for cardholders that have frequent, low-ticket purchases or who may be splitting spend across multiple cards. The goal is to get a higher share of wallet. For example, “Spend $3,000 or more over the next 30 days and get a $25 statement credit.”",
        2: "Recommendation for Segment 3: Offer membership or loyalty programs or recommend related products to upsell them and help them become your Loyalists or Champions. Offer membership / loyalty program. Keep them engaged. Offer personalized recommendations.",
        3: "Recommendation for Segment 4: Provide helpful resources on the site. Send personalized emails. probably using multiple accounts credit card .",
}
    return recommendations.get(cluster, "No specific recommendations for this segment.")

if st.button("Predict"):
    cluster = perform_clustering(user_input)
    st.write("Predicted Cluster:", cluster)
    st.write("Segment Description:", get_segment_description(cluster))
    st.write("Recommendations:", get_recommendations(cluster))