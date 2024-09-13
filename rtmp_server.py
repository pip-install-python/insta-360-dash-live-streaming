import asyncio
import os
import logging
from pyrtmp import StreamClosedException
from pyrtmp.flv import FLVFileWriter, FLVMediaType
from pyrtmp.session_manager import SessionManager
from pyrtmp.rtmp import SimpleRTMPController, RTMPProtocol, SimpleRTMPServer

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class RTMPController(SimpleRTMPController):
    def __init__(self):
        super().__init__()
        self.stream_path = 'live_stream.flv'

    async def on_ns_publish(self, session, message) -> None:
        session.state = FLVFileWriter(output=self.stream_path)
        await super().on_ns_publish(session, message)

    async def on_metadata(self, session, message) -> None:
        session.state.write(0, message.to_raw_meta(), FLVMediaType.OBJECT)
        await super().on_metadata(session, message)

    async def on_video_message(self, session, message) -> None:
        session.state.write(message.timestamp, message.payload, FLVMediaType.VIDEO)
        await super().on_video_message(session, message)

    async def on_audio_message(self, session, message) -> None:
        session.state.write(message.timestamp, message.payload, FLVMediaType.AUDIO)
        await super().on_audio_message(session, message)

    async def on_stream_closed(self, session: SessionManager, exception: StreamClosedException) -> None:
        session.state.close()
        await super().on_stream_closed(session, exception)

    async def on_command_message(self, session, message) -> None:
        if message.command_name in ['releaseStream', 'FCPublish', 'FCUnpublish']:
            logger.info(f"Received command: {message.command_name}")
        else:
            await super().on_command_message(session, message)


class SimpleServer(SimpleRTMPServer):
    async def create(self, host: str, port: int):
        loop = asyncio.get_event_loop()
        self.server = await loop.create_server(
            lambda: RTMPProtocol(controller=RTMPController()),
            host=host,
            port=port,
        )


async def main():
    server = SimpleServer()
    await server.create(host='0.0.0.0', port=1935)
    await server.start()
    await server.wait_closed()

if __name__ == "__main__":
    asyncio.run(main())