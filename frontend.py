import streamlit as st
import connection_file


class FrontEnd:

    def __init__(self):

        with open('my apikey.txt', 'r') as file:
            self.api_key = file.read()

    def main_page(self):
        st.title("🤖 Chat GPT API")
        st.write("---")

        new_question = st.text_input(label="Enter your question here")

        # context = connection_file.read_text_file("product_context.txt")
        context = ""

        if st.button("ASK  ▶"):
            answer = connection_file.ask_question(
                context,
                new_question,
                self.api_key)

            st.write("A: " + answer)


if "front_end_instance" not in st.session_state:
    front_end_instance = FrontEnd()
    st.session_state.front_end_instance = front_end_instance

st.session_state.front_end_instance.main_page()
