import streamlit as st
import pandas as pd

st.set_page_config(page_title="Stock Quality Screener", layout="wide")
st.title("Stock Quality Screener")

@st.cache_data
def load_data():
    return pd.read_parquet(r"df_miniapp.parquet")

df = load_data()

st.sidebar.header("Filter Criteria")

# Añado marcas de verificación para aplicar solo los filtros si lo desea el usuario. Si no
# hago esto, todos los filtros se aplican por defecto. Por ejemplo, las empresas que no dan
# dividendo desaparecen aunque el usuario no quiera usar el filtro con dividendo.
apply_roic = st.sidebar.checkbox("Filter by ROIC?")
if apply_roic:
    roic = st.sidebar.slider("Minimum ROIC", 0.0, 2.0, 0.0, 0.02)

apply_roe = st.sidebar.checkbox("Filter by ROE?")
if apply_roe:
    roe = st.sidebar.slider("Minimum ROE", 0.0, 2.0, 0.0, 0.02)

apply_revenue_cagr = st.sidebar.checkbox("Filter by Revenue growth?")
if apply_revenue_cagr:
    revenue_CAGR = st.sidebar.slider("Minimum revenue CAGR", -0.5, 1.0, 0.0, 0.02)

apply_operating_margin = st.sidebar.checkbox("Filter by Operating Margin?")
if apply_operating_margin:
    operative_margin = st.sidebar.slider("Minimum operative margin", 0.0, 1.0, 0.0, 0.02)

apply_gross_margin = st.sidebar.checkbox("Filter by Gross Margin?")
if apply_gross_margin:
    gross_margin = st.sidebar.slider("Minimum gross margin", 0.0, 1.0, 0.0, 0.02)

apply_gross_margin_growth = st.sidebar.checkbox("Filter by Gross Margin Growth (4Y)?")
if apply_gross_margin_growth:
    gross_margin_growth = st.sidebar.slider("Minimum gross margin growth", 0.0, 1.0, 0.0, 0.02)    

apply_operative_margin_growth = st.sidebar.checkbox("Filter by Operative Margin Growth (4Y)?")
if apply_operative_margin_growth:
    operative_margin_growth = st.sidebar.slider("Minimum operative margin growth", 0.0, 1.0, 0.0, 0.02)    

apply_dividend_growth = st.sidebar.checkbox("Filter by Dividend Growth (5Y)?")
if apply_dividend_growth:
    dividend_growth = st.sidebar.slider("Minimum dividend growth in 5Y", 0.0, 0.5, 0.0, 0.02)

apply_debt_ebitda = st.sidebar.checkbox("Filter by Debt/EBITDA?")
if apply_debt_ebitda:
    debt_ebitda = st.sidebar.slider("Maximum debt/EBITDA", 0.0, 6.0, 6.0, 0.1)

apply_capex_flow = st.sidebar.checkbox("Filter by capex per FCF?")
if apply_capex_flow:
    capex_flow = st.sidebar.slider("Maximum Capex/FCF", 0.0, 2.0, 0.0, 0.1)

apply_sector = st.sidebar.checkbox("Filter by Sector?")
if apply_sector:
    sector_selected = st.sidebar.multiselect("Sector", options=sorted(df["sector"].dropna().unique()))
else:
    sector_selected = []

# Aplica los cambios solo a al copia.
df_screened = df.copy()

# Aplicar filtros solo si están activados
if apply_roic:
    df_screened = df_screened[df_screened["roic"] >= roic]

if apply_roe:
    df_screened = df_screened[df_screened["roe"] >= roe]

if apply_revenue_cagr:
    df_screened = df_screened[df_screened["revenue_cagr"] >= revenue_CAGR]

if apply_operating_margin:
    df_screened = df_screened[df_screened["operating_margin"] >= operative_margin]

if apply_capex_flow:
    df_screened = df_screened[df_screened["capex_to_cashflow"] >= capex_flow]
    
if apply_gross_margin:
    df_screened = df_screened[df_screened["gross_margin"] >= gross_margin]

if apply_gross_margin_growth:
    df_screened = df_screened[df_screened["gross_margin_cagr"] >= gross_margin_growth]

if apply_operative_margin_growth:
    df_screened = df_screened[df_screened["operating_margin_cagr"] >= operative_margin_growth]

if apply_dividend_growth:
    df_screened = df_screened[df_screened["dividend_growth_5y"] >= dividend_growth]

if apply_debt_ebitda:
    df_screened = df_screened[df_screened["debt_ebitda"] <= debt_ebitda]

if apply_sector and sector_selected:
    df_screened = df_screened[df_screened["sector"].isin(sector_selected)]

st.subheader("Companies that fulfill the requirements")
df_screened = df_screened.set_index('company')
st.dataframe(df_screened, use_container_width=True)
