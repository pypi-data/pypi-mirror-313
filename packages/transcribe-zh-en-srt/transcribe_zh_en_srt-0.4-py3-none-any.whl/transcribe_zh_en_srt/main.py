import argparse
import os
import requests
from dotenv import load_dotenv
import demucs.separate
import shutil
import re
from datetime import datetime, timedelta
import torch

def load_api_key(secrets_dir=None):
    """
    Load the OpenAI API key from the .env file located in the secrets directory.
    If no secrets directory is provided, it will look for the .env file in the current working directory.
    """
    if secrets_dir:
        dotenv_path = os.path.join(secrets_dir, '.env')
    else:
        dotenv_path = '.env'  # Default to the current directory

    if os.path.exists(dotenv_path):
        load_dotenv(dotenv_path)  # Load the .env file
        api_key = os.getenv('OPENAI_API_KEY')  # Fetch the OpenAI API key from the .env file
        if not api_key:
            print("API key not found in the .env file.")
        return api_key
    else:
        print(f"No .env file found at {dotenv_path}.")
        return None

def separate_audio(input_audio_path, video_dir, device):
    """
    Use Demucs to separate the audio and extract both the vocal and non-vocal tracks.
    """
    try:
        # Run Demucs for audio separation, explicitly specifying output directory
        print(f"Running Demucs separation on: {input_audio_path}")
        demucs.separate.main(['-n', 'htdemucs', '--two-stems=vocals', '--out', video_dir, '--device', device, input_audio_path])  # Separate into vocals and no_vocals
        
        video_base_name = os.path.basename(video_dir)

        # Define the output directory where Demucs saves files
        output_dir = os.path.join(video_dir, 'htdemucs', f'{video_base_name}_audio')  # Look for separated audio in this folder
        print(f"Contents of the directory after Demucs: {os.listdir(output_dir)}")
        print(f"Demucs output directory: {output_dir}")

        # Find the 'vocals.wav' and 'no_vocals.wav' files from Demucs output
        vocals_dir = os.path.join(output_dir, 'vocals.wav')
        non_vocals_dir = os.path.join(output_dir, 'no_vocals.wav')

        if os.path.exists(vocals_dir) and os.path.exists(non_vocals_dir):
            print(f"Found vocals.wav at: {vocals_dir} and no_vocals.wav at: {non_vocals_dir}")

            # Construct the new names with the original file name and suffixes
            new_vocals_path = os.path.join(video_dir, f'vocals.wav')
            new_non_vocals_path = os.path.join(video_dir, f'{video_base_name}_non_vocals.wav')

            # Move both files to the desired locations
            shutil.move(vocals_dir, new_vocals_path)
            shutil.move(non_vocals_dir, new_non_vocals_path)
            print(f"Moved vocals.wav to: {new_vocals_path} and no_vocals.wav to: {new_non_vocals_path}")
            
            # Process the vocals.wav to convert it to mono and reduce bitrate
            processed_vocals_path = os.path.join(video_dir, f'{video_base_name}_vocals_processed.wav')
            print(f"Processing vocals to mono and reducing bitrate: {processed_vocals_path}")
            ffmpeg_command = f"ffmpeg -y -i {new_vocals_path} -ac 1 -ar 16000 -b:a 128k {processed_vocals_path}"
            os.system(ffmpeg_command)
            print(f"Processed vocals file saved at: {processed_vocals_path}")

            # Remove the htdemucs directory and everything underneath it
            shutil.rmtree(os.path.join(video_dir, 'htdemucs'))
            print(f"Removed the htdemucs directory and its contents.")

            return new_vocals_path, new_non_vocals_path
        else:
            print(f"Error: No vocals.wav or no_vocals.wav found in the 'separated' directory.")
            return None, None

    except Exception as e:
        print(f"Error processing with Demucs: {e}")
        return None, None


