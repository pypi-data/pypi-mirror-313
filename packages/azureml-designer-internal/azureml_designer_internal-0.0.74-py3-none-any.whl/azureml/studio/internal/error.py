import inspect
import os
from io import StringIO
from enum import IntEnum
from typing import Union
from xml.etree import ElementTree

from azureml.studio.core.utils.jsonutils import dump_to_json
from azureml.studio.core.logger import LogFormatter
from azureml.studio.core.utils.strutils import get_args_from_template, remove_suffix, truncate_string
from .types import is_null_or_empty

_DIR_NAME = os.path.dirname(os.path.realpath(__file__))
EXCEPTION_FILE_NAME = os.path.join(_DIR_NAME, "Exceptions.xml")
CUSTOMER_SUPPORT_GUIDANCE = "Please contact product team by submit a feedback. " \
                            "You can submit a feedback by clicking the face icon on top right corner of the page. "


class ErrorType:
    NO_ERROR = 'NoException'
    LIBRARY_ERROR = 'LibraryException'
    MODULE_ERROR = 'ModuleException'


class ErrorInfo:
    # This limit must less than the limit of the whole error_info.json,
    # because when saving error_info.json, the data is {'Exception': error_info}.
    MAX_LENGTH = 9000
    MAX_MESSAGE_LENGTH = 4096

    def __init__(self, error):
        self._error = error

    @property
    def exception_type(self):
        raise NotImplementedError

    @property
    def error_id(self):
        return self._error.id.name

    @property
    def error_code(self):
        return self._error.id.value

    @property
    def message(self):
        return f'{self.error_id}: {self._error.__str__()}'

    @property
    def traceback(self):
        cause = self._error
        exc_info = (type(cause), cause, cause.__traceback__)
        # Not use ExceptionFormatter, since LogFormatter is more graceful, which falls back to
        # logging.Formatter.formatException method when ExceptionFormatter fails.
        return LogFormatter().formatException(exc_info=exc_info)

    def to_dict(self):
        result = {
            'ErrorId': self.error_id,
            'ErrorCode': self.error_code,
            'ExceptionType': self.exception_type,
            'Traceback': "",  # Traceback field hasn't been used in SMT, we can get the traces from driver logs.
            'Message': self.message
        }
        with StringIO() as f:
            dump_to_json(result, f)
            dump_len = len(f.getvalue())
        # Check whether the result exceeds the max length.
        if dump_len < self.MAX_LENGTH:
            return result

        # Truncate the Message with MAX_MESSAGE_LENGTH since user could get full message in driver logs
        result['Message'] = truncate_string(result['Message'], self.MAX_MESSAGE_LENGTH)
        return result


class ModuleErrorInfo(ErrorInfo):
    @property
    def exception_type(self):
        return ErrorType.MODULE_ERROR


class UserErrorInfo(ErrorInfo):
    @property
    def error_id(self):
        return ErrorId.UserError.name

    @property
    def error_code(self):
        return ErrorId.UserError.value

    @property
    def exception_type(self):
        return ErrorType.MODULE_ERROR


class LibraryErrorInfo(ErrorInfo):
    @property
    def exception_type(self):
        return ErrorType.LIBRARY_ERROR

    @property
    def error_id(self):
        return type(self._error).__name__

    @property
    def error_code(self):
        return LibraryExceptionError(self._error).id.value

    @property
    def message(self):
        return f'Library Error - {self.error_id}: {self._error.__str__()}'


