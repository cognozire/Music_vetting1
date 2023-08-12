import streamlit as st
import librosa
import random
import numpy as np
import aubio
from collections import Counter
from scipy.spatial.distance import cosine
import os
def midi_to_note_name(midi_note):
    note_names = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
    note_name = note_names[midi_note % 12]
    return note_name

st.title("Audio Processing App")

uploaded_file = st.file_uploader("Upload an audio file", type=["mp3", "wav"])

# Dropdown menu with musical notes
musical_notes = ['A', 'A#', 'B', 'C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#']
selected_note = st.selectbox("Select a musical note", musical_notes)

if uploaded_file is not None:
    samplerate = 44100
    win_s = 4096
    hop_s = 512
    pitch_o = aubio.pitch("yin", win_s, hop_s, samplerate)
    pitch_o.set_unit("midi")
    pitch_o.set_tolerance(0.8)

    if st.button("Calculate Similarity"):
        audio_file = aubio.source(uploaded_file, samplerate, hop_s)

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
        note_counts = Counter(notes)
        most_common_note = note_counts.most_common(1)[0][0]
        if(selected_note==most_common_note):
            st.write(f"The given note is {selected_note}.")
        else:
            st.write(f"The given not doesn't matches with {selected_note}.")




