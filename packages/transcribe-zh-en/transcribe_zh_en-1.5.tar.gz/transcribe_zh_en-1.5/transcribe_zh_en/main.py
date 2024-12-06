import os
import argparse
import subprocess
import asyncio
from transcribe_zh_en.audio_to_text import asr_to_zh
import paddle
import logging
import time

# Check for gpu support
if paddle.is_compiled_with_cuda():
    print("GPU is recognized and working.")
else:
    print("GPU is not recognized. The script will run on CPU.")

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Validate if CUDA is available
def validate_device(device):
    # Check for Paddle or PyTorch CUDA support
    if device == 'gpu':
        if paddle.is_compiled_with_cuda():
            logging.info("CUDA is available in Paddle. Using GPU.")
        else:
            logging.info("CUDA is not available in Paddle. Falling back to CPU.")
            return 'cpu'
    return device

# Check if the video has subtitles
def has_subtitles(video_path):
    try:
        probe = subprocess.run(
            ['ffprobe', '-v', 'error', '-select_streams', 's', '-show_entries', 'stream=index', '-of', 'csv=p=0', video_path],
            capture_output=True, text=True
        )
        return bool(probe.stdout.strip())
    except subprocess.CalledProcessError:
        return False

# Function to extract subtitles from video
def detach_subtitles(input_video, output_subtitles):
    try:
        if has_subtitles(input_video):
            subprocess.run(['ffmpeg', '-i', input_video, '-map', '0:s:0', '-c', 'copy', output_subtitles], check=True)
            print(f"Subtitles extracted to {output_subtitles}")
        else:
            print(f"No subtitles found in {input_video}")
    except subprocess.CalledProcessError as e:
        print(f"Error during subtitle extraction: {e}")

