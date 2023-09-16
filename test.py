import assemblyai as aai
import streamlit as st
import streamlit_scrollable_textbox as stx
import tempfile
import os


aai.settings.api_key = f"24082ce0e2f84f818b64da2d3b0b27fd" 

st.set_page_config(
    page_title="Post Call Analytics",
    layout="wide",
)


def final_sentiment(transcript):
    negative, positive = 0,0
    for sentiment in transcript.sentiment_analysis:
        if sentiment.sentiment == "NEGATIVE" :
            negative += 1
        elif sentiment.sentiment == "POSITIVE" :
            positive += 1
    return positive - negative


def Transcribe(file):
    transcriber = aai.Transcriber()
    config = aai.TranscriptionConfig(speaker_labels=True,
                                    sentiment_analysis=True,
                                    summarization=True,
                                    summary_type=aai.SummarizationType.paragraph)
    print(file)
    transcript = transcriber.transcribe(file, config=config)
    # outputfile = "output.json"
    # with open(outputfile, "w") as f:
    #     json.dump(transcript.json_response, f, indent=4)
    # print(f"Speaker {utterance.speaker}: {utterance.text}")
    # transcript = transcript.json_response
    text = ""
    st.header("Transcript")
    for utterance in transcript.utterances:
        text += f"Speaker {utterance.speaker}: {utterance.text}\n"
    stx.scrollableTextbox(text, height=500)
    satisfaction = final_sentiment(transcript)
    st.header("Summary")
    st.write(transcript.summary)
    if satisfaction > 0 :
        st.success("The customer is satisfied 😀")
    elif satisfaction < 0 :
        st.error("The customer is not satisfied 😞")
    st.download_button('download transcript', text)
    
        
    
    
    # print each word and it's confidence score
    # for i,word in enumerate(transcript.words):
    #     print(f"{word.text} ({word.confidence})")
    # api_response = {
    # "words": []
    # }
    # for i, word in enumerate(transcript.words):
    # Create a dictionary for the word and add it to the "words" list
        # api_response["words"].append({"text": word.text, "confidence": word.confidence})

    # main(api_response)
    

# streamlit widget to upload audio file
# with st.sidebar.form("input"):
#     st.header("Upload your audio file")
#     audio_file = st.file_uploader("Choose a file", type=["wav", "mp3"])
#     if audio_file is not None:
#         st.audio(audio_file, format="audio/*")
#     temp_file = st.cache(audio_file, allow_output_mutation=True)
#     transcribe = st.form_submit_button(label="Start")

# if transcribe:
#    if audio_file is not None:
#        Transcribe(temp_file.name)

with st.sidebar.form("input"):
    st.header("Upload your audio file")
    # Create a file upload widget for audio files
    audio_file = st.file_uploader("Upload an audio file", type=["wav", "mp3", "ogg"])

    # Check if an audio file has been uploaded
    if audio_file is not None:
        # Create a temporary directory to store the uploaded audio
        temp_dir = tempfile.mkdtemp()

        # Define a temporary file path
        temp_audio_path = os.path.join(temp_dir, audio_file.name)

        # Save the uploaded audio to the temporary file
        with open(temp_audio_path, "wb") as temp_file:
            temp_file.write(audio_file.read())
    
    
    temp_file = st.cache(audio_file, allow_output_mutation=True)
    transcribe = st.form_submit_button(label="Transcribe")
    if transcribe:
        if audio_file is not None:
            # print(temp_audio_path)
            Transcribe(temp_audio_path)




