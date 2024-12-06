import logging
import subprocess
import os
from paddlespeech.cli.asr.infer import ASRExecutor

# Initialize logger
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Maximum duration per chunk in seconds
MAX_DURATION = 50.0  # 3 minutes

# Function to get the duration of an audio file in seconds using ffprobe
# Function to get the duration of an audio file in seconds using ffprobe
def get_audio_duration(audio_file: str) -> float:
    try:
        result = subprocess.run(
            [
                "ffprobe",
                "-v", "error",
                "-show_entries", "format=duration",
                "-of", "default=noprint_wrappers=1:nokey=1",
                audio_file,
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True
        )
        duration_str = result.stdout.decode().strip()
        duration = float(duration_str)
        logger.debug(f"Duration of '{audio_file}': {duration} seconds")
        return duration
    except subprocess.CalledProcessError as e:
        logger.error(f"FFprobe error for file '{audio_file}': {e.stderr.decode().strip()}")
    except ValueError:
        logger.error(f"Could not convert FFprobe output to float for file '{audio_file}'")
    return 0.0

# Function to convert audio to the desired format
def convert_audio_format(input_file: str, output_file: str):
    try:
        ffmpeg_command = [
            "ffmpeg",
            "-y",  # Overwrite output files without asking
            "-i", input_file,
            "-ac", "1",
            "-ar", "16000",
            "-acodec", "pcm_s16le",
            output_file
        ]
        logging.info(f"Converting audio format with command: {' '.join(ffmpeg_command)}")
        subprocess.run(
            ffmpeg_command,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        logger.debug(f"Converted '{input_file}' to '{output_file}'")
    except subprocess.CalledProcessError as e:
        error_msg = e.stderr.decode().strip()
        logger.error(f"FFmpeg error while converting '{input_file}': {error_msg}")
        raise

# Function to split and convert audio based on the maximum duration
def split_and_convert_audio(audio_file: str, max_duration: float = MAX_DURATION) -> list:
    total_duration = get_audio_duration(audio_file)
    
    if total_duration == 0.0:
        logger.error(f"Skipping file '{audio_file}' due to invalid duration.")
        return []
    
    if total_duration > max_duration:
        num_chunks = int(total_duration // max_duration) + (1 if total_duration % max_duration > 0 else 0)
        chunk_files = []
        logger.debug(f"Splitting '{audio_file}' into {num_chunks} chunk(s) of {max_duration} seconds each.")
        for i in range(num_chunks):
            start_time = i * max_duration
            chunk_file = f"{audio_file}_part_{i+1}.wav"  # Start counting from 1
            ffmpeg_command = [
                "ffmpeg",
                "-y",  # Overwrite output files without asking
                "-i", audio_file,
                "-ss", str(start_time),
                "-t", str(max_duration),
                "-ac", "1",
                "-ar", "16000",
                "-acodec", "pcm_s16le",
                chunk_file
            ]
            try:
                logging.info(f"Splitting audio with command: {' '.join(ffmpeg_command)}")
                subprocess.run(
                    ffmpeg_command,
                    check=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE
                )
                # Verify the duration of the created chunk
                chunk_duration = get_audio_duration(chunk_file)
                logger.debug(f"Created chunk '{chunk_file}' starting at {start_time} seconds with duration {chunk_duration} seconds")
                if chunk_duration > max_duration:
                    logger.warning(f"Chunk '{chunk_file}' exceeds the maximum duration of {max_duration} seconds.")
                chunk_files.append(chunk_file)
            except subprocess.CalledProcessError as e:
                error_msg = e.stderr.decode().strip()
                logger.error(f"FFmpeg error while splitting '{audio_file}': {error_msg}")
        return chunk_files
    else:
        # Convert the original file to the desired format
        converted_file = f"{audio_file}_converted.wav"
        try:
            convert_audio_format(audio_file, converted_file)
            # Verify the duration of the converted file
            converted_duration = get_audio_duration(converted_file)
            logger.debug(f"Converted file '{converted_file}' has duration {converted_duration} seconds")
            return [converted_file]
        except Exception as e:
            logger.error(f"Failed to convert '{audio_file}': {e}")
            return []

# Function to process each audio chunk with ASR and return transcribed text
def asr_to_zh(audio_path: str, lang: str, device: str = "cpu") -> str:
    # Split and convert audio
    audio_chunks = split_and_convert_audio(audio_path)
    
    if not audio_chunks:
        logger.warning(f"No valid audio chunks to process for file '{audio_path}'")
        return ""
    
    full_text = ""
    
    # Initialize ASRExecutor once
    try:
        asr_executor = ASRExecutor()
        logger.debug("Initialized ASRExecutor successfully.")
    except Exception as e:
        logger.error(f"Failed to initialize ASRExecutor: {e}")
        return ""
    
    for audio_chunk in audio_chunks:
        try:
            # Verify chunk duration before processing
            chunk_duration = get_audio_duration(audio_chunk)
            logger.debug(f"Processing chunk '{audio_chunk}' with duration {chunk_duration} seconds")
            if chunk_duration > MAX_DURATION:
                logger.error(f"Chunk '{audio_chunk}' exceeds the maximum allowed duration of {MAX_DURATION} seconds. Skipping.")
                continue
            if chunk_duration <= 0:
                logger.error(f"Chunk '{audio_chunk}' has invalid duration. Skipping.")
                continue
            
            # Additional Verification: Check if the chunk is properly formatted
            # For example, ensure it's a PCM WAV file
            try:
                subprocess.run(
                    [
                        "ffprobe",
                        "-v", "error",
                        "-select_streams", "a:0",
                        "-show_entries", "stream=codec_name,channels,sample_rate",
                        "-of", "default=noprint_wrappers=1",
                        audio_chunk
                    ],
                    check=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE
                )
                logger.debug(f"Verified audio format for '{audio_chunk}'")
            except subprocess.CalledProcessError as e:
                logger.error(f"Audio format verification failed for '{audio_chunk}': {e.stderr.decode().strip()}")
                continue  # Skip this chunk
            
            # Process each chunk with ASR
            logger.debug(f"Starting ASR processing for chunk '{audio_chunk}'")
            result = asr_executor(audio_file=audio_chunk, lang=lang, device=device, sample_rate=16000, model="conformer_wenetspeech")
            logger.debug(f"ASR result for chunk '{audio_chunk}': {result.strip()}")
            full_text += result.strip() + " "
        except Exception as e:
            logger.error(f"Error processing chunk '{audio_chunk}': {e}")
        finally:
            # Clean up chunk after processing
            try:
                os.remove(audio_chunk)
                logger.debug(f"Removed temporary file '{audio_chunk}'")
            except OSError as e:
                logger.warning(f"Failed to remove temporary file '{audio_chunk}': {e}")
    
    return full_text.strip()