import matplotlib.pyplot as plt
import numpy as np
import plotly.graph_objects as go
import requests
import streamlit as st

st.title("📊 Options Greeks Analytics Platform")

# Inputs
S = st.slider("Stock Price", 50, 200, 100)
K = st.slider("Strike Price", 50, 200, 100)
T = st.slider("Time to Expiry (Years)", 0.1, 2.0, 1.0)
r = st.slider("Interest Rate", 0.01, 0.1, 0.05)
sigma = st.slider("Volatility", 0.1, 0.5, 0.2)
option_type = st.selectbox("Option Type", ["call", "put"])

# API call
response = requests.post("http://127.0.0.1:8000/calculate", json={
    "S": S, "K": K, "T": T, "r": r, "sigma": sigma, "option_type": option_type
})

data = response.json()

st.subheader("Greeks Output")
st.write(data)

# 3D Surface Plot (Delta)
st.subheader("3D Delta Surface")

S_range = np.linspace(50, 150, 30)
T_range = np.linspace(0.1, 2, 30)

Z = []

for t in T_range:
    row = []
    for s in S_range:
        res = requests.post("http://127.0.0.1:8000/calculate", json={
            "S": float(s), "K": K, "T": float(t), "r": r, "sigma": sigma, "option_type": option_type
        }).json()
        row.append(res["delta"])
    Z.append(row)

fig = go.Figure(data=[go.Surface(z=Z, x=S_range, y=T_range)])
fig.update_layout(title="Delta Surface", scene=dict(
    xaxis_title='Stock Price',
    yaxis_title='Time',
    zaxis_title='Delta'
))

st.plotly_chart(fig)

# Strategy Builder (Straddle)
st.subheader("📈 Straddle Strategy Payoff")

def straddle(S, K, premium=5):
    return max(S-K,0)-premium + max(K-S,0)-premium

prices = np.linspace(50,150,100)
payoffs = [straddle(p,K) for p in prices]

plt.figure()
plt.plot(prices, payoffs)
plt.axhline(0)
plt.title("Straddle Payoff")
plt.xlabel("Stock Price")
plt.ylabel("Profit/Loss")

st.pyplot(plt)