def get_hf_token_or_none(secrets):
    try:
        return secrets.get("hf_access_token", None)
    except:  # noqa
        return None
