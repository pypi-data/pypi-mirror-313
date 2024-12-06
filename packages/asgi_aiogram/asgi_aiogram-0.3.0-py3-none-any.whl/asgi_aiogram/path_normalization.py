from asgi_aiogram.exceptions import PlaceholderMissingException

TOKEN_PLACEHOLDER = "{bot_token}"
TOKEN_PLACEHOLDER_LIGHT = 11


def split_path_by_token_placeholder(path: str) -> tuple[str, slice, str]:
    if TOKEN_PLACEHOLDER not in path:
        raise PlaceholderMissingException(TOKEN_PLACEHOLDER)
    token_start_index = path.index(TOKEN_PLACEHOLDER)
    token_end_index = token_start_index + TOKEN_PLACEHOLDER_LIGHT

    path_prefix = path[:token_start_index]
    path_suffix = path[token_end_index:]

    slice_end = token_end_index - len(path) or None

    return path_prefix, slice(token_start_index, slice_end), path_suffix
