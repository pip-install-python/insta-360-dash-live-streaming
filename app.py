import dash
from dash import html, dcc
import dash_pannellum
from dash.dependencies import Input, Output
import os
from flask import send_from_directory

app = dash.Dash(__name__, suppress_callback_exceptions=True)


# Add a route to serve video files
@app.server.route('/video/<path:path>')
def serve_video(path):
    return send_from_directory('assets', path)


video_config = {
    "sources": [
        {"src": "/video/converted_stream.mp4", "type": "video/mp4"},
    ],
}

app.layout = html.Div([
    html.Link(
        rel='stylesheet',
        href='https://cdnjs.cloudflare.com/ajax/libs/video.js/7.20.3/video-js.min.css'
    ),
    html.Script(src='https://cdnjs.cloudflare.com/ajax/libs/video.js/7.20.3/video.min.js'),
    html.Script(src='https://cdn.jsdelivr.net/npm/pannellum@2.5.6/build/pannellum.js'),
    html.Link(
        rel='stylesheet',
        href='https://cdn.jsdelivr.net/npm/pannellum@2.5.6/build/pannellum.css'
    ),
    dash_pannellum.DashPannellum(
        id='panorama',
        video=video_config,
        autoLoad=True,
        width='100%',
        height='400px',
    ),
    dcc.Interval(
        id='interval-component',
        interval=30000,  # 30 seconds
        n_intervals=0
    )
])


@app.callback(Output('panorama', 'video'),
              Input('interval-component', 'n_intervals'))
def update_video_src(n):
    return {
        "sources": [
            {"src": f"/video/converted_stream.mp4?v={n}", "type": "video/mp4"},
        ],
    }


if __name__ == '__main__':
    app.run_server(debug=True)