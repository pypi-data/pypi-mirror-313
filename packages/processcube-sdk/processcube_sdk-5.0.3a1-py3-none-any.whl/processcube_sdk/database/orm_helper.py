import numpy as np
import pandas
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, load_only

class ORMHelper(object):

    def __init__(self, connection_string):
        self._connection_string = connection_string

    def __get_columns_from_dataframe(self, pandas_dataframe):
        cols = []
        for col in pandas_dataframe.columns:
            cols.append(col)

        return cols

    def create_engine(self):
        engine = create_engine(self._connection_string)

        return engine

    def create_session(self):
        engine = self.create_engine()
        Session = sessionmaker(bind=engine)

        return Session()

    def merge_panda_records(self, orm_type, pandas_dataframe, session=None, **additional_fields):
        must_destroy_session = False
        if session is None:
            must_destroy_session = True
            session = self.create_session()

        columns = self.__get_columns_from_dataframe(pandas_dataframe)

        for _, row in pandas_dataframe.iterrows():
            fields = {}

            for column in columns:
                if row[column] is np.NaN or row[column] == 'NaN':
                    fields[column] = None
                else:
                    fields[column] = row[column]

            record = orm_type(**fields)
            session.merge(record)

        if must_destroy_session:
            session.commit()
            del session

    def query_as_pandas_dataframe(self, query, **additional):
        engine = self.create_engine()

        fields = additional.get('fields', None)

        if fields:
            query = query.options(load_only(*fields))

        df = pandas.read_sql(query.statement, engine)

        engine.dispose()
        del engine

        return df
