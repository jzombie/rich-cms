# Free P2P Services

There are several free hosted services that can facilitate peer-to-peer object exchange between browsers. These services typically provide a signaling server for WebRTC, which is necessary for establishing the initial connection between peers. Here are a few options:

## 1. **PeerJS Cloud Server**
PeerJS provides a free cloud-hosted server for signaling, making it easy to set up peer-to-peer connections.

- **Website:** [PeerJS](https://peerjs.com/)
- **How to Use:** PeerJS offers a free, hosted signaling server. You can use it by simply creating a new `Peer` object without any additional configuration.
- **Example:**

  ```javascript
  // Include PeerJS library
  const peer = new Peer(); // Uses the default free PeerJS server

  // Generate a unique ID for the peer
  peer.on('open', (id) => {
    console.log('My peer ID is: ' + id);
  });

  // Connect to another peer
  const conn = peer.connect('another-peer-id');

  // Send a message
  conn.on('open', () => {
    conn.send('Hello!');
  });

  // Receive a message
  peer.on('connection', (conn) => {
    conn.on('data', (data) => {
      console.log('Received', data);
    });
  });
  ```

## 2. **SkyWay**
SkyWay is a P2P WebRTC platform that offers a free tier for basic usage. It supports both data channels and media streams.

- **Website:** [SkyWay](https://webrtc.ecl.ntt.com/)
- **How to Use:** SkyWay provides an API for peer-to-peer connections. You need to sign up to get an API key.
- **Example:**

  ```javascript
  const peer = new Peer({
    key: 'your-api-key',
    debug: 3
  });

  peer.on('open', id => {
    console.log('My peer ID is: ' + id);
  });

  const conn = peer.connect('another-peer-id');

  conn.on('open', () => {
    conn.send('Hello!');
  });

  peer.on('connection', conn => {
    conn.on('data', data => {
      console.log('Received', data);
    });
  });
  ```

## 3. **Socket.io + WebRTC**
Socket.io can be used as a signaling server for WebRTC. While Socket.io itself isn't specifically a WebRTC signaling service, it's a powerful tool that can facilitate the necessary signaling process for establishing WebRTC connections.

- **Website:** [Socket.io](https://socket.io/)
- **How to Use:** You can use a free tier from any cloud provider that supports Socket.io (e.g., Heroku, Vercel) to set up your signaling server.
- **Example:**

  **Server (Node.js with Socket.io):**
  ```javascript
  const express = require('express');
  const http = require('http');
  const socketIo = require('socket.io');

  const app = express();
  const server = http.createServer(app);
  const io = socketIo(server);

  io.on('connection', (socket) => {
    socket.on('signal', (data) => {
      io.to(data.peerId).emit('signal', data.signal);
    });
  });

  server.listen(3000, () => {
    console.log('Server is running on port 3000');
  });
  ```

  **Client (Browser with WebRTC and Socket.io):**
  ```html
  <script src="/socket.io/socket.io.js"></script>
  <script>
    const socket = io();

    // Create a new RTCPeerConnection
    const pc = new RTCPeerConnection();

    // Handle ICE candidates
    pc.onicecandidate = (event) => {
      if (event.candidate) {
        socket.emit('signal', { peerId: 'another-peer-id', signal: { candidate: event.candidate } });
      }
    };

    // Handle data channel events
    pc.ondatachannel = (event) => {
      const dataChannel = event.channel;
      dataChannel.onopen = () => {
        console.log('Data channel is open');
        dataChannel.send('Hello from peer1');
      };
      dataChannel.onmessage = (event) => {
        console.log('Received message:', event.data);
      };
    };

    // Create a data channel
    const dataChannel = pc.createDataChannel('chat');

    // Create an offer
    pc.createOffer().then(offer => {
      pc.setLocalDescription(offer);
      socket.emit('signal', { peerId: 'another-peer-id', signal: { sdp: offer } });
    });

    socket.on('signal', (data) => {
      if (data.signal.sdp) {
        pc.setRemoteDescription(new RTCSessionDescription(data.signal.sdp)).then(() => {
          if (pc.remoteDescription.type === 'offer') {
            pc.createAnswer().then(answer => {
              pc.setLocalDescription(answer);
              socket.emit('signal', { peerId: data.peerId, signal: { sdp: answer } });
            });
          }
        });
      } else if (data.signal.candidate) {
        pc.addIceCandidate(new RTCIceCandidate(data.signal.candidate));
      }
    });
  </script>
  ```

## 4. **P2P CDN Services (WebTorrent)**
WebTorrent is a streaming torrent client for the web. It uses WebRTC for peer-to-peer communication and can be used to share files between browsers.

- **Website:** [WebTorrent](https://webtorrent.io/)
- **How to Use:** WebTorrent provides a free library that you can use to share files between browsers using P2P.
- **Example:**

  ```html
  <script src="https://cdn.jsdelivr.net/npm/webtorrent/webtorrent.min.js"></script>
  <script>
    const client = new WebTorrent();

    // Create a new torrent
    client.seed(file, (torrent) => {
      console.log('Torrent info hash:', torrent.infoHash);
      console.log('Magnet URI:', torrent.magnetURI);
    });

    // Download a torrent
    client.add('magnet-uri', (torrent) => {
      torrent.files.forEach((file) => {
        file.getBlobURL((err, url) => {
          if (err) throw err;
          console.log('File URL:', url);
        });
      });
    });
  </script>
  ```

These services and libraries offer various ways to establish peer-to-peer connections between browsers, facilitating direct object exchange without the need for an intermediary server after the initial connection is established.
