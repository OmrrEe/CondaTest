import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Sales Dashboard", layout="wide")
st.title(" Sales Dashboard")

@st.cache_data
def load_data():
    df = pd.read_excel("sellers.xlsx")
    df["FULL NAME"] = df["NAME"] + " " + df["LASTNAME"]
    df["SALES AVERAGE %"] = (df["SALES AVERAGE"] * 100).round(2)
    return df

df = load_data()

# ── Sidebar filters ───────────────────────────────────────────────────────────
st.sidebar.header("Filters")

regions = ["All"] + sorted(df["REGION"].unique().tolist())
selected_region = st.sidebar.selectbox("Filter by Region", regions)

filtered = df if selected_region == "All" else df[df["REGION"] == selected_region]

vendors = ["All"] + sorted(filtered["FULL NAME"].unique().tolist())
selected_vendor = st.sidebar.selectbox("Filter by Vendor", vendors)

# ── Main table ────────────────────────────────────────────────────────────────
st.subheader(f"Sellers Table — {selected_region}")

display_cols = ["REGION", "ID", "NAME", "LASTNAME", "INCOME",
                "SOLD UNITS", "TOTAL SALES", "SALES AVERAGE %"]
st.dataframe(filtered[display_cols].reset_index(drop=True), use_container_width=True)

# ── Charts ────────────────────────────────────────────────────────────────────
st.subheader(" Charts by Seller")

chart_data = filtered.set_index("FULL NAME")

col1, col2, col3 = st.columns(3)

def bar_chart(ax, values, title, color, ylabel):
    ax.bar(values.index, values.values, color=color, edgecolor="white")
    ax.set_title(title, fontsize=13, fontweight="bold")
    ax.set_ylabel(ylabel)
    ax.tick_params(axis="x", rotation=45, labelsize=7)
    ax.spines[["top", "right"]].set_visible(False)

with col1:
    fig, ax = plt.subplots(figsize=(5, 4))
    bar_chart(ax, chart_data["SOLD UNITS"], "Units Sold", "#4C72B0", "Units")
    plt.tight_layout()
    st.pyplot(fig)

with col2:
    fig, ax = plt.subplots(figsize=(5, 4))
    bar_chart(ax, chart_data["TOTAL SALES"], "Total Sales", "#55A868", "MXN")
    plt.tight_layout()
    st.pyplot(fig)

with col3:
    fig, ax = plt.subplots(figsize=(5, 4))
    bar_chart(ax, chart_data["SALES AVERAGE %"], "Avg Sales %", "#C44E52", "%")
    plt.tight_layout()
    st.pyplot(fig)

# ── Vendor detail ─────────────────────────────────────────────────────────────
st.subheader(" Vendor Detail")

if selected_vendor != "All":
    vendor_row = filtered[filtered["FULL NAME"] == selected_vendor].iloc[0]
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Region", vendor_row["REGION"])
    c2.metric("Units Sold", f"{vendor_row['SOLD UNITS']:,}")
    c3.metric("Total Sales", f"${vendor_row['TOTAL SALES']:,}")
    c4.metric("Avg Sales", f"{vendor_row['SALES AVERAGE %']}%")

    st.markdown(f"**ID:** {vendor_row['ID']} &nbsp;|&nbsp; "
                f"**Income:** ${vendor_row['INCOME']:,}")
else:
    st.info("Select a specific vendor in the sidebar to see their detail card.")
