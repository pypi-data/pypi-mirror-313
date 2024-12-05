from enum import Enum


class ScriptEnvStatus(str, Enum):
    NONEXISTENT = 'nonexistent'
    CREATING = 'creating'
    CREATION_FAILED = 'creation_failed'
    CREATED = 'created'
    INSTALLING = 'installing'
    INSTALLATION_FAILED = 'installation_failed'
    INSTALLED = 'installed'


class ScriptExecutionStatus(str, Enum):
    PENDING = 'pending'
    PRECONDITION_NOT_MET = 'precondition_not_met'
    EXECUTING = 'executing'
    EXECUTION_FAILED = 'execution_failed'
    DONE = 'done'


class ScriptLang(str, Enum):
    R = 'r'
    PYTHON = 'python'


class ScriptType(str, Enum):
    DATA_QUALITY_TEST = 'data_quality_test'
    INTAKE = 'intake'
    MODEL_TRAINING = 'model_training'
    PREDICTION_LINE = 'prediction_line'
    PREDICTION_POINT = 'prediction_point'
    SCOPE_CALCULATION = 'scope_calculation'
    STEERING_SIMULATION = 'steering_simulation'
