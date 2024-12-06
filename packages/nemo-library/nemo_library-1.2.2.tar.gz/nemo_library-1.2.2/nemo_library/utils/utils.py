import re


def display_name(column: str,idx: int=None) -> str:
    if idx:
        return f"({idx:03}) {column}"
    else:
        return column

def internal_name(column: str,idx: int=None) -> str:
    if idx:
        return sanitized_name(f"{column}_({idx:03})")
    else:
        return sanitized_name(column)

def import_name(column: str,idx: int=None) -> str:
    if idx:
        return sanitized_name(display_name(column,idx))
    else:
        return sanitized_name(column)

def sanitized_name(displayName: str) -> str:
    return re.sub(r"[^a-z0-9_]", "_", displayName.lower()).strip()