class ErrorId(IntEnum):
    ColumnNotFound = 1
    ParameterParsing = 2
    NullOrEmpty = 3
    GreaterThan = 4
    GreaterThanOrEqualTo = 5
    LessThan = 6
    LessThanOrEqualTo = 7
    NotInRangeValue = 8
    IncorrectAzureStorageOrContainer = 9
    NotEqualColumnNames = 10
    NoColumnsSelected = 11
    UntrainedModel = 12
    InvalidLearner = 13
    ColumnUniqueValuesExceeded = 14
    ErrorDatabaseConnection = 15
    NotCompatibleColumnTypes = 16
    InvalidColumnType = 17
    InvalidDataset = 18
    NotSortedValues = 19
    TooFewColumnsInDataset = 20
    TooFewRowsInDataset = 21
    BadNumberOfSelectedColumns = 22
    InvalidTargetColumn = 23
    NotLabeledDataset = 24
    NotScoredDataset = 25
    EqualColumnNames = 26
    InconsistentSize = 27
    DuplicatedColumnName = 28
    InvalidUri = 29
    CouldNotDownloadFile = 30
    TooFewColumnsSelected = 31
    NaN = 32
    Infinity = 33
    MoreThanOneRating = 34
    MissingFeatures = 35
    DuplicateFeatureDefinition = 36
    MultipleLabelColumns = 37
    FailedToCompleteOperation = 39
    CouldNotConvertColumn = 42
    CannotDeriveElementType = 44
    MixedColumn = 45
    InvalidPathForDirectoryCreation = 46
    TooFewFeatureColumnsInDataset = 47
    CouldNotOpenFile = 48
    FileParsingFailed = 49
    IncorrectAzureStorageKey = 52
    NoUserFeaturesOrItemsFound = 53
    InvalidColumnCategorySelected = 56
    AlreadyExists = 57
    NotExpectedLabelColumn = 58
    ColumnIndexParsing = 59
    InvalidColumnIndexRange = 60
    ColumnCountNotEqual = 61
    LearnerTypesNotCompatible = 62
    IncorrectAzureStorageOrKey = 64
    IncorrectAzureBlobName = 65
    UnableToUploadToAzureBlob = 66
    UnexpectedNumberOfColumns = 67
    InvalidHiveScript = 68
    InvalidSQLScript = 69
    AzureTableNotExist = 70
    TimeoutOccured = 72
    ErrorConvertingColumn = 73
    InvalidBinningFunction = 75
    UnsupportedBlobWriteMode = 77
    HttpRedirectionNotAllowed = 78
    IncorrectAzureContainer = 79
    ColumnWithAllMissings = 80
    PCASparseDatasetWrongDimensionsNumber = 81
    UnableToDeserializeModel = 82
    InvalidTrainingDataset = 83
    UnableToEvaluateCustomModel = 84
    FailedToEvaluateScript = 85
    FailedToCreateHiveTable = 90
    InvalidZipFile = 102
    UnsupportedParameterType = 105
    UnsupportedOutputType = 107
    SchemaDoesNotMatch = 125
    ImageExceedsLimit = 127
    NumberOfUnconditionalProbabilitiesExceedsLimit = 128
    ExceedsColumnLimit = 129
    LabelColumnDoesNotHaveLabeledPoints = 134
    ModuleOutOfMemory = 138
    NotEnoughNormalizedColumns = 141
    JoinOnIncompatibleColumnTypes = 154
    ColumnNamesNotString = 155
    FailedToReadAzureSQLDatabase = 156
    IncorrectAzureMLDatastore = 157
    InvalidTransformationDirectory = 158
    InvalidModelDirectory = 159
    FailedToWriteOutputs = 160
    FailedJoinOperation = 161
    FailedToDownloadFiles = 162
    ComponentDeprecated = 163
    LibraryException = 1000
    UserError = 2000

    @staticmethod
    def from_name(name):
        """Given a name of ErrorId, find a corresponding item in ErrorId enum.

        :param name: The name of ErrorId.
        :return: The corresponding item in ErrorId enum.
        """
        for e in ErrorId:
            if e.name == name:
                return e
        else:
            raise ValueError(f"Unrecognized ErrorId: {name}")

    @staticmethod
    def from_class_name(class_name):
        """Given a class name of ModuleError, find the corresponding ErrorId for it.

        Assumes that the error class name is named as '{ErrorId.name}Error'.

        :param class_name: The name of ErrorId.
        :return: The corresponding item in ErrorId enum.
        """
        name = remove_suffix(class_name, suffix='Error')
        return ErrorId.from_name(name)


class AlghostRuntimeError(Exception):
    """
    General exception inside alghost. (Internal Server Error for DS)
    """

    def __init__(self, message):
        super().__init__(message)


doc = ElementTree.parse(EXCEPTION_FILE_NAME)


class ErrorMetaClass(type):
    """
    This metaclass is designed to check whether the error classes are defined correctly according to xml file.
    """

    def __new__(mcs, name, bases, namespace, **kargs):
        # Only check subclasses, do not check for base class.
        if name != 'ModuleError':
            init_func = namespace.get('__init__')
            mcs._check_class_definition_is_suitable_to_xml_file(name, init_func)

        return super().__new__(mcs, name, bases, namespace)

    @classmethod
    def _check_class_definition_is_suitable_to_xml_file(mcs, class_name, init_func):
        if not class_name.endswith('Error'):
            raise ValueError(f"Bad class name '{class_name}'. Must end with 'Error'.")

        # Will raise if err_id not found
        err_id = ErrorId.from_class_name(class_name)

        # Check the entry in xml
        err_name = err_id.name
        messages = doc.find(f"Exception[@id='{err_name}']/Messages")
        if not messages:
            raise ValueError(f"No xml entry found for {err_name}.")

        keywords_in_init_func = mcs._get_arg_names_of_func(init_func)

        for m in messages:
            if m.tag == 'Message':
                keywords_in_template = get_args_from_template(m.text)
                for keyword in keywords_in_template:
                    if keyword not in keywords_in_init_func:
                        raise ValueError(f"Argument '{keyword}' found in xml message,"
                                         f" but does not exist in {class_name}.__init__ method as a param."
                                         f" Maybe a typo?")

    @staticmethod
    def _get_arg_names_of_func(func):
        spec = inspect.getfullargspec(func)

        result = spec.args
        result.remove('self')

        if spec.varkw:
            result.extend(spec.varkw)

        if spec.kwonlyargs:
            result.extend(spec.kwonlyargs)

        return tuple(result)


