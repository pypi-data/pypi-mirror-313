import re

REGEX_NUMERIC = re.compile(r"^\d+$")

REGEX_NUMBERS_ONLY = re.compile(r"^[\d\.]+$")

REGEX_CAMEL_CASE = re.compile(
    r"((?<=[a-z0-9])(?=[A-Z])|(?<!^)(?<=[A-Z])(?=[A-Z][a-z]))"
)

RE_DOMAIN_NAMES = re.compile(
    r"^(?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+[a-z0-9][a-z0-9-]{0,61}[a-z0-9]$"
)

RE_UUID = re.compile(r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$")

# r"^[\w.-]+@[\w.-]+\.\w+$",
RE_EMAIL = re.compile(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")

RE_HTML = re.compile(r"<[^<]+?>")

RE_URL = re.compile(
    r"^https?:\/\/(?:(?:www\.)?(?:[a-zA-Z0-9-]+\.)+[a-zA-Z0-9]{2,}|(?:[a-zA-Z0-9-]+\.)*[a-zA-Z0-9-]+(?:\/[^\s/]+)+)(?:\/[^?\s]*)?(?:\?[^\s]*)?$"
)


# r"^(\+?\d{1,3})?\s?\d{3}[\s.-]\d{3}[\s.-]\d{4}$"
RE_PHONE_NUMBER = re.compile(r"^(\+?\d{1,3})?\s?\d{3}[\s.-]\d{3}[\s.-]\d{4}$")

# r"^\s*function\s+\w+\s*\("
RE_JAVASCRIPT = re.compile(r"^\s*function\s+\w+\s*\(")
