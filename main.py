"""
Demo v0 for IDEP
Purpose: Prototype the process of recording audio, encrypting it, decrypting it and creating stored transcripts of it. 
By: Abigail Swallow
"""

# IMPORTS

from cryptography.fernet import Fernet
import speech_recognition as sr

# ENCRYPT AUDIO FILE

# Generate a key for encryption and decryption
key = Fernet.generate_key()
cipher_suite = Fernet(key)
print("Encryption key generated.")

# Open audio file
with open("audio/test01.wav", "rb") as audio_file:
    audio_bytes = audio_file.read()
print("Audio file encrypted.")

# Encrypt the audio bytes
encrypted_audio = cipher_suite.encrypt(audio_bytes)

# PLACEHOLDER - send audio file to db ??

# DECRYPT AUDIO FILE
decrypted_audio = cipher_suite.decrypt(encrypted_audio)

# Write the decrypted audio back to a temporary file to process into transcription
temp_audio_path = "temp_decrypted_audio.wav"
with open(temp_audio_path, "wb") as temp_audio_file:
    temp_audio_file.write(decrypted_audio)
print("Decrypted audio ready for speech recognition.")

# PROCESS AUDIO INTO WRITTEN TRANSCRIPT
r = sr.Recognizer()

# Load the decrypted audio file
with sr.AudioFile(temp_audio_path) as source:
    # Listen to the audio file
    audio = r.record(source)

# Create transcript
try:
    print("Google Speech Recognition thinks you said:")
    transcript = r.recognize_google(audio)
    print(transcript)
except sr.UnknownValueError:
    print("Google Speech Recognition could not understand audio")
except sr.RequestError as e:
    print("Could not request results from Google Speech Recognition service; {0}".format(e))

# Delete temporary audio path
import os
os.remove(temp_audio_path)
print("Temporary audio file removed.")
# PLACEHOLDER - delete whole audio file from db

# ENCRYPT THE TRANSCRIPT
encrypted_transcription = cipher_suite.encrypt(transcript.encode()) 
print("Transcription text encrypted.")

print("Process completed")
