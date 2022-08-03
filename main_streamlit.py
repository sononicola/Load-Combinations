import streamlit as st
from LoadCombinations.load_enums import LoadType, DesignTypeULS, PermanentActions, VariableActions
from LoadCombinations.combination import Load, Combination

# -- DATA --
possibleActions = [load.value for load in PermanentActions]
possibleActions.extend([load.value for load in VariableActions])


# -- GENERAL PAGE SETUP --
st.set_page_config(
     page_title = "Load Combinations",
     page_icon = "👷‍♂️",
     initial_sidebar_state = "expanded",
     layout="centered"
)
# -- SIDEBAR --


# -- PAGE CONTENT --
st.header("Load Combinations")
st.subheader("according to NTC18 and EuroCode 0")

c1, c2 = st.columns([2,1])
with c1:
    nLoads = int(st.number_input(
            label = "n carichi", 
            min_value=1, 
            value=4)
    )
with c2:
    design_type = st.selectbox(
        label="TIpo di analisi", 
        options=[d_type.value for d_type in DesignTypeULS],
        index=1
        )

c1, c2, c3 = st.columns([1,0.8,1.2])
with c1:
    loadValues = [
        st.number_input(
            label = f"Valore {i}",
            min_value = 1.,
            step = 1.,
            format = "%.3f",
            key = f"LoadValue {i}"
            )
        for i in range(1,nLoads+1)
        ]
with c2:
    action = [
        st.selectbox(
            label = f"Tipologia {i}", 
            options = possibleActions, 
            key = f"LoadType {i}",
            index=i-1            
            ) 
        for i in range(1,nLoads+1)
        ]
with c3:
    loadTypes = [
        st.selectbox(
            label = f"Sfav or Fav {i}", 
            options = [loadtype.value for loadtype in LoadType], 
            key = f"Load_sfav_or_fav {i}"            
            ) 
        for i in range(1,nLoads+1)
        ]


# Since there are two enums class we need to find in which the load is
action_real = []
for i in range(nLoads):
    try:
        PermanentActions(action[i])
        action_real.append(PermanentActions(action[i]))
    except:
        action_real.append(VariableActions(action[i]))



loads = [Load(action_real[i], LoadType(loadTypes[i]), loadValues[i]) for i in range(nLoads) ]

comb = Combination(loads=loads, design_type=DesignTypeULS(design_type))

st.latex(r"\footnotesize"+comb.run("latex", is_streamlit=True))

t1,t2,t3 = st.tabs(["Plain Text", "LaTeX", "LaTeX+SIunitx"])
with t1:
        st.code(comb.run("plain"))

with t2:
    st.code(comb.run("latex"),language="latex")