from datetime import date, datetime, timedelta, time
import math
from dateutil.relativedelta import relativedelta
import polars as pl


############################
# heavy lifting functions
############################
SECONDS_IN_A_YEAR = 365.25*24*60*60

def get_all_offset_injection_dates():
    ALL_OFFSET_INJECTION_DATES = get_all_offset_transfer_dates()
    return ALL_OFFSET_INJECTION_DATES


# generate all payday dates
# given arbitrary date
def get_all_offset_transfer_dates() -> set:
  dates = []
  arbitrary_date = date(2025,5,31) # today


  # get all dates 1 fortnights prior to today spanning up to 2 years 
  lower_bound_date = arbitrary_date - timedelta(weeks=52*2)
  prior_dates = []
  cur_date = arbitrary_date
  while cur_date >= lower_bound_date:
    prior_dates.append(cur_date)
    cur_date -= timedelta(weeks=2)

  # get all dates 1 fortnight after this date, spanning 30 years
  upper_bound_date = arbitrary_date + timedelta(weeks=52*30)
  next_dates = []
  cur_date = arbitrary_date
  while cur_date <= upper_bound_date:
    next_dates.append(cur_date)
    cur_date += timedelta(weeks=2)
  
  return set(sorted(list(set([*prior_dates, *next_dates]))))


def get_min_monthly_repayments(principal, loan_term, annual_interest_rate):
    monthly_rate = annual_interest_rate/12
    one_plus_r_n = (1+monthly_rate)**(loan_term*12)
    return (
        principal*monthly_rate*(
            one_plus_r_n
            / (one_plus_r_n-1)
        )
    )


# PERIOD
def get_next_period(mortgage_start_date):
  """
  gets all periods starting from mortgage start date max 30 years
  """
  curr_month = mortgage_start_date
  for _ in range(30*12):
    prev_month = curr_month
    curr_month = curr_month + relativedelta(months=1)
    yield (prev_month, curr_month)


def date_in_period(date: datetime, period: tuple[datetime, datetime]):
  if date >= period[0] and date <= period[1]:
    return True
  return False

def generate_dates_in_period(period: tuple[datetime, datetime]) -> list[datetime]:
  dates = []
  start = period[0]
  end = period[1]
  cur = start
  while cur <= end:
    dates.append(cur)
    cur += timedelta(days=1)

  return dates


# INTEREST
def calculate_interest_daily(principle: float, interest_pa: float):
  interest_daily = interest_pa/365
  return principle * interest_daily

def calculate_interest_for_period(balance: float, period: tuple[datetime, datetime], interest_rate):
  """
  generate dates within the period
  for each date check if it matches a date_range in interest rates
  if so apply the daily interest calculations
  """
  interest_charged = 0
  for date in generate_dates_in_period(period):
    rate = interest_rate
    daily_charge = calculate_interest_daily(balance, rate)
    interest_charged += daily_charge

  return interest_charged




def generate(
    principal: int=700000,
    initial_offset: int = 0,
    mortgage_start_date=datetime(2027,1,1),
    loan_term=30,
    interest_rate=0.60,
    monthly_offset_amount=-999,
    monthly_repayment=-999,
):
    # things i want to change
    PRINCIPLE = principal
    INITIAL_OFFSET=initial_offset
    # MONTHLY_OFFSET_AMOUNT = (2000+600)*2 # how much gets transferred into offset

    # rolling variables
    # will change programatically
    ROLLING_OFFSET_BALANCE=INITIAL_OFFSET
    ROLLING_LOAN_BALANCE=PRINCIPLE
    MORTGAGE_START_DATE = mortgage_start_date
    if not isinstance(MORTGAGE_START_DATE, datetime):
       MORTGAGE_START_DATE = datetime.combine(MORTGAGE_START_DATE, time.min)
    assert isinstance(MORTGAGE_START_DATE, datetime), f"got {type(MORTGAGE_START_DATE)}"


    # can make more accurate by calculating interest based 
    # on actual balance on the date by iterating through balanace per day in period.
    records = []
    for period in get_next_period(MORTGAGE_START_DATE):
        ###################
        # charge interest #
        ###################
        start_date, end_date = period
        days = (end_date - start_date).days
        interest_calculatable_amount = ROLLING_LOAN_BALANCE - ROLLING_OFFSET_BALANCE
        interest_charged = calculate_interest_for_period(interest_calculatable_amount, period, interest_rate)
        interest_rate_current = interest_rate
        # apply interest
        ROLLING_LOAN_BALANCE += interest_charged

        offset_injection_amount = monthly_offset_amount
        ROLLING_OFFSET_BALANCE += offset_injection_amount

        # not tracked by simulator, just a "tracker function"        
        # extra_injections = get_extra_injections(period)
        # ROLLING_OFFSET_BALANCE += extra_injections

        #################################
        # BANK LOAN AUTOMATED REPAYMENT #
        #################################
        ROLLING_LOAN_BALANCE -= monthly_repayment
        ROLLING_OFFSET_BALANCE -= monthly_repayment

        records.append({
            # current state.
            "offset_balance": ROLLING_OFFSET_BALANCE,
            "loan_balance": ROLLING_LOAN_BALANCE,
            "interest_charged": interest_charged,
            "period_start": start_date,
            "period_end": end_date,
            # dynamically changing params
            "pa_interest_rate": interest_rate_current,
            "monthly_repayments": monthly_repayment,
            "monthly_offset_added": offset_injection_amount,
            # analysis fields
            "extra_money_from_minimum_repayment": monthly_repayment - interest_charged, # directly decreases loan amount
            "extra_money_from_monthly_contribution": offset_injection_amount - monthly_repayment, # increases offset account
            "extra_money_overall": offset_injection_amount - interest_charged, # this is the extra money regardless of whether it ends in offset or directly into mortgage.
            "time_elapsed": (end_date - MORTGAGE_START_DATE).total_seconds() / SECONDS_IN_A_YEAR,
            "loan_term": loan_term,
        })

        if ROLLING_OFFSET_BALANCE >= ROLLING_LOAN_BALANCE:
            break

    df = pl.DataFrame(records)

    # calculate interests charged per day (because interest charged is different for months with different number of days)
    total_days_in_month_expr = (pl.col("period_end").sub(pl.col("period_start"))).dt.total_days()
    df = df.with_columns(
        interest_charged_per_day=(
            (pl.col("interest_charged") / total_days_in_month_expr).round(2)
        )
    )
    # with cumulative sum of interest rates
    df = df.with_columns(
       cumulative_interest_charged=(
          pl.col("interest_charged").cum_sum()
       )
    )

    return df