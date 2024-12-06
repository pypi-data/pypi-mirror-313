import enum


class MatchType(str, enum.Enum):
    STRICT = "strict"
    FUZZY = "fuzzy"
