let currentTransport;

// "Connect" button handler.
async function connect() {
  const url = 'https://localhost:4433/wt';
  var transport = new WebTransport(url);
  try {
    await transport.ready;
  } catch (e) {
    addToEventLog('Connection failed. ' + e, 'error');
    return;
  }
  transport.closed
  currentTransport = transport;
  document.forms.sending.elements.send.disabled = false;
  document.getElementById('connect').disabled = true;
}

// "Send ping" button handler.
async function sendData() {
  let encoder = new TextEncoder('utf-8');
  let rawData = 'ping'; // data that we send to our server
  let data = encoder.encode(rawData);
  let transport = currentTransport;
  let stream = await transport.createBidirectionalStream();
  readFromIncomingStream(stream);

  let writer = stream.writable.getWriter();
  await writer.write(data);
  await writer.close();
}

async function readFromIncomingStream(stream) {
  addToEventLog(await new Response(stream.readable).text());
}

function addToEventLog(text, severity = 'info') {
  let log = document.getElementById('event-log');
  let entry = document.createElement('li');
  entry.innerText = text;
  log.appendChild(entry);
}