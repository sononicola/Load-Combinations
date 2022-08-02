from typing import Literal
from .load_enums import LoadType, DesignTypeULS, PermanentActions, VariableActions
from dataclasses import dataclass
import json

from .global_variables import *

def siunitex(number:float, unit:str = False) -> str:
    if unit:
        return "\\SI{" + f"{number:.2f}" + "}{" + unit + "}"
    return "\\num{" + f"{number:.2f}" + "}"


@dataclass
class Load:
    action_type: PermanentActions | VariableActions
    load_type: LoadType
    value: float

    def __post_init__(self):
        with open("LoadCombinations/regulations.json") as file:
            data = json.load(file)[CODE_NAME][self.action_type.value]

        self.name = data["name"]

        if self.action_type in VariableActions:
            self.psi: list = data["psi"]

    ## Create strings for actual combination output:

    def prod_str2(self, gamma: bool, psi: Literal[0,1,2] | None = None, print_style: Literal["plain", "latex", "latex-siunitex"] = "plain") -> str:
        "" 
        if print_style == "plain":
            if self.action_type in VariableActions:
                if psi:
                    return f"{GAMMA_FAV_PLAIN if self.load_type is LoadType.FAVOURABLE else GAMMA_UNFAV_PLAIN} * {Q_NAME_PLAIN}{self.name} * {PSI_PLAIN}{psi}"
                else:
                    return f"{GAMMA_FAV_PLAIN if self.load_type is LoadType.FAVOURABLE else GAMMA_UNFAV_PLAIN} * {Q_NAME_PLAIN}{self.name}"
            else:
                return f"{GAMMA_FAV_PLAIN if self.load_type is LoadType.FAVOURABLE else GAMMA_UNFAV_PLAIN} * {self.name}"
        elif print_style == "latex" or "latex-siunitex":
            if self.action_type in VariableActions:
                return f"{GAMMA_FAV_LATEX if self.load_type is LoadType.FAVOURABLE else GAMMA_UNFAV_LATEX} {PRODUCT_LATEX} {Q_NAME_LATEX}{self.name}"+ r"}"+ f" {PRODUCT_LATEX} {PSI_LATEX}{psi}"
            else:
                return f"{GAMMA_FAV_LATEX if self.load_type is LoadType.FAVOURABLE else GAMMA_UNFAV_LATEX} {PRODUCT_LATEX} {self.name}"

    def prod_numb(self, gamma:bool, psi: Literal[0,1,2] | None = None, print_style: Literal["plain", "latex", "latex-siunitex"] = "plain") -> str:
        if print_style == "plain":
            if gamma and psi != None:
                return f"{self.gamma[0] if self.load_type is LoadType.FAVOURABLE else self.gamma[1]} * {self.value} * {self.psi[psi]}"
            elif gamma and psi == None:
                return f"{self.gamma[0] if self.load_type is LoadType.FAVOURABLE else self.gamma[1]} * {self.value}"
            elif gamma == False and psi != None:
                return f"{self.value} * {self.psi[psi]}"
            else:
                return f"{self.value}"
        elif print_style == "latex":
            if gamma and psi != None:
                return f"{self.gamma[0] if self.load_type is LoadType.FAVOURABLE else self.gamma[1]} {PRODUCT_LATEX} {self.value} {PRODUCT_LATEX} {self.psi[psi]}"
            elif gamma and psi == None:
                return f"{self.gamma[0] if self.load_type is LoadType.FAVOURABLE else self.gamma[1]} {PRODUCT_LATEX} {self.value}"
            elif gamma == False and psi != None:
                return f"{self.value} {PRODUCT_LATEX} {self.psi[psi]}"
            else:
                return f"{self.value}"
        elif print_style == "latex-siunitex":
            if gamma and psi != None:
                return f"{self.gamma[0] if self.load_type is LoadType.FAVOURABLE else self.gamma[1]} {PRODUCT_LATEX} " + siunitex(self.value) + f"{PRODUCT_LATEX} {self.psi[psi]}"
            elif gamma and psi == None:
                return f"{self.gamma[0] if self.load_type is LoadType.FAVOURABLE else self.gamma[1]} {PRODUCT_LATEX} " + siunitex(self.value)
            elif gamma == False and psi != None:
                return siunitex(self.value) + f"{PRODUCT_LATEX} {self.psi[psi]}"
            else:
                return siunitex(self.value)

    def prod_res(self, gamma:bool, psi: Literal[0,1,2] | None = None) -> float:
        gamma_real = self.gamma[0] if self.load_type is LoadType.FAVOURABLE else self.gamma[1] if gamma  else 1
        psi_real = 1 if psi == None else self.psi[psi]
        
        return gamma_real * self.value * psi_real

    def prod_str(self, gamma: bool, psi: Literal[0,1,2] | None = None, print_style: Literal["plain", "latex", "latex-siunitex"] = "plain") -> str:
        "" 
        if gamma: #  so is a ULS combination
            if print_style == "plain":
                if self.action_type in VariableActions:
                    if psi != None:
                        return f"γ_{self.name},{SUBSCRIPT_GAMMA_FAV if self.load_type is LoadType.FAVOURABLE else SUBSCRIPT_GAMMA_UNFAV} * {Q_NAME_PLAIN}{self.name} * {PSI_PLAIN}{psi}"
                    else:
                        return f"γ_{self.name},{SUBSCRIPT_GAMMA_FAV if self.load_type is LoadType.FAVOURABLE else SUBSCRIPT_GAMMA_UNFAV} * {Q_NAME_PLAIN}{self.name}"
                else:
                    return f"γ_{self.name},{SUBSCRIPT_GAMMA_FAV if self.load_type is LoadType.FAVOURABLE else SUBSCRIPT_GAMMA_UNFAV} * {self.name}"
            elif print_style == "latex" or "latex-siunitex":
                if self.action_type in VariableActions:
                    if psi != None:
                        return r"\gamma_{" + f"{self.name},{SUBSCRIPT_GAMMA_FAV if self.load_type is LoadType.FAVOURABLE else SUBSCRIPT_GAMMA_UNFAV}" + r"}" + f" {PRODUCT_LATEX} {Q_NAME_LATEX}{self.name}"+ r"}"+ f" {PRODUCT_LATEX} {PSI_LATEX}{psi}"
                    else:
                        return r"\gamma_{" + f"{self.name},{SUBSCRIPT_GAMMA_FAV if self.load_type is LoadType.FAVOURABLE else SUBSCRIPT_GAMMA_UNFAV}" + r"}" + f" {PRODUCT_LATEX} {Q_NAME_LATEX}{self.name}"+ r"}"
                else:
                    return r"\gamma_{" + f"{self.name},{SUBSCRIPT_GAMMA_FAV if self.load_type is LoadType.FAVOURABLE else SUBSCRIPT_GAMMA_UNFAV}" + r"}" + f" {PRODUCT_LATEX} {self.name}"
        else: # so is a SLS combination
            if print_style == "plain":
                if self.action_type in VariableActions:
                    return f"{Q_NAME_PLAIN}{self.name} * {PSI_PLAIN}{psi}"
                else:
                    return f"{self.name}"
            elif print_style == "latex" or "latex-siunitex":
                if self.action_type in VariableActions:
                    return f" {PRODUCT_LATEX} {Q_NAME_LATEX}{self.name}"+ r"}"+ f" {PRODUCT_LATEX} {PSI_LATEX}{psi}"
                else:
                    return f"{self.name}"
        

    

