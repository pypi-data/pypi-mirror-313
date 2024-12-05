import os
from typing import Optional

from tp_interfaces.helpers.convert import string_to_bool

DEFAULT_AMP_OPTIMIZE = False
DEFAULT_CPU_BATCH_SIZE = 1
DEFAULT_GPU_BATCH_SIZE = 1
DEFAULT_GPU_OOM_TIMEOUT = 30.0
DEFAULT_GPU_UTILIZATION_LIMIT = 1.0
DEFAULT_GPU_OOM_REPEAT_LIMIT = 3
DEFAULT_MAX_LENGTH = 40000


def get_bert_example_length() -> Optional[int]:
    bert_example_length_str = os.environ.get('BERT_EXAMPLE_LENGTH')
    return int(bert_example_length_str) if bert_example_length_str is not None else None


def get_bert_max_word_subtokens() -> Optional[int]:
    bert_max_word_subtokens = os.environ.get('BERT_MAX_WORD_SUBTOKENS')
    return int(bert_max_word_subtokens) if bert_max_word_subtokens is not None else None


def get_amp_optimize() -> bool:
    amp_optimize = os.environ.get('AMP_OPTIMIZE')
    return string_to_bool(amp_optimize) if amp_optimize is not None else DEFAULT_AMP_OPTIMIZE


def get_cpu_batch_size() -> int:
    cpu_batch_size_str = os.environ.get('CPU_BATCH_SIZE')
    return int(cpu_batch_size_str) if cpu_batch_size_str is not None else DEFAULT_CPU_BATCH_SIZE


def get_gpu_batch_size() -> int:
    gpu_batch_size_str = os.environ.get('GPU_BATCH_SIZE')
    return int(gpu_batch_size_str) if gpu_batch_size_str is not None else DEFAULT_GPU_BATCH_SIZE


def get_gpu_oom_timeout() -> float:
    gpu_oom_timeout = os.environ.get('GPU_OOM_TIMEOUT')
    return float(gpu_oom_timeout) if gpu_oom_timeout is not None else DEFAULT_GPU_OOM_TIMEOUT


def get_gpu_utilization_limit() -> float:
    gpu_utilization_limit = os.environ.get('GPU_UTILIZATION_LIMIT')
    return float(gpu_utilization_limit) if gpu_utilization_limit is not None else DEFAULT_GPU_UTILIZATION_LIMIT


def get_gpu_oom_repeat_limit() -> int:
    gpu_oom_repeat_limit = os.environ.get('GPU_OOM_REPEAT_LIMIT')
    return int(gpu_oom_repeat_limit) if gpu_oom_repeat_limit is not None else DEFAULT_GPU_OOM_REPEAT_LIMIT


def get_max_length() -> int:
    max_length = os.getenv('MAX_LENGTH')
    return int(max_length) if max_length else DEFAULT_MAX_LENGTH
