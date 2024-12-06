from dbt.adapters.record import RecordReplayHandle

from dbt.adapters.gaussdbdws.record.cursor.cursor import GaussDBDWSRecordReplayCursor


class GaussDBDWSRecordReplayHandle(RecordReplayHandle):
    """A custom extension of RecordReplayHandle that returns
    a psycopg-specific GaussDBDWSRecordReplayCursor object."""

    def cursor(self):
        cursor = None if self.native_handle is None else self.native_handle.cursor()
        return GaussDBDWSRecordReplayCursor(cursor, self.connection)
