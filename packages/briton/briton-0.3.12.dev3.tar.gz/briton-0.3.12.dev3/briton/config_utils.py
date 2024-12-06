import logging
from typing import Optional
from briton.trtllm_config import TrussTRTLLMBatchSchedulerPolicy


def trtllm_config_check(config):
    if "trt_llm" not in config:
        raise ValueError("trt_llm config is required for this model")


def batch_scheduler_policy_to_int(policy: TrussTRTLLMBatchSchedulerPolicy, logger: logging.Logger) -> int:
    if policy == TrussTRTLLMBatchSchedulerPolicy.MAX_UTILIZATION:
        return 0
    elif policy == TrussTRTLLMBatchSchedulerPolicy.GUARANTEED_NO_EVICT:
        return 1
    else:
        logger.warning(f"Unknown batch scheduler policy: {policy}. Using GUARANTEED_NO_EVICT.")
        return 1
    