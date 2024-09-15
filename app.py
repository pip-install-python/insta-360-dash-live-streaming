# import dash
# from dash import html, dcc
# import dash_pannellum
# from dash.dependencies import Input, Output
# import os
# from flask import send_from_directory
# import time
#
# app = dash.Dash(__name__, suppress_callback_exceptions=True)
#
# # Add a route to serve video files
# @app.server.route('/video/<path:path>')
# def serve_video(path):
#     return send_from_directory('assets', path, conditional=True)
#
# video_config = {
#     "sources": [
#         {"src": "/video/converted_stream.mp4", "type": "video/mp4"},
#     ],
# }
#
# app.layout = html.Div([
#     html.Link(
#         rel='stylesheet',
#         href='https://cdnjs.cloudflare.com/ajax/libs/video.js/7.20.3/video-js.min.css'
#     ),
#     html.Script(src='https://cdnjs.cloudflare.com/ajax/libs/video.js/7.20.3/video.min.js'),
#     html.Script(src='https://cdn.jsdelivr.net/npm/pannellum@2.5.6/build/pannellum.js'),
#     html.Link(
#         rel='stylesheet',
#         href='https://cdn.jsdelivr.net/npm/pannellum@2.5.6/build/pannellum.css'
#     ),
#     dash_pannellum.DashPannellum(
#         id='panorama',
#         video=video_config,
#         autoLoad=True,
#         width='100%',
#         height='400px',
#     ),
#     dcc.Interval(
#         id='interval-component',
#         interval=5000,  # 5 seconds
#         n_intervals=0
#     )
# ])
#
# @app.callback(Output('panorama', 'video'),
#               Input('interval-component', 'n_intervals'))
# def update_video_src(n):
#     timestamp = int(time.time())
#     return {
#         "sources": [
#             {"src": f"/video/converted_stream.mp4?v={timestamp}", "type": "video/mp4"},
#         ],
#     }
#
# if __name__ == '__main__':
#     app.run_server(debug=True)

# import dash
# from dash import html, dcc
# import dash_pannellum
# from dash.dependencies import Input, Output
# from flask import send_from_directory
# import os
#
# app = dash.Dash(__name__, suppress_callback_exceptions=True)
#
# # Add a route to serve HLS files
# @app.server.route('/hls/<path:path>')
# def serve_hls(path):
#     return send_from_directory('assets/hls', path)
#
# video_config = {
#     "sources": [
#         {"src": "/hls/stream.m3u8", "type": "application/x-mpegURL"},
#     ],
#     "techOrder": ["html5", "flash"],
#     "plugins": {
#         "httpSourceSelector": {
#             "default": "auto"
#         }
#     },
#     "controlBar": {
#         "children": [
#             "playToggle",
#             "volumePanel",
#             "progressControl",
#             "qualitySelector",
#             "fullscreenToggle"
#         ]
#     }
# }
#
# app.layout = html.Div([
#     html.Link(
#         rel='stylesheet',
#         href='https://vjs.zencdn.net/7.20.3/video-js.min.css'
#     ),
#     html.Script(src='https://vjs.zencdn.net/7.20.3/video.min.js'),
#     html.Script(src='https://unpkg.com/@videojs/http-streaming@2.14.2/dist/videojs-http-streaming.min.js'),
#     html.Script(src='https://cdn.jsdelivr.net/npm/pannellum@2.5.6/build/pannellum.js'),
#     html.Link(
#         rel='stylesheet',
#         href='https://cdn.jsdelivr.net/npm/pannellum@2.5.6/build/pannellum.css'
#     ),
#     dash_pannellum.DashPannellum(
#         id='panorama',
#         video=video_config,
#         autoLoad=True,
#         width='100%',
#         height='400px',
#     )
# ])
#
# if __name__ == '__main__':
#     app.run_server(debug=True)
import dash
from dash import html, dcc, Input, Output, State, ClientsideFunction
import dash_pannellum
from flask import send_from_directory
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = dash.Dash(__name__, suppress_callback_exceptions=True)

@app.server.route('/hls/<path:path>')
def serve_hls(path):
    logger.debug(f"Serving HLS file: {path}")
    return send_from_directory('assets/hls', path)

video_config = {
    "sources": [
        {"src": "/hls/stream.m3u8", "type": "application/x-mpegURL"},
    ],
}

app.layout = html.Div([
    html.Div(id='last-update-time', style={'display': 'none'}),
    dash_pannellum.DashPannellum(
        id='panorama',
        video=video_config,
        width='100%',
        height='400px',
        showCenterDot=True,
        compass=True,
        northOffset=0,
        useHttpStreaming=True,
        autoLoad=True
    ),
    dcc.Interval(
        id='interval-component',
        interval=10000,  # 10 seconds
        n_intervals=0
    )
])

app.clientside_callback(
    ClientsideFunction(
        namespace='clientside',
        function_name='updateVideoSource'
    ),
    Output('last-update-time', 'children'),
    Input('interval-component', 'n_intervals')
)

@app.callback(
    Output('panorama', 'video'),
    Input('last-update-time', 'children'),
    State('panorama', 'video')
)
def update_video_config(last_update_time, current_video):
    logger.debug(f"Updating video config at {last_update_time}")
    if current_video and current_video['sources'][0]['src'].startswith('/hls/stream.m3u8'):
        new_src = f"/hls/stream.m3u8?_={last_update_time}"
        current_video['sources'][0]['src'] = new_src
        return current_video
    else:
        return video_config

if __name__ == '__main__':
    logger.info("Starting Dash server")
    app.run_server(debug=True)