class ModuleError(Exception, metaclass=ErrorMetaClass):
    def __init__(self, *args, **kwargs):
        class_name = type(self).__name__
        self.id = ErrorId.from_class_name(class_name)

        message = self._format_with_keyword_args(kwargs)
        if not message:
            raise ValueError(f"Argument names {list(kwargs.keys())} of error class {class_name} "
                             f"do not match with exception templates")

        self.message = message
        super().__init__(message)

    def _format_with_keyword_args(self, kwargs: dict):
        # If no argument is given, return default message
        if not kwargs:
            default_message = doc.findall(f"Exception[@code='{self.id.value}']/Messages/Default")
            if default_message:
                return default_message[0].text
            return None

        messages = doc.findall(f"Exception[@code='{self.id.value}']/Messages/Message")
        for m in messages:
            keywords_in_template = get_args_from_template(m.text)
            keywords_in_kwargs = tuple(kwargs.keys())
            if set(keywords_in_template) == set(keywords_in_kwargs):
                return m.text.format(**kwargs)
        return None

    def __str__(self):
        return self.message


class ColumnNotFoundError(ModuleError):
    def __init__(self, column_id: str = None, column_names: list = None, arg_name_missing_column: str = None,
                 arg_name_has_column: str = None):
        super().__init__(**_valid_kwargs(locals()))


class ParameterParsingError(ModuleError):
    def __init__(self, arg_name_or_column: str = None, to_type: str = None, from_type: str = None, arg_value=None,
                 fmt: str = None):
        super().__init__(**_valid_kwargs(locals()))


class NullOrEmptyError(ModuleError):
    def __init__(self, name: str = None, troubleshoot_hint: str = None):
        super().__init__(**_valid_kwargs(locals()))


class GreaterThanError(ModuleError):
    def __init__(self, arg_name: str = None, lower_boundary=None, actual_value=None):
        super().__init__(**_valid_kwargs(locals()))


class GreaterThanOrEqualToError(ModuleError):
    def __init__(self, arg_name: str = None, lower_boundary=None, value=None):
        super().__init__(**_valid_kwargs(locals()))


class LessThanError(ModuleError):
    def __init__(self, arg_name: str = None, upper_boundary_parameter_name=None, value=None):
        super().__init__(**_valid_kwargs(locals()))


class LessThanOrEqualToError(ModuleError):
    def __init__(self, arg_name: str = None, actual_value=None, upper_boundary_parameter_name: str = None,
                 upper_boundary=None, upper_boundary_meaning: str = None):
        super().__init__(**_valid_kwargs(locals()))


class NotInRangeValueError(ModuleError):
    def __init__(self, arg_name: str = None, lower_boundary=None, upper_boundary=None, reason: str = None):
        super().__init__(**_valid_kwargs(locals()))


class IncorrectAzureStorageOrContainerError(ModuleError):
    def __init__(self, account_name, container_name):
        super().__init__(**_valid_kwargs(locals()))


class NotEqualColumnNamesError(ModuleError):
    def __init__(self, col_index, dataset1, dataset2):
        super().__init__(**_valid_kwargs(locals()))


class NoColumnsSelectedError(ModuleError):
    def __init__(self, column_set: str = None):
        super().__init__(**_valid_kwargs(locals()))


class UntrainedModelError(ModuleError):
    def __init__(self, arg_name=None):
        super().__init__(**_valid_kwargs(locals()))


class InvalidLearnerError(ModuleError):
    def __init__(self, arg_name: str = None, learner_type: str = None, exception_message: str = None,
                 troubleshoot_hint: str = None):
        super().__init__(**_valid_kwargs(locals()))


class ColumnUniqueValuesExceededError(ModuleError):
    def __init__(self, column_name=None, limitation=None, troubleshoot_hint: str = None):
        super().__init__(**_valid_kwargs(locals()))


class ErrorDatabaseConnectionError(ModuleError):
    def __init__(self, connection_str):
        super().__init__(**_valid_kwargs(locals()))


