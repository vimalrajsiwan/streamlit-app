import streamlit as st
from openai import OpenAI

st.set_page_config("AI Chat App", page_icon="🤖")
st.title("Chatbot")

if 'setup_complete' not in st.session_state:
    st.session_state.setup_complete = False

def complete_setup():
    st.session_state.setup_complete = True 

# show the form when setup_complete = false
if st.session_state.setup_complete == False:
    st.subheader("Personal Information", divider= "rainbow")

    if "name" not in st.session_state:
        st.session_state["name"] =""
    if "experience" not in st.session_state:
        st.session_state["experience"] =""
    if "skills" not in st.session_state:
        st.session_state["skills"] =""

    st.session_state["name"] = st.text_input(label="Name", value= st.session_state["name"], max_chars= None, placeholder="Enter Your Name")
    st.session_state["experience"] = st.text_area( label="Experience", value=st.session_state["experience"], height=None, max_chars=None, placeholder= "Describe your experience")
    st.session_state["skills"] = st.text_area( label="Skills", value=st.session_state["skills"], height=None, max_chars=None, placeholder= "List your skills")

    st.write(f"""**Your Name**: {st.session_state["name"]}""")
    st.write(f"""**Your Experience**: {st.session_state["experience"]}""")
    st.write(f"""**Your Skills**: {st.session_state["skills"]}""")

    st.subheader("Company and Position", divider= "rainbow")

    if "level" not in st.session_state:
        st.session_state["level"] ="Junior"
    if "position" not in st.session_state:
        st.session_state["position"] ="Data Scientist"
    if "company" not in st.session_state:
        st.session_state["company"] ="Amazon"


    col1, col2 = st.columns(2)

    with col1:
        st.session_state["level"] = st.radio(
            label="Choose level",
            key= "visibility",
            options= ["Junior", "Mid-level", "Senior"]
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

    st.write(f"""**Your information**: {st.session_state["level"]} {st.session_state["position"]} at {st.session_state["company"]}""")

    if st.button("Start Interview", on_click= complete_setup):
        st.write("Setup completed, Starting interview...")

# Interview stage
if st.session_state.setup_complete:

    # Display a welcome message and prompt the user to introduce themselves
    st.info(
        """
        Start by introducing yourself.
        """,
        icon = "👋"
    )

    client = OpenAI(api_key= st.secrets["OPENAI_API_KEY"])

    if 'openai_model' not in st.session_state:
        st.session_state.openai_model = "gpt-4o"

    if "messages" not in st.session_state:
        st.session_state.messages = [{
                "role": "system",
                "content": f"""You are an HR executive
                that interviews an interviewee called {st.session_state["name"]} 
                with expirience {st.session_state["experience"]} 
                and skills {st.session_state["skills"]}. 
                You should interview him for the 
                position {st.session_state["level"]} {st.session_state["position"]} 
                at the company {st.session_state["company"]}"""
            }
        ]


    for message in st.session_state.messages:
        if message["role"] != "system":
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    if prompt := st.chat_input("Enter Your Query"):
        st.session_state.messages.append({
            "role": "user",
            "content": prompt
        })
        with st.chat_message("user"):
            st.markdown(prompt)
        
        with st.chat_message("assistant"):
            stream = client.chat.completions.create(
                model= st.session_state.openai_model,
                messages= [
                    { "role": m["role"], "content": m["content"] } for m in st.session_state.messages
                ],
                max_tokens= 1000,
                stream= True
            )

            response = st.write_stream(stream)
        st.session_state.messages.append({"role": "assistant", "content": response})
