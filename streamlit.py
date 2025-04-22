import os
import openai
from streamlit import st

# Initialize OpenAI client with API key (replace with your actual key)
openai.api_key = "YOUR_OPENAI_API_KEY"

def main():
    # Title
    st.title("Notarized Language Translation App")

    # Description
    st.write("Translate text between languages with AI assistance. Note: This app handles translation, not notarization.")

    # Input Section
    with st.form("translation_form"):
        original_text = st.text_area("Enter Original Text:", height=150)
        from_lang = st.selectbox("From Language", options=list(openai_LANGUAGES))
        to_lang = st.selectbox("To Language", options=list(openai_LANGUAGES))
        submitted = st.form_submit_button("Translate")

    # Translation Section
    if submitted:
        if not original_text:
            st.warning("Please enter text to translate.")
            return

        try:
            with st.spinner("Translating..."):
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": f"You are a notary assistant who verifies translations."},
                        {"role": "user", "content": f"Verify the translation of this text: {original_text} from {from_lang} to {to_lang}. Ensure it is accurate and notarized. Provide only the translation
text in English."}
                    ]
                )
                translation = response.choices[0].message.content
                st.write("Translation:", translation)

        except openai.APIError as e:
            st.error(f"OpenAI API Error: {str(e)}")

if __name__ == "__main__":
    main()