from datetime import date, datetime
import math
import re

from mortgage_sim.simulation.calculations import generate, get_min_monthly_repayments
from mortgage_sim.simulation.tax_bracket import get_medicare_amount, get_taxed_amount_fy_25_26
import streamlit as st
import polars as pl
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from base64 import b64decode, b64encode
import json
from urllib.parse import unquote

def load_data(raw_url_input):
    decoded_url = unquote(raw_url_input)
    # 2. Extract only the valid Base64 characters
    # This ignores the b' and ' regardless of their position
    b64_match = re.search(r'[A-Za-z0-9+/=]{10,}', decoded_url)
    if b64_match:
        clean_b64 = b64_match.group()
        str_ = b64decode(clean_b64).decode()
        return json.loads(str_)
    return {}

if "first_load" not in st.session_state:
    # check for data attribute
    if qs := st.query_params.get("data"):
        data = load_data(qs)
        for key, val in data.items():
            if key == "start_date":
                st.session_state.start_date = datetime.fromisoformat(val)
                assert isinstance(st.session_state.start_date, datetime)
            else:
                setattr(st.session_state, key, val)
        

    # so we do not run this again
    st.session_state.first_load = True

def persist_in_url():
    d_ = {
        "salary": st.session_state.salary,
        "loan_amount": st.session_state.loan_amount,
        "interest_rate": st.session_state.interest_rate,
        "mortgage_percent": st.session_state.mortgage_percent,
        "start_date": st.session_state.start_date.isoformat(),
        "comparative_rent_cost": st.session_state.comparative_rent_cost,
    }
    d_encoded = str(b64encode(json.dumps(d_).encode()))
    st.query_params["data"] = d_encoded


st.set_page_config(layout="wide")
col1,col2 = st.columns([1,5])

DEFAULT_SALARY = 100_000

if "salary" not in st.session_state:
    st.session_state.salary = DEFAULT_SALARY

def handle_salary_slider_onchange():
    # main state
    st.session_state.salary = st.session_state.salary_slider

    # synchronise others
    st.session_state.salary_input = st.session_state.salary

    persist_in_url()

def handle_salary_input_onchange():
    # main state
    st.session_state.salary = st.session_state.salary_input

    # synchronise others
    st.session_state.salary_slider = st.session_state.salary

    persist_in_url()

with col1:
    st.subheader("Loan parameters")
    st.number_input(
        "Loan amount",
        min_value=100_000,
        max_value=10_000_000,
        value=st.session_state.get("loan_amount", 700_000),
        key="loan_amount",
        on_change=lambda: persist_in_url(),
    )
    st.number_input(
        "Loan term",
        min_value=10,
        max_value=35,
        value=st.session_state.get("loan_term",30),
        key="loan_term",
        on_change=lambda: persist_in_url(),
    )
    st.number_input(
        "Interest rate",
        min_value=0.1,
        max_value=30.0,
        value=st.session_state.get("interest_rate",5.0),
        key="interest_rate",
        on_change=lambda: persist_in_url(),
    )
    st.subheader("Salary")
    st.slider(
        "Select your salary", 
        max_value=300_000, 
        min_value=1, 
        value=st.session_state.get("salary", 100_000),
        key="salary_slider",
        on_change=handle_salary_slider_onchange,
    )
    st.number_input(
        "Enter a salary value",
        max_value=1_000_000, 
        min_value=1, 
        value=st.session_state.get("salary", 100_000),
        key="salary_input",
        on_change=handle_salary_input_onchange,
    )

    st.slider(
        "what % of income will you use on mortgage?",
        min_value=0,
        max_value=100,
        value=st.session_state.get("mortgage_percent", 50),
        key="mortgage_percent",
        on_change=lambda: persist_in_url()
    )

