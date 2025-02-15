from mortgage_sim.data_source.tables.templates.schema import SchemaTemplate
import polars as pl


class EventsTableSchema(SchemaTemplate):
    @classmethod
    def get_polars_schema(self) -> dict[str, pl.DataType]:
        return {
            "id": pl.String(),
            "fk__recurring_payments": pl.String(),
            "fk__single_payments": pl.String(),
            # metadata
            "event_registered_timestamp": pl.Datetime(),
        }

    # python 3.13+ compatibility due
    # to @classmethod + @properties being discontinued

    # NOTE wrapped is required for instance methods
    # NOTE polars_schema = property(get_polars_schema.__wrapped__)
    # for classmethods wrapped is not required
    polars_schema = property(get_polars_schema)
