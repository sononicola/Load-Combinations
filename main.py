from load_combinations.load_enums import LoadType, DesignTypeULS, PermanentActions, VariableActions
from load_combinations.combination import Load, Combination

#TODO i kmod legno vanno definiti a mano nel json perché dipendono da troppe variabili
#TODO error se I o K
#TODO check se ci sono 0 g1 o 0 g2. check se ce ne sono piu di due di qualsiasi tipo
# TODO se tutti fav: togliere i variabli dalla lista combinazioni
def main():
    g1 = Load(action_type=PermanentActions.G1, load_type=LoadType.UNFAVOURABLE, value=23.75)
    g2 = Load(action_type=PermanentActions.G2, load_type=LoadType.UNFAVOURABLE, value=28.24)
    #q_a = Load(action_type=VariableActions.CAT_A, load_type=LoadType.UNFAVOURABLE, value=10)
    q_b = Load(action_type=VariableActions.CAT_B, load_type=LoadType.UNFAVOURABLE, value=22.50)
    #q_c = Load(action_type=VariableActions.CAT_C, load_type=LoadType.UNFAVOURABLE, value=7)
    q_snow = Load(action_type=VariableActions.SNOW_LOWER100, load_type=LoadType.UNFAVOURABLE, value=10.13)
    q_wind = Load(action_type=VariableActions.WIND, load_type=LoadType.UNFAVOURABLE, value=0.4328)


    #print(q_a.action_type in PermanentActions)

    comb = Combination([g1, g2, q_b, q_snow, q_wind], design_type=DesignTypeULS.STR)


    #print(g2.gamma)
    #print(q_a.gamma)

    print(comb.run("plain"))
    print(comb.run("latex-siunitex", "kN"))
    print(comb.calc_combinations_results("latex"))

if __name__ == "__main__":
    main()

