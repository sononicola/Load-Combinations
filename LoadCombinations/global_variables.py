CODE_NAME = "NTC18"

NAME_ULS = "SLU "
NAME_SLS = "SLE "
NAME_SLS_CHAR = "rara"
NAME_SLS_FREQ = "freq."
NAME_SLS_QP =  "q. perm."

Q_NAME_PLAIN = "Q "
GAMMA_UNFAV_PLAIN = "γ_s"
GAMMA_FAV_PLAIN= "γ_f"
PSI_PLAIN = "ψ_"

Q_NAME_LATEX = r"Q_{"
GAMMA_UNFAV_LATEX = r"\gamma_{s}"
GAMMA_FAV_LATEX= r"\gamma_{f}"



PRODUCT_LATEX = r"\cdot"
PSI_LATEX = r"\psi_"

SUBSCRIPT_GAMMA_UNFAV = "S"
SUBSCRIPT_GAMMA_FAV = "F"

NOTHING_PLAIN = "∅"
NOTHING_LATEX = r"\varnothing"


DICT_GENIERIC_MATERIAL = {
    "ULS": {
        "gamma": True,
        "psi" : (None,0)
        },
    "SLS_CHAR": {
        "gamma": False,
        "psi" : (None,0)
        },
    "SLS_FREQ" : {
        "gamma": False,
        "psi" : (1,2)
        },
    "SLS_QP": {
        "gamma": False,
        "psi" : (2,2)
        }

}
