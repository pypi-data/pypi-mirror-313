import os
import pandas as pd
from azureml.studio.core.data_frame_schema import DataFrameSchema
from azureml.studio.core.io.data_frame_directory import load_data_frame_from_directory, DataFrameDirectory
from azureml.designer.modules.vowpal_wabbit.common.entry_param import EntryParam


class Dataset(metaclass=EntryParam):
    def __init__(self, df: pd.DataFrame, column_attributes=None, name: str = None):
        self.df = df
        self.name = name
        if column_attributes is None:
            self.column_attributes = self.build_column_attributes()
        else:
            self.column_attributes = column_attributes

    def get_column_type(self, col_key):
        return self.column_attributes[col_key].column_type

    def get_element_type(self, col_key):
        return self.column_attributes[col_key].element_type

    def build_column_attributes(self):
        self.column_attributes = DataFrameSchema.generate_column_attributes(df=self.df)
        return self.column_attributes

    @property
    def column_count(self):
        return self.df.shape[1]

    @property
    def row_count(self):
        return self.df.shape[0]

    @property
    def columns(self):
        return self.df.columns

    @classmethod
    def load(cls, load_from: str):
        if isinstance(load_from, (str, os.PathLike)):
            dfd = load_data_frame_from_directory(load_from_dir=load_from)
            return cls(df=dfd.data, column_attributes=dfd.schema_instance.column_attributes)
        elif isinstance(load_from, DataFrameDirectory):
            return cls(df=load_from.data, column_attributes=load_from.schema_instance.column_attributes)
        else:
            raise NotImplementedError(f"Cannot load data from {load_from} of type {type(load_from)}")
