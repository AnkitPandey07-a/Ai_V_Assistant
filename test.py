#yeha hum ne ek function banaya hai jo kisi bhi audio/video 
# file ko WAV format me convert karta hai aur fir usko chhote segments me todta hai. 
# Ye function pydub library ka use karta hai.


from utils.audio_processor import process_input
from core.transcriber import transcribe_all

source = "https://www.youtube.com/watch?v=W7W0Wacoun8&list=PL1BQkm1ZUCaVB6hh63DhcTs28NrwiR4N2&index=10"


chunks = process_input(source)

print("Transcription in progress...")
transcription = transcribe_all(chunks)
print("Transcription completed.")