class NotCompatibleColumnTypesError(ModuleError):
    def __init__(self, first_col_names: str = None, second_col_names: str = None,
                 first_dataset_names: str = None, second_dataset_names: str = None):
        super().__init__(**_valid_kwargs(locals()))


class InvalidColumnTypeError(ModuleError):
    def __init__(self, col_type: Union[type, str] = None, col_name: str = None, arg_name: str = None,
                 reason: str = None, troubleshoot_hint: str = None):
        super().__init__(**_valid_kwargs(locals()))


class InvalidDatasetError(ModuleError):
    def __init__(self, dataset1: str = None, dataset2: str = None, reason: str = None,
                 invalid_data_category: str = None, troubleshoot_hint: str = None):
        super().__init__(**_valid_kwargs(locals()))


class NotSortedValuesError(ModuleError):
    def __init__(self, col_index=None, dataset=None, arg_name=None, sorting_order=None):
        super().__init__(**_valid_kwargs(locals()))


class TooFewColumnsInDatasetError(ModuleError):
    def __init__(self, arg_name: str = None, required_columns_count: int = None):
        super().__init__(**_valid_kwargs(locals()))


class TooFewRowsInDatasetError(ModuleError):
    def __init__(self, arg_name: str = None, required_rows_count: int = None, actual_rows_count: int = None,
                 row_type: str = None, reason: str = None, troubleshoot_hint: str = None):
        """

        :param arg_name: dataset name
        :param required_rows_count: the minimum row required.
        :param actual_rows_count: the number of (valid) row instances.
        :param row_type: works as attribute to modify row in error message
        :param reason: the reason of error message
        """
        super().__init__(**_valid_kwargs(locals()))


class BadNumberOfSelectedColumnsError(ModuleError):
    def __init__(self, selection_pattern_friendly_name: str = None,
                 expected_col_count: int = None, selected_col_count: int = None):
        super().__init__(**_valid_kwargs(locals()))


class InvalidTargetColumnError(ModuleError):
    def __init__(self, column_index, learner_type: str = None):
        super().__init__(**_valid_kwargs(locals()))


class NotLabeledDatasetError(ModuleError):
    def __init__(self, dataset_name: str = None, troubleshoot_hint: str = None):
        super().__init__(**_valid_kwargs(locals()))


class NotScoredDatasetError(ModuleError):
    def __init__(self, dataset_name: str = None, learner_type: str = None, column_name: str = None,
                 troubleshoot_hint: str = None):
        super().__init__(**_valid_kwargs(locals()))


class EqualColumnNamesError(ModuleError):
    def __init__(self, arg_name_1: str = None, arg_name_2: str = None):
        super().__init__(**_valid_kwargs(locals()))


class InconsistentSizeError(ModuleError):
    def __init__(self, friendly_name1: str = None, friendly_name2: str = None):
        super().__init__(**_valid_kwargs(locals()))


class DuplicatedColumnNameError(ModuleError):
    def __init__(self, duplicated_name: str = None, arg_name: str = None, details: str = None):
        super().__init__(**_valid_kwargs(locals()))


class InvalidUriError(ModuleError):
    def __init__(self, invalid_url=None, message: str = None):
        super().__init__(**_valid_kwargs(locals()))


class CouldNotDownloadFileError(ModuleError):
    def __init__(self, file_url=None):
        super().__init__(**_valid_kwargs(locals()))


class TooFewColumnsSelectedError(ModuleError):
    def __init__(self, arg_name: str = None, input_columns_count: int = None, required_columns_count: int = None):
        super().__init__(**_valid_kwargs(locals()))


class NaNError(ModuleError):
    def __init__(self, arg_name: str = None):
        super().__init__(**_valid_kwargs(locals()))


class InfinityError(ModuleError):
    def __init__(self, arg_name: str = None, column_name: str = None):
        super().__init__(**_valid_kwargs(locals()))


class MoreThanOneRatingError(ModuleError):
    def __init__(self, user: str = None, item: str = None, dataset=None):
        super().__init__(**_valid_kwargs(locals()))


class MissingFeaturesError(ModuleError):
    def __init__(self, required_feature_name=None):
        super().__init__(**_valid_kwargs(locals()))


class DuplicateFeatureDefinitionError(ModuleError):
    def __init__(self, duplicated_name: str = None, dataset: str = None, troubleshoot_hint: str = None):
        super().__init__(**_valid_kwargs(locals()))


class MultipleLabelColumnsError(ModuleError):
    def __init__(self, dataset_name: str = None):
        super().__init__(**_valid_kwargs(locals()))


class FailedToCompleteOperationError(ModuleError):
    def __init__(self, failed_operation: str = None, reason: str = None):
        super().__init__(**_valid_kwargs(locals()))


