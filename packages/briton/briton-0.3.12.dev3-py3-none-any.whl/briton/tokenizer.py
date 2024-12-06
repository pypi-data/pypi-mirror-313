from typing import List

from tokenizers import AddedToken


def serialize_added_tokens_to_config(added_tokens: List[AddedToken]) -> List[str]:
    """Serialize to pbtxt format."""
    lines = ["added_tokens {"]
    for added_token in added_tokens:
        token_lines = serialize_added_token_to_config(added_token)
        lines.extend([f"  {line}" for line in token_lines])
    lines.append("}")
    return lines


def serialize_added_token_to_config(added_token: AddedToken) -> List[str]:
    """Serialize to pbtxt format."""
    fields = [
        f'content: "{added_token.content}"',
        f"single_word: {added_token.single_word}",
        f"lstrip: {added_token.lstrip}",
        f"rstrip: {added_token.rstrip}",
        f"normalized: {added_token.normalized}",
        f"special: {added_token.special}",
    ]
    return [
        "tokens {",
        *[f"  {field}" for field in fields],
        "}",
    ]
