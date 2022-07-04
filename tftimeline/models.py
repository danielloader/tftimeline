from enum import Enum

class OutputTypes(str, Enum):
    html = "html"
    png = "png"
    svg = "svg"
    json = "json"