class Combination:
    def __init__(self, loads: list[Load], design_type: DesignTypeULS = DesignTypeULS.STR):
        self.loads = loads
        self.design_type = design_type

        self.add_gamma_to_loads() 

    def add_gamma_to_loads(self):
        "Add gamma coeficients to Load objects. Have to be done here because they depend on design type"
        with open("LoadCombinations/regulations.json") as file:
            data = json.load(file)[CODE_NAME]

        for load in self.loads:
            if load.action_type in PermanentActions:
                load.gamma: list = data[f"gamma_{self.design_type.value}"][load.action_type.value] # G1 and G2
            else:
                load.gamma: list = data[f"gamma_{self.design_type.value}"]["variable"]

    def only_permanent_loads(self) -> list[Load]:
        """
        Return only permanent loads in self.loads

        Example: Given [g1, g2, q_catH, q_snow, q_wind] Load objects returns:
        [g1, g2]
        """
        return [load for load in self.loads if load.action_type in PermanentActions]

    def only_variable_loads(self) -> list[Load]:
        """
        Return only variable loads in self.loads

        Example: Given [g1, g2, q_catH, q_snow, q_wind] Load objects returns:
        [q_catH, q_snow, q_wind]
        """
        return [load for load in self.loads if load.action_type in VariableActions]
        
    def iteration_variable_loads(self) -> list[list[Load]]:
        """
        Given a list of variable loads, return all possibile iterations

        Example: Given [g1, g2, q_catH, q_snow, q_wind] Load objects returns:
        [[q_catH, q_snow, q_wind], [q_snow, q_catH, q_wind], [q_wind, q_catH, q_snow]]
        where the first one is the principal load
        """
        variable_loads = self.only_variable_loads()

        list_iterations = []
        for load in range(len(variable_loads)):
            not_principal_loads = variable_loads.copy()
            not_principal_loads.pop(load)

            principal_load = [variable_loads[load]]
            principal_load.extend(not_principal_loads)

            list_iterations.append(principal_load)
            
            
        return list_iterations

    def combinations(self) -> list[list[Load]]:
        """
        Return a list of list with all combinations

        Example: Given [g1, g2, q_catH, q_snow, q_wind] Load objects returns:
        [[g1, g2, q_catH, q_snow, q_wind], [g1, g2, q_snow, q_catH, q_wind], [g1, g2, q_wind, q_catH, q_snow]]
        """
        permanent_loads = self.only_permanent_loads()
        list_iterations = self.iteration_variable_loads()

        # there isn't any variable load
        if len(list_iterations) == 0: 
            return [permanent_loads]

        combinations:list[list[Load]]  = []
        for iteration in range(len(list_iterations)):
            comb = permanent_loads.copy()
            comb.extend(list_iterations[iteration])
            combinations.append(comb)

        return combinations

    

    def generic_comb(self, name:str, name2:str, gamma:bool, psi: list[int | None], print_style: Literal["plain", "latex", "latex-siunitex"] = "latex", measure_unit_plain:str = "kN", measure_unit_siunitex:str = r"\kilo\newton")-> str:
        combinations = self.combinations()
        # combinations are composed always with g1 g2 principal load, and not principal loads
        # gamma[0] == favourable, gamma[1] == unfavourable

        JUST = 28
        text  = ""
    
        for comb in combinations:
            text += f"{name}_{name2}_{comb[2].name}".ljust(JUST-1) + "= "
            # G1 and G2
            for load in comb[0:1]: 
                text += load.prod_str(gamma=gamma, print_style=print_style)
                text += " + "
            for load in comb[1:2]: 
                text += load.prod_str(gamma=gamma, print_style=print_style)
            # principal load
            if comb[2:]: # if there isn't any variable loads
                for load in comb[2:3]: 
                    text += " + " 
                    text += load.prod_str(gamma=gamma, psi=psi[0], print_style=print_style)
            # Not principal loads
            if comb[3:]: # if exixt
                for load in comb[3:]: 
                    text += " + " 
                    text += load.prod_str(gamma=gamma, psi=psi[1], print_style=print_style)

            # G1 and G2
            text += "\n " .ljust(JUST) + "= "
            for load in comb[0:1]: 
                text += load.prod_numb(gamma=gamma, print_style=print_style)
                text += " + "
            for load in comb[1:2]: 
                text += load.prod_numb(gamma=gamma, print_style=print_style)
            # principal load
            if comb[2:]: # if there isn't any variable loads
                for load in comb[2:3]: 
                    text += " + " 
                    text += load.prod_numb(gamma=gamma, psi=psi[0], print_style=print_style)
            # Not principal loads
            if comb[3:]: # if exixt
                for load in comb[3:]: 
                    text += " + " 
                    text += load.prod_numb(gamma=gamma, psi=psi[1], print_style=print_style)

            text += "\n " .ljust(JUST) + "= "
            res = []
            # G1 and G2
            for load in comb[0:1]: 
                text += f"{load.prod_res(gamma=gamma):.2f}"
                res.append(load.prod_res(gamma=gamma))
                text += " + "
            for load in comb[1:2]: 
                text += f"{load.prod_res(gamma=gamma):.2f}"
                res.append(load.prod_res(gamma=gamma))
            # principal load
            if comb[2:]: # if there isn't any variable loads
                for load in comb[2:3]: 
                    text += " + " 
                    text += f"{load.prod_res(gamma=gamma, psi=psi[0]):.2f}"
                    res.append(load.prod_res(gamma=gamma, psi=psi[0]))
            # Not principal loads
            if comb[3:]: # if existt
                for load in comb[3:]: 
                    text += " + " 
                    text += f"{load.prod_res(gamma=gamma, psi=psi[1]):.2f}"
                    res.append(load.prod_res(gamma=gamma, psi=psi[1]))

            text += "\n ".ljust(JUST) + f"= {sum(res):.2f}"
            text += "\n\n"


        return text

    def ULS(self, print_style: Literal["plain", "latex", "latex-siunitex"] = "plain"):
        return self.generic_comb(name = NAME_ULS, name2="", gamma=True, psi= [None, 0], print_style=print_style)

    def SLS_CHAR(self, print_style: Literal["plain", "latex", "latex-siunitex"] = "plain"):
        return self.generic_comb(name = NAME_SLS, name2=NAME_SLS_CHAR, gamma=False, psi= [None, 0], print_style=print_style)

    def SLS_FREQ(self, print_style: Literal["plain", "latex", "latex-siunitex"] = "plain"):
        return self.generic_comb(name = NAME_SLS, name2=NAME_SLS_FREQ, gamma=False, psi= [1, 2], print_style=print_style)

    def SLS_QP(self, print_style: Literal["plain", "latex", "latex-siunitex"] = "plain"):
        return self.generic_comb(name = NAME_SLS, name2=NAME_SLS_QP, gamma=False, psi= [2, 2], print_style=print_style)

