import dash
from dash import html

app = dash.Dash(__name__)

app.layout = html.Div([
    # Include the Video.js CSS
    html.Link(
        rel='stylesheet',
        href='https://vjs.zencdn.net/8.16.1/video-js.css'
    ),

    # Video.js player with autoplay enabled
    html.Video(
        id='my-video',
        className='video-js vjs-default-skin',
        controls=True,
        autoPlay=True,  # Enable autoplay
        preload='auto',
        width='640',
        height='264',
        poster='/assets/MY_VIDEO_POSTER.jpg',
        **{'data-setup': '{"autoplay": true}'},  # Pass autoplay option to Video.js
        children=[
            html.Source(src='/assets/converted_stream.mp4', type='video/mp4'),
            # html.Source(src='/assets/MY_VIDEO.webm', type='video/webm'),
            html.P(
                "To view this video please enable JavaScript, and consider upgrading to a "
                "web browser that supports HTML5 video."
            )
        ]
    ),

    # Include the Video.js JavaScript
    html.Script(src='https://vjs.zencdn.net/8.16.1/video.min.js')
])

if __name__ == '__main__':
    app.run_server(debug=True, port='9111')

