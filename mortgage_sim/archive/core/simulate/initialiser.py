from datetime import date
from pathlib import Path

from mortgage_sim.core.management.management import EventManager
from mortgage_sim.data_source.datasource import DataSource
from mortgage_sim.utils.asserts import assert_type


def initialise_environment(
    *,
    path: Path,
    initial_principle_amount: float,
    initial_interest: float,
    monthly_repayment: float,
    mortgage_start_date: date,
):
    assert_type(path, Path)
    assert_type(initial_principle_amount, float)
    assert_type(initial_interest, float)
    assert_type(monthly_repayment, float)
    assert_type(mortgage_start_date, date)

    ds = DataSource.init(path=path)
    em = EventManager(data_source=ds)

    if len(ds.events_table) > 0:
        raise AssertionError(
            "Cannot run initialise environment function",
            "datasource has already been initialised.",
        )

    _init_loan_params(
        event_manager=em,
        initial_principle_amount=initial_principle_amount,
        initial_interest=initial_interest,
        monthly_repayment=monthly_repayment,
    )


def _init_loan_params(
    *,
    event_manager: EventManager,
    initial_principle_amount: float,
    initial_interest: float,
    monthly_repayment: float,
):
    assert_type(event_manager, EventManager)
    assert_type(initial_principle_amount, float)
    assert_type(initial_interest, float)
    assert_type(monthly_repayment, float)

    event_manager.new_loan_parameter(
        principle_amount=initial_principle_amount,
        interest_rate=initial_interest,
        monthly_repayment=monthly_repayment,
    )

    if len(event_manager.data_source.loan_parameters_table.scan_csv().collect()) != 1:
        raise AssertionError("Loan Param Init Failed.")
