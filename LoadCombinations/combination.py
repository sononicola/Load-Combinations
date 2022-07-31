from typing import Literal
from .load_enums import LoadType, DesignTypeULS, PermanentActions, VariableActions
from dataclasses import dataclass
import json

from .global_variables import CODE_NAME

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

        combinations = []
        for iteration in range(len(list_iterations)):
            comb = permanent_loads.copy()
            comb.extend(list_iterations[iteration])
            combinations.append(comb)

        return combinations

