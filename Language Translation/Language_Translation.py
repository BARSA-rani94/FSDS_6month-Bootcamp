import streamlit as st
from mtranslate import translate
import pandas as pd
import os
from gtts import gTTS
import base64

# Read dataset
df = pd.read_csv(r"C:\Users\HP\Downloads\New folder\31st - spacy\MULTIPLE LANGUAGE TRANSLATION\language.csv")
df.dropna(inplace=True)
lang = df['name'].to_list()
langcode = df['iso'].to_list()
lang_array = {lang[i]: langcode[i] for i in range(len(langcode))}

st.title("🌍 Language Translation App")

inputtext = st.text_area("Enter text to translate:", height=100)
choice = st.sidebar.radio('SELECT LANGUAGE', tuple(lang))

speech_langs = {
    "af": "Afrikaans",
    "ar": "Arabic",
    "bg": "Bulgarian",
    "bn": "Bengali",
    "bs": "Bosnian",
    "ca": "Catalan",
    "cs": "Czech",
    "cy": "Welsh",
    "da": "Danish",
    "de": "German",
    "el": "Greek",
    "en": "English",
    "eo": "Esperanto",
    "es": "Spanish",
    "et": "Estonian",
    "fi": "Finnish",
    "fr": "French",
    "gu": "Gujarati",
    "od" : "odia",
    "hi": "Hindi",
    "hr": "Croatian",
    "hu": "Hungarian",
    "hy": "Armenian",
    "id": "Indonesian",
    "is": "Icelandic",
    "it": "Italian",
    "ja": "Japanese",
    "jw": "Javanese",
    "km": "Khmer",
    "kn": "Kannada",
    "ko": "Korean",
    "la": "Latin",
    "lv": "Latvian",
    "mk": "Macedonian",
    "ml": "Malayalam",
    "mr": "Marathi",
    "my": "Myanmar (Burmese)",
    "ne": "Nepali",
    "nl": "Dutch",
    "no": "Norwegian",
    "pl": "Polish",
    "pt": "Portuguese",
    "ro": "Romanian",
    "ru": "Russian",
    "si": "Sinhala",
    "sk": "Slovak",
    "sq": "Albanian",
    "sr": "Serbian",
    "su": "Sundanese",
    "sv": "Swedish",
    "sw": "Swahili",
    "ta": "Tamil",
    "te": "Telugu",
    "th": "Thai",
    "tl": "Filipino",
    "tr": "Turkish",
    "uk": "Ukrainian",
    "ur": "Urdu",
    "vi": "Vietnamese",
    "zh-CN": "Chinese"
}  # keep your dictionary here

def get_binary_file_downloader_html(bin_file, file_label='File'):
    with open(bin_file, 'rb') as f:
        data = f.read()
    bin_str = base64.b64encode(data).decode()
    href = f'<a href="data:application/octet-stream;base64,{bin_str}" download="{os.path.basename(bin_file)}">Download {file_label}</a>'
    return href

if not inputtext.strip():
    st.info("👋 Please type something above to translate.")
else:
    try:
        output = translate(inputtext, lang_array[choice])
        c1, c2 = st.columns([4,3])
        with c1:
            st.text_area("TRANSLATED TEXT", output, height=200)

        if lang_array[choice] in speech_langs.keys():
            aud_file = gTTS(text=output, lang=lang_array[choice], slow=False)
            aud_file.save("lang.mp3")
            with c2:
                audio_file_read = open('lang.mp3', 'rb')
                audio_bytes = audio_file_read.read()
                st.audio(audio_bytes, format='audio/mp3')
                st.markdown(get_binary_file_downloader_html("lang.mp3", 'Audio File'), unsafe_allow_html=True)
    except Exception as e:
        st.error(e)