with col2:
    income = st.session_state.salary
    st.subheader("Income")
    taxed_amount = get_taxed_amount_fy_25_26(income)
    medicare_amount = get_medicare_amount(income)
    total_tax_amount = taxed_amount + medicare_amount
    net_income = income - total_tax_amount
    scol1,scol2,scol3,scol4 = st.columns([1,1,1,1])
    with scol1:
        st.metric("Net Income (annual)", value=net_income, format="dollar")
        st.metric("Base tax amount", value=taxed_amount, format="dollar")
    with scol2:
        st.metric("Net Income (month)", value=net_income/12, format="dollar")
        st.metric("Medicare amount", value=medicare_amount, format="dollar",)
    with scol3:
        st.metric("Net Income (fortnight)", value=net_income/(52/2), format="dollar")
        st.metric("Total tax amount", value=total_tax_amount, format="dollar",)
    with scol4:
        st.metric("Net Income (weekly)", value=net_income/(52), format="dollar")
        st.metric("MLS", value="N/A")


    st.header("Charts")
    scol1,scol2 = st.columns([2,4])
    minimum_repayments = get_min_monthly_repayments(
        principal=st.session_state.loan_amount,
        loan_term=st.session_state.loan_term,
        annual_interest_rate=st.session_state.interest_rate/100,
    )
    monthly_income=net_income/12
    percent_income_spent_on_mortgage = monthly_income* (st.session_state.mortgage_percent/100)
    extra_repayment=percent_income_spent_on_mortgage-minimum_repayments
    with scol1:
        st.metric("Minimum Repayments (month)", value=minimum_repayments, format="dollar")
        st.metric("Monthly Income put into Repayments", value=percent_income_spent_on_mortgage, format="dollar")
        st.metric("Extra money in offset", value=extra_repayment, format="dollar")
        st.metric("Money Left over", value=monthly_income-percent_income_spent_on_mortgage, format="dollar")
        if percent_income_spent_on_mortgage < minimum_repayments:
            st.badge("Does not meet required minimum", color="red")
        else:
            st.badge("Meets minimum requirement", color="green")

    with scol2:
        
        # pie chart
        data = {
            "Category": ["Min Repayment", "Extra Repayment", "Non Mortgage Expenses"],
            "Amount": [minimum_repayments, extra_repayment, (monthly_income-percent_income_spent_on_mortgage)]
        }
        df = pl.DataFrame(data)
        fig1 = px.pie(
            df,
            values="Amount",
            names="Category",
            color="Category",
            color_discrete_map={
                "Min Repayment": "#EF553B",    # A soft red
                "Extra Repayment": "#00CC96",  # A vibrant green
                "Non Mortgage Expenses": "#8A8C8F"    # A clean blue
            }
        )
        st.plotly_chart(fig1, use_container_width=True)


#
# deeper simulations and analysis
#
def init_df():
    st.session_state.dataframe = pl.DataFrame(schema={'offset_balance': pl.Float64, 'loan_balance': pl.Float64, 'interest_charged': pl.Float64, 'period_start': pl.Datetime(time_unit='us', time_zone=None), 'period_end': pl.Datetime(time_unit='us', time_zone=None), 'extra_injections': pl.Float64, 'pa_interest_rate': pl.Float64, 'monthly_repayments': pl.Int64, 'monthly_offset_added': pl.Int64, 'extra_money_from_minimum_repayment': pl.Float64, 'extra_money_from_monthly_contribution': pl.Int64, 'extra_money_overall': pl.Float64, 'time_elapsed': pl.Float64, 'interest_charged_per_day': pl.Float64})

def set_main_state(*args, **kwargs):
    results = generate(*args, **kwargs)
    st.session_state.dataframe = results
init_df()

st.header("Run deep Simulations")
st.date_input("start_date", value=st.session_state.get("start_date", datetime(2027,1,1)), key="start_date", on_change=lambda: persist_in_url())
st.number_input("comparative_rent_cost", value=st.session_state.get("comparative_rent_cost", 600), key="comparative_rent_cost", on_change=lambda: persist_in_url())
if st.button("Deep Simulation"):
    with st.spinner("simulating..."):
        set_main_state(
            principal=st.session_state.loan_amount,
            mortgage_start_date=st.session_state.start_date,
            loan_term=st.session_state.loan_term,
            interest_rate=st.session_state.interest_rate/100,
            monthly_offset_amount=percent_income_spent_on_mortgage,
            monthly_repayment=minimum_repayments,
        )
        persist_in_url()


col1, col2 = st.columns([2,1])
with col1:
    st.dataframe(st.session_state.dataframe)
with col2:

    # calculate total interest charged
    df = st.session_state.dataframe
    total_interest_charged = df.select("interest_charged").sum().item()
    st.metric(label="total interest charged", value=f"${total_interest_charged:.2f}")

    # Calculate the duration first, then extract the single value
    total_time_elapsed = (df.select("period_start").max() - df.select("period_start").min()).item()
    total_days = total_time_elapsed.days if total_time_elapsed else 0
    total_years = total_days // 365
    remaining_days = total_days % 365
    st.metric(label="total time_elapsed", value=f"{total_years}yrs {remaining_days}days")

    # calculating amortised cost in weekly terms
    total_weeks = math.ceil(total_days / 7) or 1
    st.metric(label="amortised weekly cost", value=f"${total_interest_charged/total_weeks:.2f}/week")

