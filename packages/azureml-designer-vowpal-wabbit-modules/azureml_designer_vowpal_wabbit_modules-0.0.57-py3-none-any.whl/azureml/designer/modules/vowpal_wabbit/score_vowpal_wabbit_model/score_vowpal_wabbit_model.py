import os
from azureml.designer.modules.vowpal_wabbit.common.entry_param import Boolean
from azureml.designer.modules.vowpal_wabbit.common.vowpal_wabbit_model_wrapper import VowpalWabbitModelWrapper, \
    DataFormat, VowpalWabbitPredictor
from azureml.designer.modules.vowpal_wabbit.common.dataset import Dataset
from azureml.designer.modules.vowpal_wabbit.common.entry_utils import params_loader
from azureml.designer.modules.vowpal_wabbit.common.entry_param import MultiTypeParam
from azureml.studio.internal.error import ErrorMapping, NullOrEmptyError, InvalidDatasetError, \
    UnexpectedNumberOfColumnsError, TooFewRowsInDatasetError, InvalidColumnTypeError
from azureml.studio.core.schema import ColumnTypeName
from azureml.studio.core.io.data_frame_directory import DataFrameDirectory, load_data_frame_from_directory
from azureml.studio.core.logger import module_logger

DATASET_NAME = "Test data"
TRAINED_MODEL_PARAM_NAME = "Trained Vowpal Wabbit model"
NAME_OF_THE_TEST_DATA_PARAM = "Name of the test data file"