class CouldNotConvertColumnError(ModuleError):
    def __init__(self, type1: Union[type, str], type2: Union[type, str],
                 col_name1: str = None, col_name2: str = None):
        super().__init__(**_valid_kwargs(locals()))


class CannotDeriveElementTypeError(ModuleError):
    def __init__(self, column_name: str = None, dataset_name: str = None):
        super().__init__(**_valid_kwargs(locals()))


class MixedColumnError(ModuleError):
    def __init__(self, column_id: int = None, row_1: int = None, type_1: type = None, row_2: int = None,
                 type_2: type = None, chunk_id_1: int = None, chunk_id_2: int = None, chunk_size: int = None):
        super().__init__(**_valid_kwargs(locals()))


class InvalidPathForDirectoryCreationError(ModuleError):
    def __init__(self, path):
        super().__init__(**_valid_kwargs(locals()))


class TooFewFeatureColumnsInDatasetError(ModuleError):
    def __init__(self, required_columns_count: int = None, arg_name: str = None):
        super().__init__(**_valid_kwargs(locals()))


class CouldNotOpenFileError(ModuleError):
    def __init__(self, file_name, exception=None):
        super().__init__(**_valid_kwargs(locals()))


class FileParsingFailedError(ModuleError):
    def __init__(self, file_format, file_name=None, failure_reason=None):
        super().__init__(**_valid_kwargs(locals()))


class IncorrectAzureStorageKeyError(ModuleError):
    def __init__(self):
        super().__init__(**_valid_kwargs(locals()))


class NoUserFeaturesOrItemsFoundError(ModuleError):
    def __init__(self):
        super().__init__(**_valid_kwargs(locals()))


class InvalidColumnCategorySelectedError(ModuleError):
    def __init__(self, col_name: str = None, troubleshoot_hint: str = None):
        super().__init__(**_valid_kwargs(locals()))


class AlreadyExistsError(ModuleError):
    def __init__(self, file_path: str = None):
        super().__init__(**_valid_kwargs(locals()))


class NotExpectedLabelColumnError(ModuleError):
    def __init__(self, dataset_name: str = None, column_name: str = None, reason: str = None,
                 troubleshoot_hint: str = None):
        super().__init__(**_valid_kwargs(locals()))


class ColumnIndexParsingError(ModuleError):
    def __init__(self, column_index_or_range=None):
        super().__init__(**_valid_kwargs(locals()))


class InvalidColumnIndexRangeError(ModuleError):
    def __init__(self, column_range=None):
        super().__init__(**_valid_kwargs(locals()))


class ColumnCountNotEqualError(ModuleError):
    def __init__(self, chunk_id_1=None, chunk_id_2=None, chunk_size=None,
                 filename_1=None, filename_2=None, column_count_1=None, column_count_2=None):
        super().__init__(**_valid_kwargs(locals()))


class LearnerTypesNotCompatibleError(ModuleError):
    def __init__(self, actual_learner_type=None, expected_learner_type_list=None):
        super().__init__(**_valid_kwargs(locals()))


class IncorrectAzureStorageOrKeyError(ModuleError):
    def __init__(self, account_name=None):
        super().__init__(**_valid_kwargs(locals()))


class IncorrectAzureBlobNameError(ModuleError):
    def __init__(self, blob_name=None, blob_name_prefix=None, container_name=None, blob_wildcard_path=None):
        super().__init__(**_valid_kwargs(locals()))


class UnableToUploadToAzureBlobError(ModuleError):
    def __init__(self, source_path, dest_path):
        super().__init__(**_valid_kwargs(locals()))


class UnexpectedNumberOfColumnsError(ModuleError):
    def __init__(self, dataset_name: str = None, expected_column_count: int = None, actual_column_count: int = None):
        super().__init__(**_valid_kwargs(locals()))


class InvalidHiveScriptError(ModuleError):
    def __init__(self):
        super().__init__(**_valid_kwargs(locals()))


class InvalidSQLScriptError(ModuleError):
    def __init__(self, sql_query, exception=None):
        super().__init__(**_valid_kwargs(locals()))


class AzureTableNotExistError(ModuleError):
    def __init__(self, table_name: str = None):
        super().__init__(**_valid_kwargs(locals()))


class TimeoutOccuredError(ModuleError):
    def __init__(self):
        super().__init__(**_valid_kwargs(locals()))


class ErrorConvertingColumnError(ModuleError):
    def __init__(self, target_type=None):
        super().__init__(**_valid_kwargs(locals()))


class InvalidBinningFunctionError(ModuleError):
    def __init__(self):
        super().__init__(**_valid_kwargs(locals()))


