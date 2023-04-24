#!/usr/bin/env python3
import argparse
import asyncio
from typing import Dict, Optional

from aioquic.asyncio import QuicConnectionProtocol, serve
from aioquic.h3.connection import H3_ALPN, H3Connection
from aioquic.h3.events import H3Event, HeadersReceived, WebTransportStreamDataReceived
from aioquic.quic.configuration import QuicConfiguration
from aioquic.quic.events import ProtocolNegotiated, StreamReset, QuicEvent

BIND_ADDRESS = '::1'
BIND_PORT = 4433


class PingPongHandler:

    def __init__(self, session_id, http: H3Connection) -> None:
        self._session_id = session_id
        self._http = http

    def h3_event_received(self, event: H3Event) -> None:
        if isinstance(event, WebTransportStreamDataReceived):
            if event.data:
                print(event.data)
            if event.stream_ended:
                payload = str('pong').encode('ascii')  # message to client
                self._http._quic.send_stream_data(event.stream_id, payload, end_stream=True)
                self.stream_closed(event.stream_id)

    def stream_closed(self, stream_id: int) -> None:
        print(f'Connection closed: {stream_id}')
        pass


class WebTransportProtocol(QuicConnectionProtocol):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._http: Optional[H3Connection] = None
        self._handler: Optional[PingPongHandler] = None

    def quic_event_received(self, event: QuicEvent) -> None:
        if isinstance(event, ProtocolNegotiated):
            self._http = H3Connection(self._quic, enable_webtransport=True)
        elif isinstance(event, StreamReset) and self._handler is not None:
            self._handler.stream_closed(event.stream_id)

        if self._http is not None:
            for h3_event in self._http.handle_event(event):
                self._h3_event_received(h3_event)

    def _h3_event_received(self, event: H3Event) -> None:
        if isinstance(event, HeadersReceived):
            headers = {}
            for header, value in event.headers:
                headers[header] = value
            if headers.get(b":method") == b"CONNECT" and headers.get(b":protocol") == b"webtransport":
                self._handshake_webtransport(event.stream_id, headers)
            else:
                self._send_response(event.stream_id, 400, end_stream=True)
        if self._handler:
            self._handler.h3_event_received(event)

    def _handshake_webtransport(self, stream_id: int, request_headers: Dict[bytes, bytes]) -> None:
        authority = request_headers.get(b":authority")
        path = request_headers.get(b":path")
        if authority is None or path is None:
            self._send_response(stream_id, 400, end_stream=True)
            return
        if path == b"/wt":
            assert(self._handler is None)
            self._handler = PingPongHandler(stream_id, self._http)
            self._send_response(stream_id, 200)
        else:
            self._send_response(stream_id, 404, end_stream=True)

    def _send_response(self, stream_id: int, status_code: int, end_stream=False) -> None:
        headers = [(b":status", str(status_code).encode())]
        if status_code == 200:
            headers.append((b"sec-webtransport-http3-draft", b"draft02"))
        self._http.send_headers(stream_id=stream_id, headers=headers, end_stream=end_stream)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('certificate')
    parser.add_argument('key')
    args = parser.parse_args()

    configuration = QuicConfiguration(alpn_protocols=H3_ALPN, is_client=False, max_datagram_frame_size=65536)
    configuration.load_cert_chain(args.certificate, args.key)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(
        serve(BIND_ADDRESS, BIND_PORT, configuration=configuration, create_protocol=WebTransportProtocol))
    try:
        print("Listening on https https://localhost:4433/wt")
        loop.run_forever()
    except KeyboardInterrupt:
        pass
