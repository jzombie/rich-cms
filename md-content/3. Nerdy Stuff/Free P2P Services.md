# Free P2P Services

There are several free hosted services that can facilitate peer-to-peer object exchange between browsers. These services typically provide a signaling server for WebRTC, which is necessary for establishing the initial connection between peers. Here are a few options:

## 1. **PeerJS Cloud Server**
PeerJS provides a free cloud-hosted server for signaling, making it easy to set up peer-to-peer connections.

- **Website:** [PeerJS](https://peerjs.com/)
- **How to Use:** PeerJS offers a free, hosted signaling server. You can use it by simply creating a new `Peer` object without any additional configuration.

## 2. **SkyWay**
SkyWay is a P2P WebRTC platform that offers a free tier for basic usage. It supports both data channels and media streams.

- **Website:** [SkyWay](https://webrtc.ecl.ntt.com/)
- **How to Use:** SkyWay provides an API for peer-to-peer connections. You need to sign up to get an API key.

## 3. **Socket.io + WebRTC**
Socket.io can be used as a signaling server for WebRTC. While Socket.io itself isn't specifically a WebRTC signaling service, it's a powerful tool that can facilitate the necessary signaling process for establishing WebRTC connections.

- **Website:** [Socket.io](https://socket.io/)
- **How to Use:** You can use a free tier from any cloud provider that supports Socket.io (e.g., Heroku, Vercel) to set up your signaling server.

## 4. **P2P CDN Services (WebTorrent)**
WebTorrent is a streaming torrent client for the web. It uses WebRTC for peer-to-peer communication and can be used to share files between browsers.

- **Website:** [WebTorrent](https://webtorrent.io/)
- **How to Use:** WebTorrent provides a free library that you can use to share files between browsers using P2P.

These services and libraries offer various ways to establish peer-to-peer connections between browsers, facilitating direct object exchange without the need for an intermediary server after the initial connection is established.

## 5. **Trystero**

Trystero is a library that provides instant, serverless peer-to-peer communication over WebRTC. It supports multiple strategies for peer discovery, including BitTorrent, Nostr, MQTT, Supabase, Firebase, and IPFS.

- **Website:** [Trystero](https://oxism.com/trystero/)
- **How to Use:** Install Trystero via npm and use it to join a room for peer-to-peer communication.
