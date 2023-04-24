Main dealbreaker is not only create app that use WebTransport
we also need server that will host our app and will work with HTTP/3 and WebTransport

# Python

## Disclaimer
This is insane task. Because technology is not ready for production use.
Because browser just start support it.
https://caniuse.com/webtransport

Chrome start support it 22Jan2022 and only 22% of users update to this version.

### Python package for python http3 client (No WebTransport support)
https://pypi.org/project/http3/

### Package for testing WebTransport
web-platform-test
https://web-platform-tests.org/tools/webtransport/README.html

### Security
We could send data via datagram or if we want more secure way use stream.
Datagrams are ideal for sending and receiving data that does not require strong delivery guarantees.

Useful link
https://pgjones.dev/blog/http-1-2-3-2019/