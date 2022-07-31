from enum import Enum

class LoadType(Enum):
    UNFAVOURABLE = "unfavourable"
    FAVOURABLE = "favourable"

class DesignTypeULS(Enum):
    EQU = "EQU"
    STR = "STR"
    GEO = "GEO"

class PermanentActions(Enum):
    G1 = "G1"
    G2 = "G2"

class VariableActions(Enum):
    CAT_A = "A"
    CAT_B = "B"
    CAT_C = "C"
    CAT_D = "D"
    CAT_E = "E"
    CAT_F = "F"
    CAT_G = "G"
    CAT_H = "H"
    CAT_I = "I"
    CAT_K = "K"
    WIND = "wind"
    SNOW_LOWER100 = "snow < 1000m"
    SNOW_UPPER100 = "snow > 1000m"
    TEMPERATURE = "temperature"