def send_audio_to_openai(api_key, audio_file, subtitle_file, input_lang):
    """
    Send the audio file to OpenAI's /v1/audio/translations endpoint to get a translation/transcription
    in SRT format based on the provided subtitle prompt.
    """
    # Initialize the language variables
    if input_lang == "zh":
        desired_input_lang = "Chinese Language"
    else:
        desired_input_lang = "Chinese Language"
    
    desired_target_lang = "English Language"  # Target language for translation
    target_lang = 'en'

    
    url = "https://api.openai.com/v1/audio/translations"

    # Prepare the prompt from the subtitle text
    try:
        with open(subtitle_file, 'r', encoding='utf-8') as f:
            prompt_text = f.read()
    except FileNotFoundError:
        print(f"Subtitle file not found: {subtitle_file}")
        return None

    try:
        # Open the audio file
        with open(audio_file, 'rb') as audio:
            files = {'file': audio}
            
            # Prepare the prompt for the translation
            prompt = {
                "prompt": f"use the provided text {prompt_text} as baseline for original subtitles, and convert from {desired_input_lang} to {desired_target_lang}. The srt formatted file must only contain {desired_target_lang} and not a mix of languages."
            }

            headers = {
                "Authorization": f"Bearer {api_key}",
            }

            data = {
                'model': 'whisper-1',  # Whisper model
                'language': target_lang,  # Language to translate to
                'response_format': 'verbose_json',  # Get detailed response for segments and timestamps
                'timestamp_granularities[]': 'segment',  # Ensure segment-level timestamps
                'prompt': prompt
            }

            # Send the POST request to OpenAI API
            response = requests.post(url, headers=headers, data=data, files=files)

            if response.status_code == 200:
                return response.json()  # Return the full response as JSON to handle detailed segment data
            else:
                print(f"Error: {response.status_code}, {response.text}")
                return None
    except Exception as e:
        print(f"Error processing audio file: {e}")
        return None


def translate_srt_with_chat(api_key, srt_content, target_lang):
    """
    Translate the given SRT content (in English) into the target language using a direct POST request to the OpenAI API.

    This version does not use sessions, proxies, or retries. It directly calls the API with requests.post.
    """
    
    if target_lang == 'en':
        return srt_content

    language_map = {
        'fr': "French",
        'de': "German",
        'es': "Spanish",
        'zh': "Chinese",
        'ar': "Arabic"
    }

    if target_lang not in language_map:
        print(f"Error: Target language '{target_lang}' is not supported.")
        return None

    desired_target_lang = language_map[target_lang]

    messages = [
        {
            "role": "system",
            "content": (
                "You are a professional subtitle translator. Your task is to translate provided subtitle text "
                "into the specified target language while strictly preserving the SRT format, including timing "
                "and numbering. Do not add extra commentary or text outside the subtitle entries."
            )
        },
        {
            "role": "user",
            "content": (
                f"Please translate the following SRT subtitles from English into {desired_target_lang} language. "
                f"All subtitle lines must be fully translated into {desired_target_lang}, preserving the exact SRT structure, "
                f"including the numbering and timestamps. The output should contain no additional explanations or formatting errors. "
                f"Only return the translated SRT file content.\n\n{srt_content}"
            )
        }
    ]

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "gpt-4",  # or "gpt-3.5-turbo" if needed
        "messages": messages,
        "temperature": 0.2
    }

    try:
        response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=data)
        if response.status_code == 200:
            result = response.json()
            translated_srt = result['choices'][0]['message']['content']
            return translated_srt
        else:
            print(f"Error during chat completion translation: {response.status_code}, {response.text}")
            return None
    except requests.RequestException as e:
        print(f"Network error during chat completion translation: {e}")
        return None

def convert_to_srt(transcription_json):
    """
    Convert the verbose JSON transcription response into SRT format.
    """
    segments = transcription_json.get('segments', [])
    if not segments:
        print("No transcription segments found.")
        return ""

    srt_output = []
    index = 1

    for segment in segments:
        start_time = segment['start']
        end_time = segment['end']
        text = segment['text']

        # Format the start and end times in SRT format (HH:MM:SS,MS)
        start_str = format_time(start_time)
        end_str = format_time(end_time)

        srt_output.append(f"{index}")
        srt_output.append(f"{start_str} --> {end_str}")
        srt_output.append(text)
        srt_output.append("")  # Blank line to separate subtitles

        index += 1

    return "\n".join(srt_output)

