import streamlit as st
from langchain_ollama import ChatOllama


st.set_page_config(page_title="Streamlit Chat", page_icon="💬")

st.title("Chatbot")

if "setup_complete" not in st.session_state:
    st.session_state.setup_complete = False
if "user_message_count" not in st.session_state:
    st.seesion_state.user_message_count = 0
if "feedback_shown" not in st.session_state:
    st.session_state.feedback_shown = False
if "messages" not in st.seesion_state:
    st.session_state.messages = []
if "chat_complete" not in st.session_state:
    st.sesion_state.chat_complete = False


def complete_setup():
    st.session_state.setup_complete = True
    
def show_feedback():
    st.session_state.feedback_shown = True

if not st.session_state.setup_complete:

    st.subheader("Personal information", divider="rainbow")
    
    if "name" not in st.session_state:
        st.session_state["name"] = ""
    if "experience" not in st.session_state:
        st.session_state["experience"] = ""
    if "skills" not in st.session_state:
        st.session_state["skills"] = ""

    st.session_state["name"] = st.text_input(label="Name", value = st.session_state["name"], max_chars=40, placeholder="Enter you name")

    st.session_state["experience"] = st.text_area(
        label="Expirience", value=st.session_state["experience"], height=None,
        max_chars=200, placeholder="List your skills"
    )

    st.session_state["skills"] = st.text_area(
        label="Skills", value=st.session_state["skills"], height=None,
        max_chars=200,
        placeholder="List your skills"
        )

    st.write(f"**Your Name**: {st.session_state['name']}")
    st.write(f"**Your Experience**: {st.session_state['experience']}")
    st.write(f"**Your Skills**: {st.session_state['skills']}")

    st.subheader("Company and Position", divider="rainbow")
    
    if "level" not in st.session_state:
        st.session_state["level"] = "Junior"
    if "position" not in st.session_state:
        st.session_state["position"] = "Data Scientist"
    if "company" not in st.session_state:
        st.session_state["company"] = "Amazon"

    col1, col2 = st.columns(2)

    with col1:
        st.session_state["level"] = st.radio(
            "Choose level",
            key="visibility",
            options=["Junior", "Mid-level", "Senior"]
        )
        
    with col2:
        st.session_state["position"] = st.selectbox(
            "Choose a position",
            ("Data Scientist", "Data engineer", "ML Engineer", "BI Analyst", "Financial Analyst")
        )
        
    st.session_state["company"] = st.selectbox(
        "Choose a Company",
        ("Amazon", "Meta", "Udemy", "365 Company", "Nestle", "LinkedIn", "Spotify")
    )

    st.write(f"**Your information**: {st.session_state['level']}, {st.session_state['position']} at {st.session_state['company']}")
    
    if st.button("Start Interview", on_click=complete_setup):
        st.write("Setup complete. Starting interview...")
        
        
if st.session_state.setup_complete and not st.session.feedback_shown and not st.session.chat_complete:
    st.info(
        """
        Start by introducing yourself
        """,
        icon="👋"
    )

    client = ChatOllama(model="llama3.2", temperature=0.6, top_p=0.9)

    # if "ollama_model" not in st.session_state:
    #     st.session_state["ollama_model"] = "llama3.2"
        
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role":"system", "content": f"""
            You are an HR executive that interviews an interviewee called {st.session_state["name"]}
            with experience {st.session_state["experience"]} and {st.session_state["skills"]}. You should interview them 
            for position {st.session_state["level"]} {st.session_state["position"]} at the company {st.session_state["company"]}.
            """}
        ]
        
    for message in st.session_state.messages:
        if message["role"] != "system":
            with st.chat_message(message['role']):
                st.markdown(message["content"])
        
    if prompt := st.chat_input("Your answer.", max_chars=1000):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        with st.chat_message("assistant"):
            stream = client.stream([(m["role"], m["content"])
                                for m in st.session_state.messages])
            
            response = st.write_stream(stream)
        st.session_state.messages.append({"role": "assistant", "content": response})