col1, col2 = st.columns([1,1])
# total interest rate charged
rent_charged_simulation = df\
    .select("period_start", "period_end")\
    .with_columns(
        num_weeks=((pl.col("period_end") - pl.col("period_start")) / pl.duration(weeks=1)).floor(),
        rent_pw=pl.lit(st.session_state.comparative_rent_cost),
    )\
    .with_columns(
        rent_per_month=pl.col("rent_pw")*pl.col("num_weeks")
    )\
    .with_columns(
        cumulative_rent=pl.col("rent_per_month").cum_sum()
    )
joined_df = df.join(rent_charged_simulation, on="period_start")
with col1:
    # plot offset balance, loan balance
    fig1 = px.line(df, x="period_start", y=["offset_balance", "loan_balance"], title="offset balance vs loan balance")
    st.plotly_chart(fig1, use_container_width=True)

    # interest charged vs rent 
    # complicated!!!
    # fig5 = px.line(joined_df, x="period_start", y=["cumulative_interest_charged", "cumulative_rent"], title="interest charged vs rent")
    joined_df=joined_df.with_columns(
        upper=np.maximum(joined_df["cumulative_rent"], joined_df["cumulative_interest_charged"]),
        lower=np.minimum(joined_df["cumulative_rent"], joined_df["cumulative_interest_charged"]),
    )
    fig5 = go.Figure()
    # invisible
    fig5.add_trace(go.Scatter(
        x=joined_df["period_start"],
        y=joined_df["cumulative_interest_charged"],
        line=dict(width=0), showlegend=False, hoverinfo='skip'
    ))
    # Fill from interest UP to the maximum (which is Rent when Rent is higher)
    fig5.add_trace(go.Scatter(
        x=joined_df['period_start'], y=joined_df['upper'],
        fill='tonexty', 
        fillcolor='rgba(0, 255, 0, 0.3)', # Green
        line=dict(width=0), name='Rent > Interest'
    ))
    # --- THE "RED" FILL (Rent < Interest) ---
    # Again, add the interest line as a invisible baseline
    fig5.add_trace(go.Scatter(
        x=joined_df['period_start'], y=joined_df['cumulative_interest_charged'],
        line=dict(width=0), showlegend=False, hoverinfo='skip'
    ))
    # Fill from interest DOWN to the minimum (which is Rent when Rent is lower)
    fig5.add_trace(go.Scatter(
        x=joined_df['period_start'], y=joined_df['lower'],
        fill='tonexty', 
        fillcolor='rgba(255, 0, 0, 0.3)', # Red
        line=dict(width=0), name='Interest > Rent'
    ))

    # --- 3. THE ACTUAL VISIBLE LINES ---
    fig5.add_trace(go.Scatter(
        x=joined_df['period_start'], y=joined_df['cumulative_rent'],
        line=dict(color='black', width=2), name='Cumulative Rent'
    ))
    fig5.add_trace(go.Scatter(
        x=joined_df['period_start'], y=joined_df['cumulative_interest_charged'],
        line=dict(color='light blue', width=2), name='Cumulative Interest'
    ))
    # Formatting
    fig5.update_layout(
        title="Rent vs Interest Comparison",
        xaxis_title="Period Start",
        yaxis_title="Total Amount ($)",
        hovermode="x unified",
        template="plotly_white"
    )
    st.plotly_chart(fig5, use_container_width=True)

with col2:
    # plot monthly interest charged
    fig2 = px.line(df, x="period_start", y=["interest_charged"], title="Interest charged (monthly rate) over time")
    st.plotly_chart(fig2, use_container_width=True)

    # 
    minmonth_df = joined_df.with_columns(
        min_monthly_repayments=get_min_monthly_repayments(
           pl.col("loan_balance").cast(pl.Float64),
           pl.col("loan_term").cast(pl.Int64),
           pl.col("pa_interest_rate").cast(pl.Float64),
        )
    )
    fig7 = px.line(minmonth_df, x="period_start", y=["rent_per_month", "min_monthly_repayments"], title="rent per month vs min_repayments")
    st.plotly_chart(fig7, use_container_width=True)