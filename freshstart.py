import assemblyai as aai
import streamlit as st
import streamlit_scrollable_textbox as stx
import tempfile
import os

aai.settings.api_key = f"5df2facc7d27404fbe5d820b2c766ed4"

st.set_page_config(
    page_title="Post Call Analytics",
    layout="wide",
)

config=aai.TranscriptionConfig(speaker_labels=True,
                               summarization=True,
                               sentiment_analysis=True,
                               summary_type=aai.SummarizationType.paragraph)
transcriber = aai.Transcriber()

def final_sentiment(transcript):
    negative, positive = 0,0
    for sentiment in transcript.sentiment_analysis:
        if sentiment.sentiment == "NEGATIVE" :
            negative += 1
        elif sentiment.sentiment == "POSITIVE" :
            positive += 1
    return positive - negative


with st.sidebar.form("..."):
    st.header("POST CALL ANALYSIS")
    audio_file = st.file_uploader("Upload an audio file", type=["wav","mp3"])
    if audio_file is not None:
        temp_dir = tempfile.mkdtemp()
        audio_file_name = "audio.wav"
        audio_file_path = os.path.join(temp_dir, audio_file_name)
        with open(audio_file_path, "wb") as temp_audio_file:
            temp_audio_file.write(audio_file.read())
        

    submit_button = st.form_submit_button(label="Transcribe")

if submit_button and audio_file:
    transcript = transcriber.transcribe(
    audio_file_path,
    config=config
    )
    # for key in transcript.json_response:
    #     print(key)
    print(transcript)
    st.header("Transcript")
    text=""
    for utterance in transcript.utterances:
    #     print(type(utterance))
        text += f"Speaker {utterance.speaker}: {utterance.text}\n"
    stx.scrollableTextbox(text, height=500)
    st.header("Summary")
    st.write(transcript.summary)
    satisfaction = final_sentiment(transcript)
    if satisfaction > 0 :
        st.success("The customer is satisfied 😀")
    elif satisfaction < 0 :
        st.error("The customer is not satisfied 😞")
    st.download_button('download transcript', text)
    temp_audio_file.close()