def format_time(seconds):
    """
    Convert seconds to SRT time format: HH:MM:SS,MS
    """
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = int(seconds % 60)
    milliseconds = int((seconds * 1000) % 1000)

    return f"{hours:02}:{minutes:02}:{seconds:02},{milliseconds:03}"

# Example of saving the SRT file after transcription:
def save_srt_file(srt_content, output_path):
    try:
        with open(output_path, 'w', encoding='utf-8') as srt_file:
            srt_file.write(srt_content)
        print(f"SRT file saved: {output_path}")
    except Exception as e:
        print(f"Error saving SRT file: {e}")

# Helper function to parse SRT timestamp
def parse_srt_timestamp(timestamp: str) -> timedelta:
    return datetime.strptime(timestamp, "%H:%M:%S,%f") - datetime(1900, 1, 1)

# Helper function to format timedelta to SRT timestamp format
def format_srt_timestamp(td: timedelta) -> str:
    total_seconds = int(td.total_seconds())
    milliseconds = int((td.total_seconds() - total_seconds) * 1000)
    return str(timedelta(seconds=total_seconds)).split('.')[0] + f",{milliseconds:03d}"

# Estimate audio length based on word count (words per minute average 150)
def estimate_audio_length(word_count: int, wpm=150) -> timedelta:
    audio_length_minutes = word_count / wpm
    return timedelta(minutes=audio_length_minutes)

# Function to fix the start time of the first subtitle based on the audio length estimate
def fix_first_segment_start_time(srt_file_path):
    with open(srt_file_path, 'r') as file:
        srt_content = file.read()

    # Split the SRT content into blocks for each subtitle
    srt_blocks = srt_content.split('\n\n')

    # Get the first subtitle block (index 0)
    first_segment = srt_blocks[0]
    
    # Extract the timestamp and content from the first segment
    match = re.match(r'(\d+)\n([\d:,]+) --> ([\d:,]+)\n(.+)', first_segment, re.DOTALL)
    if match:
        segment_number = match.group(1)
        start_time = match.group(2)
        end_time = match.group(3)
        text = match.group(4)

        # Count the words in the segment text (naive word count)
        word_count = len(text.split())
        
        # Estimate the audio length for the segment
        estimated_audio_length = estimate_audio_length(word_count)

        # Calculate the correct start time for the first segment
        end_time_obj = parse_srt_timestamp(end_time)
        correct_start_time = end_time_obj - estimated_audio_length

        # Format the new start time
        corrected_start_time = format_srt_timestamp(correct_start_time)

        # Replace the start time in the first segment
        updated_first_segment = first_segment.replace(start_time, corrected_start_time, 1)
        
        # Reconstruct the entire SRT content with the updated first segment
        updated_srt_content = updated_first_segment + '\n\n' + '\n\n'.join(srt_blocks[1:])

        # Write the updated content back to the SRT file
        with open(srt_file_path, 'w') as file:
            file.write(updated_srt_content)

        print(f"First segment start time corrected to: {corrected_start_time}")
    else:
        print("Failed to parse SRT content.")

