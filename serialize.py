def parse_message(raw: str | None) -> tuple[str, str] | None:
    if not raw:
        return None
    key, sep, value = raw.partition(": ")
    key = key.strip()
    if not sep or not key or not value:
        return None
    return key, value.strip()
