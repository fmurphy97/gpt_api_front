import streamlit as st
import text_connection
import image_connections

st.title("🤖 Chat GPT API")
st.write("---")


class FrontEnd:

    def __init__(self):

        with open('my apikey.txt', 'r') as file:
            self.api_key = file.read()

        self.images_to_gen_count = 1
        self.selected_resolution = "256x256"

        self.last_api_response = None
        self.generated_images = []

    def main_page(self):

        model_to_use = st.selectbox(
            "Select Model to Use",
            options=["gpt-4", "gpt-3.5-turbo", "text-davinci-003", "text-davinci-002",
                     "davinci", "curie", "babbage", "ada"])

        new_question = st.text_input(label="Enter your question here")

        # context = connection_file.read_text_file("product_context.txt")
        context = ""

        if st.button("ASK  ▶", key="button to ask question"):
            answer = text_connection.ask_question(
                context,
                new_question,
                self.api_key,
                model_to_use)

            st.write(answer)

    def img_page(self):

        new_question = st.text_input(label="Enter your prompt here")
        self.images_to_gen_count = st.slider('Select a number', 1, 10)

        # Define the available definitions
        definitions = ["256x256", "512x512", "1024x1024"]
        # Create the dropdown
        self.selected_resolution = st.selectbox("Select Definition:", definitions)

        if st.button("CREATE ▶", key="button to create images"):
            self.last_api_response = image_connections.generate_images(
                prompt_message=new_question, num_images=self.images_to_gen_count, img_size=self.selected_resolution)
            self.generated_images = image_connections.get_images(self.last_api_response)

        self.display_imgs_with_regen_button()

    def display_imgs_with_regen_button(self):
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
