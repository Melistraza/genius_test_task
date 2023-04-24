from unittest import TestCase, mock, main

from web_transport import WebTransportProtocol
from unittest.mock import MagicMock


# WebTransportProtocol().quic_event_received()
# WebTransportProtocol()._h3_event_received()
# WebTransportProtocol()._handshake_webtransport()
# WebTransportProtocol()._send_response()


class WebTransportProtocolTestCase(TestCase):

    def test_send_response(self):
        web_protocol = WebTransportProtocol(quic=MagicMock())
        web_protocol._http = MagicMock()
        web_protocol._send_response(1, 200, end_stream=False)
        web_protocol._http.send_headers.assert_called_once_with(
            stream_id=1,
            headers=[(b':status', b'200'), (b'sec-webtransport-http3-draft', b'draft02')],
            end_stream=False
        )

    def test_handshake_webtransport(self):
        web_protocol = WebTransportProtocol(quic=MagicMock())
        web_protocol._http = MagicMock()
        headers = {
            b":authority": None,
            b":path": None
        }
        web_protocol._handshake_webtransport(1, headers)
        web_protocol._http.send_headers.assert_called_once_with(
            stream_id=1,
            headers=[(b':status', b'400')],
            end_stream=True
        )

if __name__ == '__main__':
    main()
