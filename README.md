# Live Stream Insta 360 Panorama
_____
- Still in active development (NOT Fully Wroking or Polished, Exploratory at best)

### How to setup:
For macOS (which you seem to be using based on the error message):

1. Install Homebrew if you haven't already: /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
2. Then install FFmpeg: brew install ffmpeg


For Windows:

1. Download FFmpeg from https://ffmpeg.org/download.html
2. Extract the files and add the bin folder to your system PATH


For Linux:

1. Use your distribution's package manager, e.g., sudo apt-get install ffmpeg for Ubuntu/Debian

- Clone the repo
- create an assets folder in root
- Install the requirements
- run rtmp_server.py to start the rtmp server
- connect your phone to your insta 360 4x camera with usb c
- go to 360 recording option on the app, click on rtmp stream
- past the rtmp url and click on start streaming `rtmp://localhost:1935/live` or `rtmp://UR-IP-ADDRESS:1935/live`
- run the live_stream.py to turn the live_stream.flv into a assets/converted_stream.mp4 file
- run the app.py to view the live stream
  (re-run the live_stream.py to update the live stream)

### Goals
- [x] Connect the insta 360 camera to the hosted rtmp_server
- [x] Convert the live stream to a mp4 file
- [x] Create a Dash app to view the live stream
- [x] Add a 360 viewer to the Dash app
- [ ] combine the live_Stream.py and app.py files into one file
- [ ] Add a way to view the live stream with it continuously updating without need for manual update trigger
