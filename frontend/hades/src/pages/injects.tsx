import React, { useState, useRef, useEffect } from "react";

export default function Injects() {
  const [uuid, setUuid] = useState("");
  const [messages, setMessages] = useState<string[]>([]);
  const [connected, setConnected] = useState(false);
  const wsRef = useRef<WebSocket | null>(null);

  useEffect(() => {
    const params = new URLSearchParams(window.location.search);
    const qUuid = params.get("uuid");
    if (qUuid) {
      setUuid(qUuid);
      connect(qUuid);  // auto-connect
    }
  }, []);

  const connect = (id: string = uuid) => {
    if (!id) return;
    const socket = new WebSocket(`ws://localhost:8888/ws/${id}`);

    socket.onopen = () => {
      setConnected(true);
      setMessages((prev) => [...prev, "✅ Connected"]);
    };

    socket.onmessage = (event) => {
      setMessages((prev) => [...prev, `📩 ${event.data}`]);
    };

    socket.onclose = () => {
      setConnected(false);
      setMessages((prev) => [...prev, "❌ Disconnected"]);
    };

    socket.onerror = (err) => {
      setMessages((prev) => [...prev, `⚠️ Error: ${err}`]);
    };

    wsRef.current = socket;
  };

  const disconnect = () => {
    wsRef.current?.close();
    wsRef.current = null;
  };

  return (
    <div style={{ padding: "20px", fontFamily: "sans-serif" }}>
      <h2>RabbitMQ WebSocket Client</h2>
      <input
        type="text"
        placeholder="Enter UUID"
        value={uuid}
        onChange={(e) => setUuid(e.target.value)}
        style={{ padding: "8px", width: "300px" }}
      />
      <div style={{ marginTop: "10px" }}>
        {!connected ? (
          <button onClick={() => connect()} style={{ padding: "8px 12px" }}>
            Connect
          </button>
        ) : (
          <button onClick={disconnect} style={{ padding: "8px 12px" }}>
            Disconnect
          </button>
        )}
      </div>

      <div style={{ marginTop: "20px" }}>
        <h3>Messages</h3>
        <ul>
          {messages.map((msg, i) => (
            <li key={i}>{msg}</li>
          ))}
        </ul>
      </div>
    </div>
  );
}
