# import subprocess
# import time
# import os
# import sys
# import signal
#
#
# def check_ffmpeg_installed():
#     try:
#         subprocess.run(['ffmpeg', '-version'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
#         return True
#     except (subprocess.CalledProcessError, FileNotFoundError):
#         return False
#
#
# def convert_flv_to_mp4():
#     input_file = 'live_stream.flv'
#     output_file = os.path.join('assets', 'converted_stream.mp4')
#     temp_output_file = os.path.join('assets', 'temp_converted_stream.mp4')
#
#     if not check_ffmpeg_installed():
#         print("Error: FFmpeg is not installed or not in your system PATH.")
#         print("Please install FFmpeg and make sure it's accessible from the command line.")
#         print("Installation instructions:")
#         print("- On macOS: Use Homebrew with 'brew install ffmpeg'")
#         print("- On Windows: Download from https://ffmpeg.org/download.html and add to PATH")
#         print("- On Linux: Use your distribution's package manager, e.g., 'sudo apt-get install ffmpeg'")
#         sys.exit(1)
#
#     ffmpeg_command = [
#         'ffmpeg',
#         '-i', input_file,
#         '-c:v', 'libx264',
#         '-preset', 'ultrafast',
#         '-tune', 'zerolatency',
#         '-crf', '23',
#         '-c:a', 'aac',
#         '-b:a', '128k',
#         '-ar', '44100',
#         '-f', 'mp4',
#         '-movflags', 'frag_keyframe+empty_moov+faststart+separate_moof+omit_tfhd_offset+default_base_moof',
#         '-frag_duration', '1000000',
#         temp_output_file
#     ]
#
#     process = None
#
#     def signal_handler(signum, frame):
#         if process:
#             process.terminate()
#         sys.exit(0)
#
#     signal.signal(signal.SIGINT, signal_handler)
#     signal.signal(signal.SIGTERM, signal_handler)
#
#     while True:
#         try:
#             if os.path.exists(input_file):
#                 process = subprocess.Popen(ffmpeg_command)
#                 process.wait()
#
#                 # Rotate the files
#                 if os.path.exists(output_file):
#                     os.remove(output_file)
#                 os.rename(temp_output_file, output_file)
#             else:
#                 time.sleep(1)  # Wait for 1 second before checking again
#         except subprocess.CalledProcessError as e:
#             print(f"Error running FFmpeg: {e}")
#             time.sleep(5)  # Wait for 5 seconds before retrying
#         except KeyboardInterrupt:
#             print("Conversion stopped by user.")
#             break
#
#
# if __name__ == "__main__":
#     convert_flv_to_mp4()
#Most Recent working File: live_stream.py
# import subprocess
# import time
# import os
# import sys
# import signal
# 
# def check_ffmpeg_installed():
#     try:
#         subprocess.run(['ffmpeg', '-version'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
#         return True
#     except (subprocess.CalledProcessError, FileNotFoundError):
#         return False
# 
# def convert_flv_to_hls():
#     input_file = 'live_stream.flv'
#     output_dir = os.path.join('assets', 'hls')
#     output_path = os.path.join(output_dir, 'stream.m3u8')
# 
#     if not os.path.exists(output_dir):
#         os.makedirs(output_dir)
# 
#     if not check_ffmpeg_installed():
#         print("Error: FFmpeg is not installed or not in your system PATH.")
#         print("Please install FFmpeg and make sure it's accessible from the command line.")
#         print("Installation instructions:")
#         print("- On macOS: Use Homebrew with 'brew install ffmpeg'")
#         print("- On Windows: Download from https://ffmpeg.org/download.html and add to PATH")
#         print("- On Linux: Use your distribution's package manager, e.g., 'sudo apt-get install ffmpeg'")
#         sys.exit(1)
# 
#     ffmpeg_command = [
#         'ffmpeg',
#         '-i', input_file,
#         '-c:v', 'libx264',
#         '-preset', 'veryfast',  # Changed from 'ultrafast' for better quality/performance balance
#         '-tune', 'zerolatency',
#         '-c:a', 'aac',
#         '-b:a', '128k',
#         '-ar', '44100',
#         '-f', 'hls',
#         '-hls_time', '2',  # Changed from 5 to 2 for lower latency
#         '-hls_list_size', '10',  # Added to limit the playlist size
#         '-hls_flags', 'delete_segments+omit_endlist',  # Added to remove old segments and keep the stream live
#         '-hls_segment_filename', os.path.join(output_dir, 'segment%03d.ts'),
#         output_path
#     ]
# 
#     process = None
# 
#     def signal_handler(signum, frame):
#         if process:
#             process.terminate()
#         sys.exit(0)
# 
#     signal.signal(signal.SIGINT, signal_handler)
#     signal.signal(signal.SIGTERM, signal_handler)
# 
#     while True:
#         try:
#             if os.path.exists(input_file):
#                 process = subprocess.Popen(ffmpeg_command)
#                 process.wait()
#             else:
#                 time.sleep(1)  # Wait for 1 second before checking again
#         except subprocess.CalledProcessError as e:
#             print(f"Error running FFmpeg: {e}")
#             time.sleep(5)  # Wait for 5 seconds before retrying
#         except KeyboardInterrupt:
#             print("Conversion stopped by user.")
#             break
# 
# if __name__ == "__main__":
#     convert_flv_to_hls()
import subprocess
import time
import os
import sys
import signal
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def check_ffmpeg_installed():
    try:
        subprocess.run(['ffmpeg', '-version'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def convert_flv_to_hls():
    input_file = 'live_stream.flv'
    output_dir = os.path.join('assets', 'hls')
    output_path = os.path.join(output_dir, 'stream.m3u8')

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    if not check_ffmpeg_installed():
        logger.error("FFmpeg is not installed or not in your system PATH.")
        sys.exit(1)

    ffmpeg_command = [
        'ffmpeg',
        '-re',  # Read input at native frame rate
        '-i', input_file,
        '-c:v', 'libx264',
        '-preset', 'veryfast',
        '-tune', 'zerolatency',
        '-c:a', 'aac',
        '-b:a', '128k',
        '-ar', '44100',
        '-f', 'hls',
        '-hls_time', '2',
        '-hls_list_size', '10',
        '-hls_flags', 'delete_segments+omit_endlist+append_list',
        '-hls_segment_filename', os.path.join(output_dir, 'segment%d.ts'),
        '-hls_start_number_source', 'epoch',
        '-live_start_index', '-3',
        output_path
    ]

    process = None

    def signal_handler(signum, frame):
        if process:
            process.terminate()
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    while True:
        try:
            if os.path.exists(input_file):
                logger.info("Starting FFmpeg conversion")
                process = subprocess.Popen(ffmpeg_command)
                process.wait()
            else:
                logger.warning(f"Input file {input_file} not found. Waiting...")
                time.sleep(5)
        except subprocess.CalledProcessError as e:
            logger.error(f"Error running FFmpeg: {e}")
            time.sleep(5)
        except KeyboardInterrupt:
            logger.info("Conversion stopped by user.")
            break

if __name__ == "__main__":
    convert_flv_to_hls()