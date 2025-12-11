import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Belmont North Property Dashboard",
    layout="wide"
)

@st.cache_data
def load_data():
    df = pd.read_csv("belmont_north_market.csv")
    df["date"] = pd.to_datetime(df["date"], dayfirst=True)
    df = df[df["metric"] == "sell_price"].copy()
    df = df.sort_values("date").reset_index(drop=True)
    return df

df = load_data()

st.title("Belmont North Property Market Dashboard")
st.markdown(
    "This dashboard turns a long time series of suburb prices into a few simple views "
    "that are easy for residential property investors to understand."
)

df_sell = df[df["metric"] == "sell_price"].copy()

start = df_sell.iloc[0]["suburb_value"]
end = df_sell.iloc[-1]["suburb_value"]
growth = (end - start) / start * 100

years = (df_sell["date"].iloc[-1] - df_sell["date"].iloc[0]).days / 365
cagr = (end / start)**(1 / years) - 1

col1, col2, col3 = st.columns(3)
col1.metric("Start price", f"${start:,.0f}")
col2.metric("Latest price", f"${end:,.0f}")
col3.metric("Total growth", f"{growth:.1f}%")

col4, col5 = st.columns(2)
col4.metric("CAGR", f"{cagr*100:.2f}% per year")
col5.write("")

st.write("---")

tab1, tab2, tab3, tab4 = st.tabs(
    ["Growth vs region", "Houses vs units", "Premium vs SA3", "Rolling growth"]
)

# --------------------------------------------------
# TAB 1: Indexed growth vs region
# --------------------------------------------------
with tab1:
    st.subheader("Indexed price growth - suburb vs regional benchmarks")

    base = df.iloc[0]
    df_idx = df.copy()
    df_idx["suburb_index"] = df_idx["suburb_value"] / base["suburb_value"] * 100
    df_idx["cr_index"] = df_idx["cr_value"] / base["cr_value"] * 100
    df_idx["sa3_index"] = df_idx["sa3_value"] / base["sa3_value"] * 100

    yearly = df_idx.resample("A", on="date").mean(numeric_only=True).reset_index()

    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(yearly["date"], yearly["suburb_index"], label="Belmont North", linewidth=2)
    ax.plot(yearly["date"], yearly["cr_index"], label="CR benchmark", linestyle="--")
    ax.plot(yearly["date"], yearly["sa3_index"], label="SA3 benchmark", linestyle=":")
    ax.set_ylabel("Index (start = 100)")
    ax.set_xlabel("Year")
    ax.grid(True)
    ax.legend()
    st.pyplot(fig)

    st.markdown(
        """
### Insights

- **Belmont North has outperformed its regional benchmarks over the long term.**  
  While all three indexes trend upward, Belmont North’s price index has consistently accelerated since 2018, ending **above both CR and SA3 benchmarks**.

- **A structural shift occurs around 2020.**  
  Post-COVID market dynamics pushed all regions upward, but Belmont North shows a **sharper and more sustained growth trajectory**, indicating stronger buyer demand and tightening supply.

- **SA3 shows more volatility**, especially in the earlier periods.  
  This suggests the broader Lake Macquarie East market experienced larger swings than Belmont North, reinforcing the suburb’s **relative stability**.

- **Since 2022, Belmont North has closed the gap with SA3 and eventually matched or exceeded its performance.**  
  This implies the suburb is transitioning from an “affordable alternative” to a **growth-leading submarket** within the region.

- **Long-term compounding effect:**  
  Starting from the same 100 index baseline, Belmont North ends near **280+**, meaning prices have **nearly tripled**, outpacing CR and matching or beating SA3 over two decades.

Overall, the index comparison reinforces Belmont North as a **strong long-term performer** with  
both **resilience during downturns** and **strong acceleration during market upswings**.

        """
    )