def detach_audio(input_video, output_audio, output_video_no_audio):
    try:
        logging.info(f"Detaching audio from: {input_video}")
        
        # Detach and convert audio
        ffmpeg_audio_command = [
            'ffmpeg',
            '-y',  # Overwrite output files without asking
            '-i', input_video,
            '-vn',
            '-acodec', 'pcm_s16le',
            '-ar', '16000',
            '-ac', '1',
            output_audio
        ]
        logging.info(f"Extracting and converting audio with command: {' '.join(ffmpeg_audio_command)}")
        subprocess.run(ffmpeg_audio_command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        logging.info(f"Audio detached and converted to {output_audio}")
        
        # Detach video without audio
        ffmpeg_video_command = [
            'ffmpeg',
            '-y',
            '-i', input_video,
            '-an',
            '-vcodec', 'copy',
            output_video_no_audio
        ]
        logging.info(f"Extracting video without audio with command: {' '.join(ffmpeg_video_command)}")
        subprocess.run(ffmpeg_video_command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        logging.info(f"Video (without audio) saved to {output_video_no_audio}")
        
    except subprocess.CalledProcessError as e:
        logging.error(f"Error during audio detachment: {e.stderr.decode().strip()}")


# Transcribe audio to text (sequentially, without concurrency)
async def transcribe_audio(audio_paths, video_output_dir, stt_zh_flag, device):
    for audio_path in audio_paths:
        await transcribe_audio_single(audio_path, video_output_dir, stt_zh_flag, device)

# Transcribe a single audio file
async def transcribe_audio_single(audio_path, video_output_dir, stt_zh_flag, device):
    output_audio = os.path.join(video_output_dir, os.path.basename(audio_path))
    
    # Default to an empty string or another language if not processing in Chinese
    lang = "en"  # Default language

    if stt_zh_flag:
        lang = "zh"  # Override to Chinese if flag is set

    if os.path.exists(output_audio):
        start_time = time.time()
        logger.info(f"Starting time for processing {audio_path} at {time.ctime(start_time)}")
        
        # Transcribe audio to the selected language
        text = asr_to_zh(output_audio, lang, device)
        output_text_file = os.path.join(video_output_dir, f"{os.path.basename(audio_path)}_{lang}.txt")
        
        if text:
            # Save full transcription text to a file
            try:
                with open(output_text_file, "w", encoding='utf-8') as f:
                    f.write(text)  # Directly write the full text
                logger.info(f"Transcription saved to '{output_text_file}'")
            except Exception as e:
                logger.error(f"Failed to write transcription to '{output_text_file}': {e}")
        else:
            logger.info(f"No transcription available for '{audio_path}'")
        
        end_time = time.time()
        logger.info(f"Finished processing for {audio_path} at {time.ctime(end_time)}")
        logger.info(f"Time taken for ASR model <conformer_u2pp_online_wenetspeech> to finish processing: {end_time - start_time:.2f} seconds")
    else:
        logger.warning(f"Audio file '{output_audio}' not found. Skipping transcription.")


# Process each video
def process_video(video_path, processed_dir, detach_subtitles_flag, detach_audio_flag, stt_zh_flag, device="cpu"):
    video_name = os.path.splitext(os.path.basename(video_path))[0]
    video_output_dir = os.path.join(processed_dir, video_name)

    os.makedirs(video_output_dir, exist_ok=True)

    output_subtitles = os.path.join(video_output_dir, f"{video_name}_subtitles.srt")
    output_audio = os.path.join(video_output_dir, f"{video_name}_audio.wav")  # Changed to .wav
    output_video_no_audio = os.path.join(video_output_dir, f"{video_name}_no_audio.mp4")

    # Detach subtitles if flag is set
    if detach_subtitles_flag:
        detach_subtitles(video_path, output_subtitles)

    # Detach audio if flag is set
    if detach_audio_flag:
        detach_audio(video_path, output_audio, output_video_no_audio)

    # Handle transcription if audio exists
    if os.path.exists(output_audio):
        print(f"Audio file found: {output_audio}")
        audio_paths = [output_audio]
        asyncio.run(transcribe_audio(audio_paths, video_output_dir, stt_zh_flag, device))
    else:
        print(f"Audio file {output_audio} not found. Skipping transcription.")


def main():
    parser = argparse.ArgumentParser(description="Process videos by detaching subtitles, detaching audio, and performing speech-to-text conversion.")
    
    parser.add_argument('--input-dir', required=True, help='Path to the directory containing the original videos to be processed.')
    
    parser.add_argument('--output-dir', help='Path to the directory where processed videos and files will be saved. If not provided, the parent directory of the input directory will be used.')
    
    parser.add_argument('--detach-subtitles', action='store_true', help='Flag to detach subtitles from the videos. If set, subtitles will be extracted and saved as .srt files.')
    
    parser.add_argument('--detach-audio', action='store_true', help='Flag to detach audio from the videos. If set, audio will be extracted and saved as .wav files, and the video without audio will be saved as well.')
    
    parser.add_argument('--device', default='cpu', help='Flag to specify the device this workload will be conducted on. The device is used for speeding up the process. Options are "cpu" for using the CPU and "gpu" for using the GPU (if CUDA is available).')
    
    parser.add_argument('--speech-to-text-zh', action='store_true', help='Flag to perform speech-to-text conversion in Chinese. If not set, the default language for transcription will be English.')

    args = parser.parse_args()

    # If output directory is not provided, use the parent directory of input directory
    if not args.output_dir:
        args.output_dir = os.path.dirname(os.path.abspath(args.input_dir))
    
    # Validate and set the device
    if args.device == "cuda":
        print("Please set device to -------> gpu <-------- in order to use CUDA.")
    device = validate_device(args.device)

    start_time = time.time()
    print(f"Execution started at {time.ctime(start_time)}")

    # Process each video in the input directory
    for video_file in os.listdir(args.input_dir):
        video_path = os.path.join(args.input_dir, video_file)

        if video_file.lower().endswith(('.mp4', '.avi', '.mov', '.mkv')):  # Handle multiple video formats
            print(f"Processing video: {video_path}")
            
            process_video(video_path, args.output_dir, args.detach_subtitles, args.detach_audio, 
                          args.speech_to_text_zh, device)

    end_time = time.time()
    print(f"Execution finished at {time.ctime(end_time)}")
    print(f"Total time taken: {end_time - start_time:.2f} seconds")

if __name__ == '__main__':
    main()