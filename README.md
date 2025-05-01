🗣️ **Text-to-Speech Converter App**
This is a Streamlit-based web application that converts text into natural-sounding speech using Amazon Polly, a powerful cloud service from AWS. It supports multiple languages, voices, and allows you to adjust the speech speed and volume. You can input text manually or extract it from a PDF file.

Features
🌍 Support for multiple languages and accents

🧑‍🤝‍🧑 Choose voice gender and voice style

🎚️ Adjustable speech speed and volume

📄 Convert text from uploaded PDF documents

✍️ Enter and convert custom text

🔊 Listen to or download generated speech

🎨 Custom background and simple UI using Streamlit

**App Overview**

Home
An introduction to the app and its core features.

Convert Document
Upload a .pdf file (up to 1000 characters of extractable text) and convert the content into speech.

Convert Text
Manually enter any text and convert it to speech.

*Tech Stack*
Python 3.8+

Streamlit for UI

Amazon Polly for speech synthesis

boto3 for AWS API interaction

PyPDF2 for PDF text extraction

base64 for embedding background imag