# Existing function to process the video directory
def process_video_directory(input_dir, api_key, device,  input_lang, target_lang):
    """Process each subdirectory under the input directory, look for audio and subtitle files."""
    for root, dirs, files in os.walk(input_dir):
        for dir_name in dirs:
            video_dir = os.path.join(root, dir_name)
            video_base_name = os.path.basename(video_dir)
            print(f"Looking inside video directory: {video_dir}")
            
            # Find the audio and subtitle files
            audio_file = None
            subtitle_file = None
            for file in os.listdir(video_dir):
                if file.endswith("_audio.wav"):
                    audio_file = os.path.join(video_dir, file)
                elif file.endswith("_audio.wav_zh.txt"):
                    subtitle_file = os.path.join(video_dir, file)
            
            if audio_file and subtitle_file:
                print(f"Found audio file: {audio_file}")
                print(f"Found subtitle file: {subtitle_file}")
                
                # Step 1: Use Demucs to separate the audio
                separated_audio_file = separate_audio(audio_file, video_dir, device)
                if not separated_audio_file:
                    print("Error: Demucs audio separation failed.")
                    return
                
                # Step 2: Ensure only the processed vocals file is used (remove the original vocals.wav if it exists)
                
                vocals_processed_path = os.path.join(video_dir, f"{video_base_name}_vocals_processed.wav")
                print(vocals_processed_path)
                print(os.path.exists(vocals_processed_path))
                if os.path.exists(vocals_processed_path):
                    print(f"Found processed vocals file: {vocals_processed_path}")
                    os.remove(os.path.join(video_dir, "vocals.wav"))  # Remove the original vocals.wav
                    print(f"Removed original vocals file: vocals.wav")
                else:
                    print(f"Error: Processed vocals file not found.")
                    return
                
                # Step 3: Send the audio and subtitle files to OpenAI
                result = send_audio_to_openai(api_key, vocals_processed_path, subtitle_file, input_lang)
                if result:
                    print("Transcription and alignment complete.")
                    # Save initial English SRT
                    srt_content = convert_to_srt(result)
                    intermediate_srt_path = os.path.join(video_dir, f"{dir_name}_translated_{input_lang}_en.srt")
                    save_srt_file(srt_content, intermediate_srt_path)
                    fix_first_segment_start_time(intermediate_srt_path)

                    # Check if target_lang is not English
                    if target_lang != 'en':
                        # Read the English SRT content
                        with open(intermediate_srt_path, 'r', encoding='utf-8') as f:
                            english_srt_content = f.read()

                        # Translate using the chat completion endpoint
                        translated_srt = translate_srt_with_chat(api_key, english_srt_content, target_lang)
                        if translated_srt:
                            # Save the translated SRT with the final name
                            final_srt_path = os.path.join(video_dir, f"{dir_name}_translated_{input_lang}_{target_lang}.srt")
                            save_srt_file(translated_srt, final_srt_path)
                            # Optionally remove the intermediate English SRT if you don't need it
                            # os.remove(intermediate_srt_path)
                        else:
                            print("Failed to translate SRT into target language.")
                    else:
                        # If target_lang is 'en', you already have the final SRT.
                        final_srt_path = intermediate_srt_path
                else:
                    print(f"Failed to process {video_dir}.")
                    
def main():
    parser = argparse.ArgumentParser(description="Audio Transcription and Translation")
    
    # Required flag: input directory
    parser.add_argument('--input-dir', required=True, help='Path to input directory containing subdirectories of video names.')
    
    # Optional flags
    parser.add_argument('--secrets-dir', help='Directory containing .env file with API key.')
    parser.add_argument('--input-lang', default='zh', help='Language of the input audio file. Default is Chinese (zh).')
    parser.add_argument('--target-lang', default='en', help='Target language for translation. Default is English (en). Other available languages: zh, es, fr, de, ar.')

    # Flags for API keys
    parser.add_argument('--openai-api-token', help='OpenAI API key (if not using secrets-dir).')
    
    # Add device option
    parser.add_argument('--device', default='cpu', help='Device to run Demucs on (default: cpu) or "cuda" if you want to use GPU).')

    args = parser.parse_args()

    # Determine the API key
    api_key = None
    if args.secrets_dir:
        api_key = load_api_key(args.secrets_dir)  # Load from secrets directory
    elif args.openai_api_token:
        api_key = args.openai_api_token  # Use the token directly

    if not api_key:
        print("API key not provided. Exiting.")
        return
    
    
    device = None
    if args.device == 'cuda' and torch.cuda.is_available():
        device = 'cuda'
        print("Using GPU")
    else:
        device = 'cpu'
        print("Using CPU")

    # Process the input directory
    process_video_directory(args.input_dir, api_key, device, args.input_lang, args.target_lang)

if __name__ == "__main__":
    main()