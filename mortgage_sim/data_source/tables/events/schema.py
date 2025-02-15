from mortgage_sim.data_source.tables.schema import SchemaTemplate
import polars as pl


class EventsSchema(SchemaTemplate):
    @property
    def polars_schema(self):
        return {
            "id": pl.String(),
            "fk__recurring_payments": pl.String(),
            "fk__single_payments": pl.String(),
            # metadata
            "event_registered_timestamp": pl.Datetime(),
        }