class UnsupportedBlobWriteModeError(ModuleError):
    def __init__(self, blob_write_mode: str = None):
        super().__init__(**_valid_kwargs(locals()))


class HttpRedirectionNotAllowedError(ModuleError):
    def __init__(self):
        super().__init__(**_valid_kwargs(locals()))


class IncorrectAzureContainerError(ModuleError):
    def __init__(self, container_name: str = None):
        super().__init__(**_valid_kwargs(locals()))


class ColumnWithAllMissingsError(ModuleError):
    def __init__(self, col_index_or_name=None):
        super().__init__(**_valid_kwargs(locals()))


class PCASparseDatasetWrongDimensionsNumberError(ModuleError):
    def __init__(self):
        super().__init__(**_valid_kwargs(locals()))


class UnableToDeserializeModelError(ModuleError):
    def __init__(self):
        super().__init__(**_valid_kwargs(locals()))


class InvalidTrainingDatasetError(ModuleError):
    def __init__(self, data_name=None, learner_type=None, reason=None, action_name=None, troubleshoot_hint=None):
        super().__init__(**_valid_kwargs(locals()))


class UnableToEvaluateCustomModelError(ModuleError):
    def __init__(self):
        super().__init__(**_valid_kwargs(locals()))


class FailedToEvaluateScriptError(ModuleError):
    def __init__(self, script_language, message):
        super().__init__(**_valid_kwargs(locals()))


class FailedToCreateHiveTableError(ModuleError):
    def __init__(self, table_name: str = None, cluster_name: str = None):
        super().__init__(**_valid_kwargs(locals()))


class InvalidZipFileError(ModuleError):
    def __init__(self):
        super().__init__(**_valid_kwargs(locals()))


class UnsupportedParameterTypeError(ModuleError):
    def __init__(self, parameter_name=None, reason=None):
        super().__init__(**_valid_kwargs(locals()))


class UnsupportedOutputTypeError(ModuleError):
    def __init__(self, output_type: str = None):
        super().__init__(**_valid_kwargs(locals()))


class SchemaDoesNotMatchError(ModuleError):
    def __init__(self):
        super().__init__(**_valid_kwargs(locals()))


class ImageExceedsLimitError(ModuleError):
    def __init__(self, file_path: str = None, size_limit=None):
        super().__init__(**_valid_kwargs(locals()))


class NumberOfUnconditionalProbabilitiesExceedsLimitError(ModuleError):
    def __init__(self, column_name_or_index_1=None, column_name_or_index_2=None):
        super().__init__(**_valid_kwargs(locals()))


class ExceedsColumnLimitError(ModuleError):
    def __init__(self, dataset_name: str = None, limit_columns_count: int = None, component_name: str = None):
        super().__init__(**_valid_kwargs(locals()))


class LabelColumnDoesNotHaveLabeledPointsError(ModuleError):
    def __init__(self, required_rows_count: int = None, dataset_name: str = None):
        super().__init__(**_valid_kwargs(locals()))


class ModuleOutOfMemoryError(ModuleError):
    def __init__(self, details: str = None):
        super().__init__(**_valid_kwargs(locals()))


class NotEnoughNormalizedColumnsError(ModuleError):
    def __init__(self, actual_num=None, lower_boundary=None):
        super().__init__(**_valid_kwargs(locals()))


class JoinOnIncompatibleColumnTypesError(ModuleError):
    def __init__(self, keys_left: str = None, keys_right: str = None):
        super().__init__(**_valid_kwargs(locals()))


class ColumnNamesNotStringError(ModuleError):
    def __init__(self, column_names: list = None):
        super().__init__(**_valid_kwargs(locals()))


class FailedToReadAzureSQLDatabaseError(ModuleError):
    def __init__(self, database_server_name: str = None, database_name: str = None,
                 sql_statement: str = None, detailed_message: str = None):
        super().__init__(**_valid_kwargs(locals()))


class IncorrectAzureMLDatastoreError(ModuleError):
    def __init__(self, datastore_name: str = None, workspace_name: str = None):
        super().__init__(**_valid_kwargs(locals()))


class InvalidTransformationDirectoryError(ModuleError):
    def __init__(self, arg_name: str = None, reason: str = None, troubleshoot_hint: str = None):
        super().__init__(**_valid_kwargs(locals()))


class InvalidModelDirectoryError(ModuleError):
    def __init__(self, arg_name: str = None, reason: str = None, troubleshoot_hint: str = None):
        super().__init__(**_valid_kwargs(locals()))


class FailedToWriteOutputsError(ModuleError):
    def __init__(self, reason: str = None, troubleshoot_hint: str = None):
        super().__init__(**_valid_kwargs(locals()))


