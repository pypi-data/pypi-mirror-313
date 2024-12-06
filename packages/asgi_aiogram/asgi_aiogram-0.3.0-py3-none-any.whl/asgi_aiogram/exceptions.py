PLACEHOLDER_MISSING_ERROR_MESSAGE: str = "Path does not contain token placeholder {token_placeholder}"

class PlaceholderMissingException(Exception):
    def __init__(self, token_placeholder: str):
        super().__init__(PLACEHOLDER_MISSING_ERROR_MESSAGE.format(
            token_placeholder=token_placeholder
        ))