class ScoreVowpalWabbitModelModule:
    def __init__(self):
        self.vw_arguments = None
        self.include_an_extra_column_containing_labels = None
        self.include_an_extra_column_containing_raw_scores = None
        self.specify_file_type = None
        self.name_of_the_test_data_file = None

    @params_loader
    def on_init(self,
                vw_arguments,
                include_an_extra_column_containing_labels,
                include_an_extra_column_containing_raw_scores,
                specify_file_type,
                name_of_the_test_data_file):
        module_logger.info("On init parameters.")
        self.vw_arguments = vw_arguments
        self.include_an_extra_column_containing_labels = include_an_extra_column_containing_labels
        self.include_an_extra_column_containing_raw_scores = include_an_extra_column_containing_raw_scores
        self.specify_file_type = specify_file_type
        self.name_of_the_test_data_file = name_of_the_test_data_file

    def update_params(self,
                      vw_arguments=None,
                      include_an_extra_column_containing_labels=None,
                      include_an_extra_column_containing_raw_scores=None,
                      specify_file_type=None,
                      name_of_the_test_data_file=None):
        module_logger.info("Update parameters.")
        for attr_name, attr_value in locals().items():
            if attr_name != "self" and attr_value is not None:
                setattr(self, attr_name, attr_value)

    @staticmethod
    def _validate_test_dataset(test_dataset):
        test_dataset.name = DATASET_NAME
        ErrorMapping.verify_number_of_rows_greater_than_or_equal_to(curr_row_count=test_dataset.row_count,
                                                                    required_row_count=1,
                                                                    arg_name=test_dataset.name)
        ErrorMapping.verify_number_of_columns_equal_to(curr_column_count=test_dataset.column_count,
                                                       required_column_count=1, arg_name=test_dataset.name)
        ErrorMapping.verify_element_type(type_=test_dataset.get_column_type(0),
                                         expected_type=ColumnTypeName.STRING,
                                         column_name=test_dataset.columns[0], arg_name=test_dataset.name)

    def _prepare_dataset(self, test_data: str):
        """Prepare test data.

        Test data can be of two types:
        1. AnyDirectory, where there is a plain text file, named 'name_of_the_test_data_file'. Each line of this
        file is an example of VW/SVMLight format. For VW format details, please refer to:
        https://github.com/VowpalWabbit/vowpal_wabbit/wiki/Input-format
        2. DataFrameDirectory, which has only one column, and each row of which is an example with VW/SVMLight format.
        """
        if isinstance(test_data, DataFrameDirectory):
            module_logger.info(f"Receive test data as a DataFrameDirectory object.")
            test_dataset = Dataset(df=test_data.data, column_attributes=test_data.schema_instance.column_attributes,
                                   name=DATASET_NAME)
            return test_dataset

        ErrorMapping.verify_not_null_or_empty(x=test_data, name=DATASET_NAME)
        try:
            dfd = load_data_frame_from_directory(load_from_dir=test_data)
            test_dataset = Dataset(df=dfd.data, column_attributes=dfd.schema_instance.column_attributes,
                                   name=DATASET_NAME)
            module_logger.info("Loaded test data from DataFrameDirectory.")
            self._validate_test_dataset(test_dataset)
            return test_dataset
        except Exception as e:
            if isinstance(e, (TooFewRowsInDatasetError, InvalidColumnTypeError, UnexpectedNumberOfColumnsError)):
                raise e
            module_logger.warning(
                f"Failed to load the path as DataFrameDirectory, will try to load it as file dataset.")

        if os.path.isfile(test_data):
            # AnyDirectory can also be a file path
            return test_data
        elif os.path.isdir(test_data):
            if self.name_of_the_test_data_file is None:
                ErrorMapping.throw(NullOrEmptyError(
                    name=NAME_OF_THE_TEST_DATA_PARAM,
                    troubleshoot_hint='Load data from a directory without a test data file name specified.'))
            else:
                # if load dfd failed, then the input is an AnyDirectory, where test dataset file is specified
                test_dataset = os.path.join(test_data, self.name_of_the_test_data_file)
                if not os.path.exists(test_dataset):
                    ErrorMapping.throw(
                        InvalidDatasetError(dataset1=DATASET_NAME,
                                            reason=f'"{self.name_of_the_test_data_file}" does not exist'))
                if not os.path.isfile(test_dataset):
                    ErrorMapping.throw(
                        InvalidDatasetError(dataset1=DATASET_NAME,
                                            reason=f'"{self.name_of_the_test_data_file}" is not a file'))
                module_logger.info("Loaded test data from AnyDirectory.")
                return test_dataset
        else:
            raise InvalidDatasetError(dataset1=DATASET_NAME,
                                      reason=f"cannot load {test_data} as {type(test_data)} type.")

    @params_loader
    def run(self,
            trained_vowpal_wabbit_model: VowpalWabbitModelWrapper,
            test_data: MultiTypeParam(exp_types=(str, DataFrameDirectory)),
            include_an_extra_column_containing_labels: Boolean,
            include_an_extra_column_containing_raw_scores: Boolean,
            specify_file_type: DataFormat,
            vw_arguments: str = None,
            name_of_the_test_data_file: str = None,
            scored_dataset: str = None):
        self.update_params(vw_arguments=vw_arguments,
                           include_an_extra_column_containing_labels=include_an_extra_column_containing_labels,
                           include_an_extra_column_containing_raw_scores=include_an_extra_column_containing_raw_scores,
                           specify_file_type=specify_file_type,
                           name_of_the_test_data_file=name_of_the_test_data_file)
        test_dataset = self._prepare_dataset(test_data=test_data)
        ErrorMapping.verify_not_null_or_empty(x=trained_vowpal_wabbit_model, name=TRAINED_MODEL_PARAM_NAME)
        vw_predictor = VowpalWabbitPredictor(trained_vowpal_wabbit_model)
        scored_data_df = vw_predictor.predict(
            test_data=test_dataset, arg_str=self.vw_arguments,
            include_labels=self.include_an_extra_column_containing_labels,
            include_raw_predictions=self.include_an_extra_column_containing_raw_scores,
            data_format=self.specify_file_type)
        scored_data_dfd = DataFrameDirectory.create(data=scored_data_df)
        if scored_dataset is not None:
            scored_data_dfd.dump(save_to=scored_dataset)

        return scored_data_dfd,
