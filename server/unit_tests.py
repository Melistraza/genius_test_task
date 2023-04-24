from unittest import TestCase, mock, main

from web_transport import WebTransportProtocol
from unittest.mock import MagicMock


# WebTransportProtocol().quic_event_received()
# WebTransportProtocol()._h3_event_received()
# WebTransportProtocol()._handshake_webtransport()
# WebTransportProtocol()._send_response()


class WebTransportProtocolTestCase(TestCase):

    def setUp(self) -> None:
        self.web_protocol = WebTransportProtocol(quic=MagicMock())
        self.web_protocol._http = MagicMock()

    def test_send_response_200(self):
        self.web_protocol._send_response(1, 200, end_stream=False)
        self.web_protocol._http.send_headers.assert_called_once_with(
            stream_id=1,
            headers=[(b':status', b'200'), (b'sec-webtransport-http3-draft', b'draft02')],
            end_stream=False
        )

    def test_send_response_400(self):
        self.web_protocol._send_response(1, 400, end_stream=True)
        self.web_protocol._http.send_headers.assert_called_once_with(
            stream_id=1,
            headers=[(b':status', b'400')],
            end_stream=True
        )

    def test_handshake_webtransport(self):
        headers = {
            b":authority": None,
            b":path": None
        }
        self.web_protocol._handshake_webtransport(1, headers)
        self.web_protocol._http.send_headers.assert_called_once_with(
            stream_id=1,
            headers=[(b':status', b'400')],
            end_stream=True
        )

    def test_handshake_webtransport_wt(self):
        headers = {
            b":authority": 'dummy',
            b":path": b"/wt"
        }
        self.web_protocol._handshake_webtransport(1, headers)
        self.web_protocol._http.send_headers.assert_called_once_with(
            stream_id=1,
            headers=[(b':status', b'200'), (b'sec-webtransport-http3-draft', b'draft02')],
            end_stream=False
        )

    def test_handshake_webtransport_non_exist_url(self):
        headers = {
            b":authority": 'dummy',
            b":path": b"/dummy"
        }
        self.web_protocol._handshake_webtransport(1, headers)
        self.web_protocol._http.send_headers.assert_called_once_with(
            stream_id=1,
            headers=[(b':status', b'404')],
            end_stream=True
        )

if __name__ == '__main__':
    main()
