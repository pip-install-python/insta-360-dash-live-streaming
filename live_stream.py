import subprocess
import time
import os
import sys

def check_ffmpeg_installed():
    try:
        subprocess.run(['ffmpeg', '-version'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        return True
    except subprocess.CalledProcessError:
        return False
    except FileNotFoundError:
        return False

def convert_flv_to_mp4():
    input_file = 'live_stream.flv'
    output_file = os.path.join('assets', 'converted_stream.mp4')

    if not check_ffmpeg_installed():
        print("Error: FFmpeg is not installed or not in your system PATH.")
        print("Please install FFmpeg and make sure it's accessible from the command line.")
        print("Installation instructions:")
        print("- On macOS: Use Homebrew with 'brew install ffmpeg'")
        print("- On Windows: Download from https://ffmpeg.org/download.html and add to PATH")
        print("- On Linux: Use your distribution's package manager, e.g., 'sudo apt-get install ffmpeg'")
        sys.exit(1)

    ffmpeg_command = [
        'ffmpeg',
        '-i', input_file,
        '-c:v', 'libx264',
        '-preset', 'ultrafast',
        '-tune', 'zerolatency',
        '-crf', '23',
        '-c:a', 'aac',
        '-b:a', '128k',
        '-ar', '44100',
        '-f', 'mp4',
        '-movflags', 'frag_keyframe+empty_moov+faststart+separate_moof+omit_tfhd_offset+default_base_moof',
        '-frag_duration', '1000000',
        output_file
    ]

    while True:
        try:
            if os.path.exists(input_file):
                process = subprocess.Popen(ffmpeg_command)
                process.wait()
            else:
                time.sleep(1)  # Wait for 1 second before checking again
        except subprocess.CalledProcessError as e:
            print(f"Error running FFmpeg: {e}")
            time.sleep(5)  # Wait for 5 seconds before retrying
        except KeyboardInterrupt:
            print("Conversion stopped by user.")
            break

if __name__ == "__main__":
    convert_flv_to_mp4()