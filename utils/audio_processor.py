import yt_dlp
import os
from pydub import AudioSegment
from typing import Any, cast

# Create a directory to store downloaded audio files    
DOWNLOAD_DIRECTORY = "downloads"
os.makedirs(DOWNLOAD_DIRECTORY, exist_ok=True) 

#ye function downloads audio from youtube and 
# saves it in the downloads folder
def download_youtube_audio(url :str) -> str:
    output_path = os.path.join(DOWNLOAD_DIRECTORY, '%(title)s.%(ext)s')

# ye ydl_opts dictionary specifies the options for yt_dlp, including the 
# format of the audio to download, the output template for the filename, and the
#  postprocessor to convert the audio to WAV format. The "quiet" option suppresses 
# the output of yt_dlp to keep the console clean.
    ydl_opts: dict[str, Any] = {
        'format': 'bestaudio/best',
        'outtmpl': output_path,
            
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'wav',
            'preferredquality': '192',
        }],
        #this option suppresses the output of yt_dlp to keep the console clean
        "quiet": True,
    }
# you can use yt_dlp to download the audio from the given YouTube URL and save it as a WAV file in the specified downloads directory. 
# The function `download_youtube_audio` takes a YouTube URL as input and returns the filename of the downloaded audio file.
    with yt_dlp.YoutubeDL(cast(Any, ydl_opts)) as ydl:
        info_dict = ydl.extract_info(url, download=True)

        filename = ydl.prepare_filename(info_dict)
        filename = os.path.splitext(filename)[0] + ".wav"

        return filename




## isme humne ek function banaya hai jo kisi bhi audio/video 
# file ko WAV format me convert karta hai. Ye function pydub 
# library ka use karta hai.
def convert_audio_to_wav(input_path: str) -> str:

    """Convert an audio/video file to WAV format using pydub."""

# ye auto segment class ka use karke input file ko load karta hai,
# fir usko mono me convert karta hai aur frame rate ko 16000 Hz set karta hai. 
# Finally, ye converted audio ko WAV format me export karta hai aur output file ka path return karta hai.
    audio = AudioSegment.from_file(input_path)
    output_path = os.path.splitext(input_path)[0] + "_convertd.wav"
    audio = audio.set_channels(1).set_frame_rate(16000)  # Convert to mono
    audio.export(output_path, format="wav")
    return output_path



# isme hum ne ek function banaya hai jo kisi bhi audio file ko chhote segments me todta hai.
#  Ye function pydub library ka use karta hai.
def chunk_audio(wav_path: str, chunk_length_minutes: int = 10) -> list[str]:
    """Chunk an audio file into smaller segments of specified length in minutes."""
    audio = AudioSegment.from_wav(wav_path)

# ye chunk_length_minutes ko milliseconds me convert karta hai,
#  fir audio ko specified length ke chunks me todta hai.
    chunk_length_ms = chunk_length_minutes * 60 * 1000  # Convert minutes to milliseconds

# ye loop audio ko chunks me todta hai aur har chunk ko alag file me save karta hai.
    chunks = []
    for i, start in enumerate(range(0, len(audio), chunk_length_ms)):
        chunk = audio[start:start + chunk_length_ms]
        chunk_path = f"{wav_path[:-4]}_chunk_{i}.wav"
        chunk.export(chunk_path, format="wav")

        chunks.append(chunk_path)
    return chunks

def process_input(source: str) -> list:
    """Process the input source (YouTube URL or local file path) and return a list of WAV file paths."""
    if source.startswith("http://") or source.startswith("https://"):
# If the source is a YouTube URL, download the audio
        print("Detected YouTube URL. Downloading audio...")
        wav_path = download_youtube_audio(source)
    else:
# If the source is a local file path, convert it to WAV
        print("Detected local file. Converting to WAV...")
        wav_path = convert_audio_to_wav(source)

# Chunk the WAV file into smaller segments
    print("Chunking audio into smaller segments...")
    chunks = chunk_audio(wav_path)
    print(f"Audio processing complete. Generated {len(chunks)} chunk(s) created.")
    return chunks