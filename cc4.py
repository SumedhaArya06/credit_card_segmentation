{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 4,
   "id": "1c982ce7",
   "metadata": {},
   "outputs": [
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "2024-01-30 05:37:15.633 \n",
      "  \u001b[33m\u001b[1mWarning:\u001b[0m to view this Streamlit app on a browser, run it with the following\n",
      "  command:\n",
      "\n",
      "    streamlit run C:\\Users\\sumedha\\AppData\\Roaming\\Python\\Python37\\site-packages\\ipykernel_launcher.py [ARGUMENTS]\n"
     ]
    }
   ],
   "source": [
    "import streamlit as st\n",
    "import pandas as pd\n",
    "import pickle\n",
    "\n",
    "with open(\"kmeans_model.pkl\", \"rb\") as file:\n",
    "    kmeans_model = pickle.load(file)\n",
    "\n",
    "st.title(\"Customer Segmentation with K-means Clustering\")\n",
    "\n",
    "st.header(\"User Input:\")\n",
    "balance = st.slider(\"Balance\", min_value=0.0, max_value=20000.0, step=100.0, value=1000.0)\n",
    "purchases = st.slider(\"Purchases\", min_value=0.0, max_value=50000.0, step=100.0, value=1000.0)\n",
    "oneoff_purchases = st.slider(\"One-Off Purchases\", min_value=0.0, max_value=50000.0, step=100.0, value=1000.0)\n",
    "installments_purchases = st.slider(\"Installments Purchases\", min_value=0.0, max_value=30000.0, step=100.0, value=1000.0)\n",
    "cash_advance = st.slider(\"Cash Advance\", min_value=0.0, max_value=50000.0, step=100.0, value=1000.0)\n",
    "credit_limit = st.slider(\"Credit Limit\", min_value=0.0, max_value=30000.0, step=100.0, value=10000.0)\n",
    "payments = st.slider(\"Payments\", min_value=0.0, max_value=50000.0, step=100.0, value=1000.0)\n",
    "prc_full_payment = st.slider(\"Percentage of Full Payment\", min_value=0.0, max_value=1.0, step=0.01, value=0.5)\n",
    "tenure = st.slider(\"Tenure\", min_value=0, max_value=20, step=1, value=10)\n",
    "credit_utilization = st.slider(\"Credit Utilization\", min_value=0.0, max_value=1.0, step=0.01, value=0.5)\n",
    "purchases_frequency = st.slider(\"Purchases Frequency\", min_value=0.0, max_value=1.0, step=0.01, value=0.5)\n",
    "purchases_instalments_frequency = st.slider(\"Purchases Instalments Frequency\", min_value=0.0, max_value=1.0, step=0.01, value=0.5)\n",
    "\n",
    "user_input = {\n",
    "    'BALANCE': balance,\n",
    "    'PURCHASES': purchases,\n",
    "    'ONEOFF_PURCHASES': oneoff_purchases,\n",
    "    'INSTALLMENTS_PURCHASES': installments_purchases,\n",
    "    'CASH_ADVANCE': cash_advance,\n",
    "    'CREDIT_LIMIT': credit_limit,\n",
    "    'PAYMENTS': payments,\n",
    "    'PRC_FULL_PAYMENT': prc_full_payment,\n",
    "    'TENURE': tenure,\n",
    "    'CREDIT_UTILIZATION': credit_utilization,\n",
    "    'PURCHASES_FREQUENCY': purchases_frequency,\n",
    "    'PURCHASES_INSTALLMENTS_FREQUENCY': purchases_instalments_frequency,\n",
    "}\n",
    "\n",
    "def perform_clustering(user_input):\n",
    "    def scale_user_input(user_input):\n",
    "        feature_ranges = {\n",
    "            'BALANCE': (0.0, 20000.0),\n",
    "            'PURCHASES': (0.0, 50000.0),\n",
    "            'ONEOFF_PURCHASES': (0.0, 50000.0),\n",
    "            'INSTALLMENTS_PURCHASES': (0.0, 30000.0),\n",
    "            'CASH_ADVANCE': (0.0, 50000.0),\n",
    "            'CREDIT_LIMIT': (0.0, 30000.0),\n",
    "            'PAYMENTS': (0.0, 50000.0),\n",
    "            'PRC_FULL_PAYMENT': (0.0, 1.0),\n",
    "            'TENURE': (0, 20),\n",
    "            'CREDIT_UTILIZATION': (0.0, 1.0),    \n",
    "            'PURCHASES_FREQUENCY': (0.0, 1.0) ,\n",
    "            'PURCHASES_INSTALLMENTS_FREQUENCY': (0.0, 1.0) \n",
    "        }\n",
    "\n",
    "        scaled_user_input = {feature: (user_input[feature] - min_val) / (max_val - min_val)\n",
    "                              for feature, (min_val, max_val) in feature_ranges.items()}\n",
    "\n",
    "        return pd.DataFrame(scaled_user_input, index=[0])\n",
    "\n",
    "    user_df_scaled = scale_user_input(user_input)\n",
    "\n",
    "    cluster = kmeans_model.predict(user_df_scaled)[0]\n",
    "    return cluster\n",
    "\n",
    "def get_segment_description(cluster):\n",
    "    segment_descriptions = {\n",
    "    0:  \"Segment 1: (Diamond): Champions-High Payments made by the user, Best Customers,  Bought frequently, High Credit Utilization, Potential Loyalist,s are your recent customers with average frequency and who spent a good amount..\",\n",
    "    4:  \"Segment 5: (Copper): Being the youngest customer, Low Payments,   Low frequency, Low Credit Utilization. \",\n",
    "    5:  \"Segment 6: (Bronze): Customers who made smaller and infrequent purchases before but haven't purchased anything in a long time. Low Payments Made good payment orders, High Balance. But frequency is low. Extremely Low Credit Utilization.\",\n",
    "    1:  \"Segment 2: (Platinum): High Balance High Payments made by the user, Frequency not High, Low Credit Utilization, Orders regularly..\",\n",
    "    2:  \"Segment 3: (Gold): Not high Balance, Spent reasonably good amount Bought frequently, Average Credit Utilization score. Recent customers who spent good amounts. Potential Loyalists .\",\n",
    "    3:  \"Segment 4: (Silver): High Payments made by the user, Bought frequently, Average Credit Utilization, Extremely Low Balance.\",\n",
    "    }\n",
    "    return segment_descriptions.get(cluster, \"Undefined Segment\")\n",
    "\n",
    "def get_recommendations(cluster):\n",
    "    recommendations = {\n",
    "        0: \"Recommendation for Segment 1: Offer membership or loyalty programs or recommend related products to upsell them and help them become your Loyalists or Champions. Reward Accelerators are effective for cardholders who are vested in your loyalty program. Bonus points or cash-back incentives encourage more frequent purchases and higher spend. For example, “Earn three times the points for all grocery purchases in the next 30 days,” or “Spend $3,000 or more and get 5% cash back”.\",\n",
    "        4: \"Recommendation for Segment 5: Make subject lines of emails very personalized. Revive their interest by a specific discount on a specific product. Win them back via renewals or newer products, don’t lose them to competition. Talk to them if necessary. Spend time on highest possible personalization.   Use and Get Offers are best suited for cardholders that have low transaction activity. The goal is to encourage repeat usage, preferably in high-volume purchase categories such as gas, groceries, and dining. For example, “Get a promotional rate of 0% if you use your card five times or more to purchase gas or groceries.”\", \n",
    "        5: \"Recommendation for Segment 6: Include them in your standard email communication but regularly check if they don't flag your content as spam. Do not overspend on this segment. Cannot Lose Them But Losing Make limited time offers. Offer personalized recommendations Use and Get Offers are best suited for cardholders that have low transaction activity. The goal is to encourage repeat usage, preferably in high-volume purchase categories such as gas, groceries, and dining. For example, “Get a promotional rate of 0% if you use your card five times or more to purchase gas or groceries.”\",\n",
    "        1: \"Recommendation for Segment 2: Responsive to promotions. Loyal Upsell higher value products. Ask for reviews.  Spend and Get Offers are appropriate for cardholders that have frequent, low-ticket purchases or who may be splitting spend across multiple cards. The goal is to get a higher share of wallet. For example, “Spend $3,000 or more over the next 30 days and get a $25 statement credit.”\",\n",
    "        2: \"Recommendation for Segment 3: Offer membership or loyalty programs or recommend related products to upsell them and help them become your Loyalists or Champions. Offer membership / loyalty program. Keep them engaged. Offer personalized recommendations.\",\n",
    "        3: \"Recommendation for Segment 4: Provide helpful resources on the site. Send personalized emails. probably using multiple accounts credit card .\",\n",
    "}\n",
    "    return recommendations.get(cluster, \"No specific recommendations for this segment.\")\n",
    "\n",
    "if st.button(\"Predict\"):\n",
    "    cluster = perform_clustering(user_input)\n",
    "    st.write(\"Predicted Cluster:\", cluster)\n",
    "    st.write(\"Segment Description:\", get_segment_description(cluster))\n",
    "    st.write(\"Recommendations:\", get_recommendations(cluster))"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.7.4"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