# --------------------------------------------------
# TAB 2: Houses vs units
# --------------------------------------------------
with tab2:
    st.subheader("Houses vs units - two markets in one suburb")

    df_house = df[df["property_type"] == "house"].copy()
    df_unit = df[df["property_type"] == "unit"].copy()

    annual_house = (
        df_house.resample("A", on="date")
        .median(numeric_only=True)
        .reset_index()
    )
    annual_unit = (
        df_unit.resample("A", on="date")
        .median(numeric_only=True)
        .reset_index()
    )

    # 2.1 price levels
    fig2, ax2 = plt.subplots(figsize=(10, 4))
    ax2.plot(
        annual_house["date"],
        annual_house["suburb_value"],
        label="House",
        linewidth=2,
    )
    ax2.plot(
        annual_unit["date"],
        annual_unit["suburb_value"],
        label="Unit",
        linewidth=2,
    )
    ax2.set_ylabel("Median sell price ($)")
    ax2.set_xlabel("Year")
    ax2.grid(True)
    ax2.legend()
    st.pyplot(fig2)

    # 2.2 price ratio
    merged = annual_house[["date", "suburb_value"]].merge(
        annual_unit[["date", "suburb_value"]],
        on="date",
        suffixes=("_house", "_unit"),
        how="inner",
    )
    merged["house_unit_ratio"] = (
        merged["suburb_value_house"] / merged["suburb_value_unit"]
    )

    fig3, ax3 = plt.subplots(figsize=(10, 3))
    ax3.plot(merged["date"], merged["house_unit_ratio"])
    ax3.axhline(1, linestyle="--", color="grey")
    ax3.set_ylabel("House / unit price")
    ax3.set_xlabel("Year")
    ax3.grid(True)
    st.pyplot(fig3)

    st.markdown(
        """
### Insights

- **Houses significantly outperform units over the long term.**  
  Since 2004, median house prices have grown from ~$300k to nearly ~$1M, while units increased from ~$350k to the mid ~$500k range.  
  This shows a **much stronger capital growth trajectory** for detached houses.

- **Around 2020, the price gap widened sharply.**  
  During the COVID housing boom, house prices accelerated dramatically, while units showed **more modest, slower gains**.  
  This suggests rising demand for land, space, and lifestyle-oriented housing.

- **Units show price stagnation after 2023.**  
  While houses continued trending upward, unit prices flattened around ~$540k.  
  This reflects lower investor activity and weaker demand for smaller dwellings post-pandemic.

- **Houses are driving market momentum.**  
  The stronger appreciation and higher volatility of house prices imply that the **suburb’s growth is land-led**, reinforcing Belmont North’s appeal to families and owner-occupiers.

- **Affordability gap continues to widen.**  
  The price ratio has shifted from roughly **1:1.1 (2004)** to **1:1.7 (2024+)**, making units the relatively more affordable entry point but also the **lower-return asset class** historically.

Overall, Belmont North demonstrates a **clear premium on land and detached housing**, with houses providing **superior long-term capital growth** and units offering **stability but limited upside**.

        """
    )


# --------------------------------------------------
# TAB 4: Rolling 12-month growth
# --------------------------------------------------
with tab3:
    st.subheader("Rolling 12-month growth - momentum and risk profile")

    df_house = df[df["property_type"] == "house"].copy()
    df_house = df_house.sort_values("date").set_index("date")

    monthly = df_house.resample("M").median(numeric_only=True)
    monthly["suburb_12m_growth"] = monthly["suburb_value"].pct_change(12) * 100
    monthly["sa3_12m_growth"] = monthly["sa3_value"].pct_change(12) * 100

    fig5, ax5 = plt.subplots(figsize=(10, 4))
    ax5.axhline(0, color="grey", linestyle="--")
    ax5.plot(
        monthly.index,
        monthly["suburb_12m_growth"],
        label="Belmont North",
        linewidth=2,
    )
    ax5.plot(
        monthly.index,
        monthly["sa3_12m_growth"],
        label="SA3 benchmark",
        linestyle=":",
    )
    ax5.set_ylabel("12-month price change (%)")
    ax5.set_xlabel("Year")
    ax5.grid(True)
    ax5.legend()
    st.pyplot(fig5)

    st.markdown(
        """
### Insights

- **Belmont North consistently shows higher volatility than the broader SA3 region.**  
  The suburb experiences sharper ups and downs, suggesting it is a more momentum-driven micro-market.  
  This often occurs in family-oriented suburbs where turnover is low and individual sales have a stronger impact on medians.

- **Periods of outperformance repeat in clear cycles.**  
  Belmont North regularly enters growth phases that exceed the regional benchmark — notably around **2017–2018**, **2021**, and again in **2024+**.  
  These surges often align with broader buyer demand shifts toward lifestyle suburbs.

- **Downturns are also sharper at suburb level.**  
  In 2020 and 2022, Belmont North dipped more steeply than SA3 before recovering.  
  This reinforces that investors should expect **higher short-term volatility** despite strong long-term performance.

- **The current trend (2023–2024) is positive.**  
  Belmont North has shifted back into strong positive territory (approaching +20% YoY at times), while the SA3 region shows more moderate growth.  
  This indicates **renewed buyer demand specific to the suburb**, not just regional strength.

- **Crossing the 0% line acts like a momentum indicator.**  
  When the blue line rises from negative into positive (e.g., 2013, 2016, 2020–2021, 2023), it reliably signals the beginning of new growth cycles.  
  Belmont North is currently in one such upward phase.

Overall, this rolling growth view highlights that Belmont North is a **high-momentum suburb that rewards long-term holders**, with cycles that **outperform the region but fluctuate more intensely in the short run**.

        """
    )
