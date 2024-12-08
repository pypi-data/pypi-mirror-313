import tiktoken


def tokenize(text: str, model: str = "gpt-3.5-turbo") -> list[int]:
    tokenizer = tiktoken.encoding_for_model(model)
    return tokenizer.encode(text)


def detokenize(tokens: list[int], model: str = "gpt-3.5-turbo") -> str:
    tokenizer = tiktoken.encoding_for_model(model)
    return tokenizer.decode(tokens)


def count_tokens(text: str) -> int:
    return len(tokenize(text))
