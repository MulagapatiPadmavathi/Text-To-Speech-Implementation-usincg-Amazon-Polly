import streamlit as st
import boto3
import os
from io import BytesIO
from PyPDF2 import PdfReader
import base64

polly_client = boto3.client(
    'polly',
    aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY'),
    region_name = os.getenv('AWS_DEFAULT_REGION', 'us-east-1')
)

if 'nav' not in st.session_state:
    st.session_state.nav = "home"

def set_nav(page):
    st.session_state.nav = page

col1, col2, col3 = st.columns(3)
with col1:
    if st.button("Home"):
        st.session_state.nav = "home"
with col2:
    if st.button("Document"):
        st.session_state.nav = "document"
with col3:
    if st.button("Text"):
        st.session_state.nav = "text"

nav = st.session_state.nav

def load_css():
    image_path = 'Landing Page bg.jpg'

    try:
        with open(image_path, 'rb') as image_file:
            base64_image = base64.b64encode(image_file.read()).decode()

        css = f"""
        <style>
            .stApp {{
                background-image: url(data:image/jpeg;base64,{base64_image});
                background-size: cover;
                background-position: center;
                background-attachment: fixed;
            }}
        </style>
        """
        st.markdown(css, unsafe_allow_html = True)
    except FileNotFoundError:
        st.error(f"Error: File '{image_path}' not found. Check the path.")
    except Exception as e:
        st.error(f'An error occured: {e}')

load_css()

voices = polly_client.describe_voices()['Voices']
voice_options = {v['Name']: v['SupportedEngines'] for v in voices}

language_options = sorted(set(v['LanguageName'] for v in voices))
selected_language = st.sidebar.selectbox('Choose Language', language_options)

filtered_voices = [v for v in voices if v['LanguageName'] == selected_language]
gender_options = sorted(set(v['Gender'] for v in filtered_voices))
selected_gender = st.sidebar.radio('Choose Gender', gender_options)

selected_voice = st.sidebar.selectbox('Choose Voice', list(voice_options.keys()))
selected_engine = voice_options[selected_voice][0]

speed = st.sidebar.slider('Speech Speed', 0.25, 2.0, 1.0, 0.25)
volume = st.sidebar.slider('Volume', 0, 100, 50)

def synthesize_speech(text, voice, engine):
    response = polly_client.synthesize_speech(
        Text = text,
        VoiceId = voice,
        Engine = engine,
        OutputFormat = 'mp3',
        TextType = 'text'
    )
    return response['AudioStream'].read()

if nav == 'home':
    st.title('Text-To-Speech Converter App')
    st.write("""
        Welcome to the **Text-To-Speech Converter App**!
        This app converts text into **natural-sounding speech** using **Amazon Polly**.You can choose from a variety of voices, languages, and speech settings to customize your experience.
             """)
    st.markdown('Features:')
    st.markdown('- Supports multiple languages and voices')
    st.markdown('- Adjustable speech speed and volume')
    st.markdown('- Uplaod and convert text from **documents**')
    st.markdown('- Manually enter text for conversion')
    st.markdown('- **Preview & download** the generated speech')

    st.info('Perfect for **audiobooks, e-learning, and accessibility tools**! Try it now.')

elif nav == 'document':
    st.title('Convert Document to Speech')

    uploaded_file = st.file_uploader('Upload a PDF document (Max 1000 characters)', type = ['pdf'])

    def extract_text_from_pdf(pdf_file):
        try:
            reader = PdfReader(pdf_file)
            text = ''
        
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text.strip() + ' '
            
            text = text.strip()
            st.write(f'Extracted Characters: {len(text)}/1000')
            
            return text[:1000] if text else None

        except Exception as e:
            st.error(f'Error extracting text from PDF: {e}')
            return None

    extracted_text = None
    if uploaded_file is not None:
        extracted_text = extract_text_from_pdf(uploaded_file)
        if extracted_text:
            st.success('Text Extracted Successfully!')
            st.text_area('Extracted Text', extracted_text, height = 200)

    if st.button('Generate Speech from PDF Text'):
        if extracted_text:
            audio_data = synthesize_speech(extracted_text, selected_voice, selected_engine)
            st.audio(BytesIO(audio_data), format = 'audio/mp3')
            st.success('PDF text converted to speech successfully!')
        else:
            st.error('Please upload a PDF file and extract text first.')

elif nav == 'text':
    st.title('Convert Text to Speech')

    text_input = st.text_area('Enter text to convert:', 'Hello, Welcome to the Text-To-Speech Converter.')

    if st.button('Generate Speech from Manual Text'):
        if text_input.strip():
            audio_data = synthesize_speech(text_input, selected_voice, selected_engine)
            st.audio(BytesIO(audio_data), format = 'audio/mp3')
            st.success('Manual text converted to Speech successfully!')
        else:
            st.error('Please enter text for conversion.')




