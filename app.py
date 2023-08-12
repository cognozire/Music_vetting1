import streamlit as st

import numpy as np
import aubio
from collections import Counter

import os
def midi_to_note_name(midi_note):
    note_names = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
    note_name = note_names[midi_note % 12]
    return note_name

st.title("Audio Processing App")

uploaded_file = st.file_uploader("Choose an audio file", type=["mp3", "wav"])

   

# Dropdown menu with musical notes
musical_notes = ['A', 'A#', 'B', 'C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#']
selected_note = st.selectbox("Select a musical note", musical_notes)

if uploaded_file is not None:
    temp_audio_dir = "temp_audio"
    os.makedirs(temp_audio_dir, exist_ok=True)  # Create the temporary directory if it doesn't exist
    temp_audio_file_path = os.path.join(temp_audio_dir, uploaded_file.name)
    
    with open(temp_audio_file_path, "wb") as f:
        f.write(uploaded_file.read())

    # Rest of your code remains the same
    samplerate = 48000
    win_s = 4096
    hop_s = 512
    pitch_o = aubio.pitch("yin", win_s, hop_s, samplerate)
    pitch_o.set_unit("midi")
    pitch_o.set_tolerance(0.8)

    if st.button("Calculate Similarity"):
        audio_file = aubio.source(temp_audio_file_path, samplerate, hop_s)

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
        
        # Delete the temporary audio file after processing
        os.remove(temp_audio_file_path)
        
        note_counts = Counter(notes)
        most_common_note = note_counts.most_common(1)[0][0]
        if selected_note == most_common_note:
            st.write(f"The given note is {selected_note}.")
        else:
            st.write(f"The given note doesn't match with {selected_note}.")





