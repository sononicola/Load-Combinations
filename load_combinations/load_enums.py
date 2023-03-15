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
    CAT_A = "Cat. A"
    CAT_B = "Cat. B"
    CAT_C = "Cat. C"
    CAT_D = "Cat. D"
    CAT_E = "Cat. E"
    CAT_F = "Cat. F"
    CAT_G = "Cat. G"
    CAT_H = "Cat. H"
    CAT_I = "Cat. I"
    CAT_K = "Cat. K"
    WIND = "Wind"
    SNOW_LOWER100 = "Snow < 1000m"
    SNOW_UPPER100 = "Snow > 1000m"
    TEMPERATURE = "Temperature"


