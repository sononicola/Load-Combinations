from math import gamma
from LoadCombinations.load_enums import LoadType, DesignTypeULS, PermanentActions, VariableActions
from LoadCombinations.combination import Load, Combination

#TODO i kmod legno vanno definiti a mano nel json perché dipendono da troppe variabili
#TODO error se I o K
#TODO check se ci sono 0 g1 o 0 g2. check se ce ne sono piu di due di qualsiasi tipo
def main():
    g1 = Load(action_type=PermanentActions.G1, load_type=LoadType.UNFAVOURABLE, value=100)
    g2 = Load(action_type=PermanentActions.G2, load_type=LoadType.UNFAVOURABLE, value=50)
    q_a = Load(action_type=VariableActions.CAT_A, load_type=LoadType.UNFAVOURABLE, value=10)
    q_b = Load(action_type=VariableActions.CAT_B, load_type=LoadType.UNFAVOURABLE, value=8)
    q_c = Load(action_type=VariableActions.CAT_C, load_type=LoadType.UNFAVOURABLE, value=7)

    print(q_c.psi)

    #print(q_a.action_type in PermanentActions)

    comb = Combination([g1, g2, q_a, q_b, q_c], design_type=DesignTypeULS.STR)
    temp = comb.combinations()
    print(temp)
    for ob in temp:
        for ob2 in ob:
            print(ob2.action_type.name)
        print()

    print(g1.gamma)
    print(g2.gamma)
    print(q_a.gamma)

    print(comb.ULS(print_style="plain"))

if __name__ == "__main__":
    main()

