import tiktoken


def count_tokens(text, model: str = "gpt-4o"):
    return len(tiktoken.encoding_for_model(model).encode(str(text)))
