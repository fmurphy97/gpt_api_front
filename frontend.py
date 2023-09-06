import streamlit as st
import text_connection
import image_connections
import os

class FrontEnd:

    def __init__(self):

        self.api_key = None

        api_key_filepath = 'my apikey.txt'
        if os.path.exists(api_key_filepath):
            with open(api_key_filepath, 'r') as file:
                self.api_key = file.read()
        else:
            self.api_key = None

        self.images_to_gen_count = 1
        self.selected_resolution = "256x256"

        self.last_api_response = None
        self.generated_images = []

        self.current_page_function = self.main_page
        self.session_messages = []

    def text_gen_page(self):

        model_to_use = st.selectbox(
            "Select Model to Use",
            options=["gpt-4", "gpt-3.5-turbo", "text-davinci-003", "text-davinci-002",
                     "davinci", "curie", "babbage", "ada"])

        # React to user input
        if prompt := st.chat_input("Send a message"):
            # Add it to messages
            self.session_messages.append({"role": "user", "content": prompt})

            # Get a response and store it in messages
            response = text_connection.ask_question(context="", question=prompt, openai_api_key=self.api_key,
                                                    model=model_to_use)
            self.session_messages.append({"role": "ai", "content": response})

        # Display all messages
        for message in self.session_messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    def img_page(self):

        new_question = st.text_input(label="Enter your prompt here")
        self.images_to_gen_count = st.slider('Select number of images', 1, 10)

        # Define the available definitions
        available_resolutions = ["256x256", "512x512", "1024x1024"]
        # Create the dropdown
        self.selected_resolution = st.selectbox("Select resolution", available_resolutions)

        if st.button("CREATE ▶", key="button to create images"):
            self.last_api_response = image_connections.generate_images(
                prompt_message=new_question, num_images=self.images_to_gen_count, img_size=self.selected_resolution)
            self.generated_images = image_connections.get_images(self.last_api_response)

        self.display_images_with_regen_button()

    def display_images_with_regen_button(self):
        total_images = len(self.generated_images)
        if total_images > 0:
            cols = st.columns(total_images)
            for i, img in enumerate(self.generated_images):
                cols[i].image(img)
                cols[i].button(label=f"🔁", on_click=self.create_variations, kwargs={"img_id": i}, key=f"Regen {i}")

    def create_variations(self, img_id):
        self.last_api_response = image_connections.generate_image_variations(
            response=self.last_api_response, resp_id=img_id, num_images=self.images_to_gen_count,
            img_size=self.selected_resolution)
        self.generated_images = image_connections.get_images(self.last_api_response)

    def main_page(self):
        st.title("🤖 Chat GPT API")
        st.write("---")

        cols = st.columns(2)
        cols[0].write("Click on new chat to start generate text")
        cols[1].write("Click on images to generate images")

    def change_current_page_function(self, new_page):
        self.session_messages = []
        self.generated_images = []
        self.current_page_function = new_page

    def run(self):
        with st.sidebar:
            if st.button("🔤 New Chat"):
                self.change_current_page_function(self.text_gen_page)

            if st.button("🖼️ Images"):
                self.change_current_page_function(self.img_page)

            if self.api_key is None:
                new_api_key = st.text_input("insert apikey")
                if new_api_key:
                    self.api_key = new_api_key

        self.current_page_function()


if "front_end_instance" not in st.session_state:
    front_end_instance = FrontEnd()
    st.session_state.front_end_instance = front_end_instance

st.session_state.front_end_instance.run()
