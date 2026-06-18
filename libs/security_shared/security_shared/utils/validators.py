import re


def is_valid_email(email: str) -> bool:
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def is_valid_ip(ip: str) -> bool:
    pattern = r'^(\d{1,3}\.){3}\d{1,3}$'
    if not re.match(pattern, ip):
        return False
    return all(0 <= int(part) <= 255 for part in ip.split('.'))


def is_valid_cidr(cidr: str) -> bool:
    parts = cidr.split('/')
    if len(parts) != 2:
        return False
    try:
        return is_valid_ip(parts[0]) and 0 <= int(parts[1]) <= 32
    except ValueError:
        return False


def sanitize_string(value: str, max_length: int = 255) -> str:
    cleaned = re.sub(r'[<>"\'&;]', '', value)
    return cleaned[:max_length].strip()


def is_valid_uuid(value: str) -> bool:
    pattern = r'^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$'
    return bool(re.match(pattern, value.lower()))