class FailedJoinOperationError(ModuleError):
    def __init__(self, reason: str = None, troubleshoot_hint: str = None):
        super().__init__(**_valid_kwargs(locals()))


class FailedToDownloadFilesError(ModuleError):
    def __init__(self, file_names: str = None):
        super().__init__(**_valid_kwargs(locals()))


class ComponentDeprecatedError(ModuleError):
    def __init__(self, component_name: str = None, reason: str = None):
        super().__init__(**_valid_kwargs(locals()))


class LibraryExceptionError(ModuleError):
    def __init__(self, exception, customer_support_guidance=None):
        super().__init__(**_valid_kwargs(locals()))


class ErrorMapping:

    @classmethod
    def throw(cls, err: ModuleError):
        raise err

    @classmethod
    def rethrow(cls, e: BaseException, err: ModuleError):
        if isinstance(e, ModuleError):
            cls.throw(e)

        raise err from e

    @classmethod
    def verify_not_null_or_empty(cls, x: Union[str, any], name: str = None):
        def _throw():
            cls.throw(NullOrEmptyError(name))

        if isinstance(x, str):
            if is_null_or_empty(x):
                _throw()
        else:
            if x is None:
                _throw()

    @classmethod
    def verify_value_in_range(cls, value, lower_bound, upper_bound, arg_name: str = None, lower_inclusive=True,
                              upper_inclusive=True):
        if lower_inclusive:
            throw_exception = value < lower_bound
        else:
            throw_exception = value <= lower_bound

        if not throw_exception:
            if upper_inclusive:
                throw_exception = value > upper_bound
            else:
                throw_exception = value >= upper_bound

        if throw_exception:
            cls.throw(NotInRangeValueError(arg_name, lower_bound, upper_bound))

    @classmethod
    def verify_less_than(cls, value, b, arg_name: str = None):
        if value >= b:
            cls.throw(LessThanError(arg_name, b))

    @classmethod
    def verify_less_than_or_equal_to(cls, value, b, arg_name: str = None, b_name: str = None):
        if value > b:
            if b_name is not None:
                cls.throw(LessThanOrEqualToError(
                    arg_name=arg_name, actual_value=value, upper_boundary_meaning=b_name, upper_boundary=b))
            else:
                cls.throw(LessThanOrEqualToError(arg_name=arg_name, actual_value=value, upper_boundary=b))

    @classmethod
    def verify_greater_than(cls, value, b, arg_name: str = None):
        if value <= b:
            cls.throw(GreaterThanError(arg_name=arg_name, lower_boundary=b, actual_value=value))

    @classmethod
    def verify_greater_than_or_equal_to(cls, value, b, arg_name: str = None):
        if value < b:
            cls.throw(GreaterThanOrEqualToError(arg_name, b))

    @classmethod
    def verity_sizes_are_consistent(cls, size1: int, size2: int,
                                    friendly_name1: str = None, friendly_name2: str = None):
        if size1 != size2:
            cls.throw(InconsistentSizeError(friendly_name1, friendly_name2))

    @classmethod
    def verify_number_of_rows_greater_than_or_equal_to(cls, curr_row_count: int, required_row_count: int,
                                                       arg_name: str = None):
        if curr_row_count < required_row_count:
            cls.throw(TooFewRowsInDatasetError(arg_name, required_row_count, curr_row_count))

    @classmethod
    def verify_number_of_columns_greater_than_or_equal_to(cls, curr_column_count: int, required_column_count: int,
                                                          arg_name: str = None):
        if curr_column_count < required_column_count:
            cls.throw(TooFewColumnsInDatasetError(arg_name, required_column_count))

    @classmethod
    def verify_number_of_columns_equal_to(cls, curr_column_count: int, required_column_count: int,
                                          arg_name: str = None):
        if curr_column_count != required_column_count:
            cls.throw(UnexpectedNumberOfColumnsError(arg_name, required_column_count, curr_column_count))

    @classmethod
    def verify_number_of_columns_less_than_or_equal_to(cls, curr_column_count: int, required_column_count: int,
                                                       arg_name: str = None):
        if curr_column_count > required_column_count:
            cls.throw(UnexpectedNumberOfColumnsError(dataset_name=arg_name))

    @classmethod
    def verify_amount_of_feature_columns(cls, curr_columns_count: int, required_columns_count: int,
                                         arg_name: str = None):
        if curr_columns_count < required_columns_count:
            cls.throw(TooFewFeatureColumnsInDatasetError(required_columns_count, arg_name))

    @classmethod
    def verify_if_all_columns_selected(cls, act_col_count: int, exp_col_count: int,
                                       selection_pattern_friendly_name: str = None, long_description: bool = False):
        if act_col_count != exp_col_count:
            if long_description:
                cls.throw(BadNumberOfSelectedColumnsError(
                    selection_pattern_friendly_name, exp_col_count, act_col_count))
            else:
                cls.throw(BadNumberOfSelectedColumnsError(selection_pattern_friendly_name, exp_col_count))

    @classmethod
    def verify_are_columns_selected(cls, curr_selected_num: int, required_selected_num: int, arg_name: str = None):
        if curr_selected_num < required_selected_num:
            cls.throw(NoColumnsSelectedError(arg_name))

    @classmethod
    def verify_column_names_are_string(cls, column_names: list):
        not_string_col_names = [col_name for col_name in column_names if not isinstance(col_name, str)]
        if not_string_col_names:
            cls.throw(ColumnNamesNotStringError(column_names=not_string_col_names))

    @classmethod
    def verify_element_type(cls, type_: str, expected_type: str, column_name: str = None, arg_name: str = None):
        """ Verify the DataTable element type of {column_name} column is expected_type.

        :param type_: an element type of dataset column
        :param expected_type: expected element type
        :param column_name: opt, corresponding column name
        :param arg_name: opt, friendly name of the corresponding argument.
        :return:
        """
        if type_ != expected_type:
            cls.throw_invalid_column_type(type_, column_name, arg_name)

    @classmethod
    def verify_model_type(cls, model, expected_type, arg_name):
        if not isinstance(model, expected_type):
            cls.throw(InvalidLearnerError(arg_name=arg_name, learner_type=model.__class__.__name__))

    @classmethod
    def verify_model_indicated_type(cls, data_type, allowed_data_types, arg_name):
        if data_type not in allowed_data_types:
            model_type_name_to_score_module = {'Cluster': 'Assign Data to Clusters',
                                               'Recommender': "Score SVD Recommender"}
            type_name = data_type.value.short_name
            score_module = model_type_name_to_score_module.get(type_name, None)
            if score_module is not None:
                cls.throw(InvalidLearnerError(arg_name=arg_name, learner_type=type_name,
                                              troubleshoot_hint=f'For scoring scenario, please use '
                                              f'"{score_module}" module.'))
            cls.throw(InvalidLearnerError(arg_name=arg_name, learner_type=type_name))

    @classmethod
    def convert_to_module_exception(cls, eid, *parameters):
        return ModuleError(eid, *parameters)

    @classmethod
    def throw_invalid_column_type(
            cls, type_: str = None, column_name: str = None, arg_name: str = None):
        if not type_:
            cls.throw(InvalidColumnTypeError())
        elif (not column_name) and (not arg_name):
            cls.throw(InvalidColumnTypeError(type_))
        elif not arg_name:
            cls.throw(InvalidColumnTypeError(type_, column_name))
        else:
            cls.throw(InvalidColumnTypeError(type_, column_name, arg_name))

    @classmethod
    def get_exception_message(cls, ex: BaseException, show_exception_name: bool = False):
        if isinstance(ex, SystemExit) or show_exception_name:
            return f"{ex.__class__.__name__}: {cls._get_message_from_exception(ex)}"
        return cls._get_message_from_exception(ex)

    @staticmethod
    def _get_message_from_exception(ex: BaseException):
        try:
            if hasattr(ex, 'message') and ex.message:
                return ex.message
        except:  # noqa: E722
            pass

        try:
            if ex.__str__():
                return ex.__str__()
        except:  # noqa: E722
            pass

        try:
            if ex.__repr__():
                return ex.__repr__()
        except:  # noqa: E722
            pass

        try:
            return f'Error type: {ex.__class__.__name__}, Args: {ex.args}.'
        except:  # noqa: E722
            return f'Error type: {ex.__class__.__name__}.'


def _valid_kwargs(kwargs):
    # incoming 'kwargs' param value are expected to come from `locals()` in subclass `__init__` functions.
    # return value are expected to be passed to `super().__init__()` function.
    #
    # for incoming kwargs pre processing,
    #  1) 'self' should be excluded otherwise will cause duplicate 'self' params error
    #  2) items with `None` value should be excluded
    frame = inspect.currentframe().f_back
    if frame.f_code.co_name != '__init__':
        raise ValueError(f"_valid_kwargs is supposed to be called directly in Error class's __init__ function")

    valid_kwargs = {k: kwargs.get(k) for k in frame.f_code.co_varnames
                    if k != 'self' and kwargs.get(k) is not None}
    return valid_kwargs


def _raise_deprecated_error(name: str):
    raise ComponentDeprecatedError(
        component_name=name,
        reason=(
            "This component HAS BEEN DEPRECATED because its dependency, "
            "the NimbusML project (https://github.com/microsoft/NimbusML), "
            "is no longer actively maintained."
        )
    )
