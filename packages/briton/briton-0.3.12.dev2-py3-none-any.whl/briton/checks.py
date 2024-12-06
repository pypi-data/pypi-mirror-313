def trllm_config_check(config):
    if "trt_llm" not in config:
        raise ValueError("trt_llm config is required for this model")
