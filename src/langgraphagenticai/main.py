import streamlit as st
from src.langgraphagenticai.ui.streamlitui.loadui import LoadStreamlitUI
from src.langgraphagenticai.LLMS.groqllm import GroqLLM
from src.langgraphagenticai.graph.graph_builder import GraphBuilder
from src.langgraphagenticai.ui.streamlitui.display_result import DisplayResultStreamlit

def load_langraph_agenticai_app():
    """
    Loads and runs the LangGraph AgeenticAI Application with Streamlit U.
    This function initializes the Ui,handles user imput,configures the LLM modell,
    set up the graph based on the selected use case and displays the output while 
    implementing exception handling for robustness

    
    """

    #Loading the UI
    ui  = LoadStreamlitUI()
    user_input = ui.load_streamlit_ui()

    if not user_input:
        st.error("Error : Failed to load user input from the UI")
        return 
    
    # Text input for user message
    if st.session_state.IsFetchButtonClicked:
        user_message = st.session_state.timeframe 
    else :
        user_message = st.chat_input("Enter your message:")

    if user_message:
        try:
            ##Configuring the llms
            obj_llm_config = GroqLLM(user_controls_input=user_input)
            model = obj_llm_config.get_llm_model()

            if not model:
                st.error("Error: LLM Model could not be initialized")
                return
            
            #Initialize and set up the graph based on the use case
            usecase = user_input.get("selected_usecase")

            if not usecase:
                st.error("Error : No use case selected.")

            ##GRaph builder
            graph_builder = GraphBuilder(model) 
            try:
                graph = graph_builder.setup_graph(usecase)
                print(user_message)
                DisplayResultStreamlit(usecase,graph,user_message).display_result_on_ui()

            except Exception as e:
                st.error(f"Error : Graph Setup failed  - {e}")
                return

        except Exception as e:
            st.error(f"Error : Graph Setup failed  - {e}")
            return


