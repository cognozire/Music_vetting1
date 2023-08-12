import streamlit as st
import os
import aubio
from collections import Counter

def midi_to_note_name(midi_note):
    note_names = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
    note_name = note_names[midi_note % 12]
    return note_name

st.title("Audio Processing App")

uploaded_file = st.file_uploader("Choose an audio file", type=["mp3", "wav"])

if uploaded_file is not None:
    temp_audio_dir = "temp_audio"
    os.makedirs(temp_audio_dir, exist_ok=True)
    temp_audio_file_path = os.path.join(temp_audio_dir, uploaded_file.name)
    
    with open(temp_audio_file_path, "wb") as f:
        f.write(uploaded_file.read())

    # Convert the uploaded file to WAV format using librosa
    import librosa
    y, sr = librosa.load(temp_audio_file_path, sr=None)
    temp_wav_file_path = os.path.splitext(temp_audio_file_path)[0] + ".wav"
    librosa.output.write_wav(temp_wav_file_path, y, sr)
    
    samplerate = sr  # Use the sample rate from the converted WAV file
    win_s = 4096
    hop_s = 512
    pitch_o = aubio.pitch("yin", win_s, hop_s, samplerate)
    pitch_o.set_unit("midi")
    pitch_o.set_tolerance(0.8)

    if st.button("Calculate Similarity"):
        audio_file = aubio.source(temp_wav_file_path, samplerate, hop_s)

        notes = []

        while True:
            samples, read = audio_file()
            pitch = pitch_o(samples)[0]

            if pitch != 0:
                note = int(pitch)
                note_name = midi_to_note_name(note)
                notes.append(note_name)

            if read < hop_s:
                break
        audio_file.close()
        
        # Delete the temporary audio files after processing
        os.remove(temp_audio_file_path)
        os.remove(temp_wav_file_path)
        
        note_counts = Counter(notes)
        most_common_note = note_counts.most_common(1)[0][0]
        st.write(f"The most common note in the audio is: {most_common_note}")
