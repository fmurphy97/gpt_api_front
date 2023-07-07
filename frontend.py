import streamlit as st
import text_connection
import image_connections

st.title("🤖 Chat GPT API")
st.write("---")


class FrontEnd:

    def __init__(self):

        with open('my apikey.txt', 'r') as file:
            self.api_key = file.read()

        self.num_image = 1
        self.selected_definition = "256x256"

    def main_page(self):

        new_question = st.text_input(label="Enter your question here")

        # context = connection_file.read_text_file("product_context.txt")
        context = ""

        if st.button("ASK  ▶"):
            answer = text_connection.ask_question(
                context,
                new_question,
                self.api_key)

            st.write("A: " + answer)

    def img_page(self):

        new_question = st.text_input(label="Enter your prompt here")
        self.num_image = st.slider('Select a number', 1, 10)

        # Define the available definitions
        definitions = ["256x256", "512x512", "1024x1024"]
        # Create the dropdown
        self.selected_definition = st.selectbox("Select Definition:", definitions)

        if st.button("Create Images"):
            api_response = image_connections.generate_images(prompt_message=new_question,
                                                             num_images=self.num_image,
                                                             img_size=self.selected_definition)

            self.display_imgs_with_regen_button(api_response)

    def display_imgs_with_regen_button(self, api_response):
        imgs = image_connections.get_images(api_response)

        cols = st.columns(len(imgs))
        for i, img in enumerate(imgs):
            cols[i].image(img)
            cols[i].button(label=f"variar {i}", on_click=image_connections.generate_image_variations, kwargs=
            dict(response=api_response, resp_id=i, num_images=self.num_image, img_size=self.selected_definition))
            # TODO: images dont display after this

    def run(self):
        tabs = st.tabs(["Text", "Image"])

        with tabs[0]:
            self.main_page()

        with tabs[1]:
            self.img_page()


if "front_end_instance" not in st.session_state:
    front_end_instance = FrontEnd()
    st.session_state.front_end_instance = front_end_instance

st.session_state.front_end_instance.run()
