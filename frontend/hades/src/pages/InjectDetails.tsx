import React, { useState, useRef, useEffect } from "react";
import { useParams } from "react-router-dom";
import {
  Avatar,
  Box,
  List,
  ListItem,
  ListItemAvatar,
  ListItemText,
  Paper,
  Typography
} from "@mui/material";
import { BACKEND } from "../constants";

type ChatMessage = {
  sender: string;
  receiver: string;
  message: string;
};

const avatarMap: Record<string, string> = {
  "System": "/hades.svg",
  "HADES-Planner": "/hades.svg",
  "HADES-Operator": "/hades.svg",
};

export default function InjectDetails() {
  const { id } = useParams<{ id: string }>();
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [connected, setConnected] = useState(false);
  const wsRef = useRef<WebSocket | null>(null);

  useEffect(() => {
    if (!id) return;

    const socket = new WebSocket(`ws://${BACKEND}/ws/${id}`);

    socket.onopen = () => {
      setConnected(true);
      setMessages((prev) => [
        ...prev,
        { sender: "System", receiver: "Client", message: "Connecting..." }
      ]);
    };

    socket.onmessage = (event) => {
      const parsed: ChatMessage = JSON.parse(event.data);
      setMessages((prev) => [...prev, parsed]);
    };

    socket.onclose = (event) => {
      setConnected(false);
      setMessages((prev) => [
        ...prev,
        {
          sender: "System",
          receiver: "Client",
          message: `Connection closed (Error: ${event.code}, Reason: ${event.reason || "Connection closed"})`
        }
      ]);
    };

    wsRef.current = socket;

    // Cleanup: just detach handlers, don't close again
    return () => {
      socket.onopen = null;
      socket.onmessage = null;
      socket.onclose = null;
      socket.onerror = null;
      wsRef.current = null;
    };
  }, [id]);

  return (
    <Box sx={{ p: 2, ml: 2, mt: 1, display: "grid", gap: 2, maxWidth: 600 }}>
      <Typography variant="subtitle1">
        <Box component="b">Inject</Box> (ID: {id})
      </Typography>
      <Paper>
        <List>
          {messages.map((msg, i) => {
            const isPlanner = msg.sender === "HADES-Planner";
            return (
              <ListItem
                key={i}
                sx={{
                  display: "flex",
                  flexDirection: isPlanner ? "row-reverse" : "row",
                  alignItems: "center",
                }}
              >
                <ListItemAvatar>
                  <Avatar
                    alt={msg.sender}
                    src={avatarMap[msg.sender]}
                    sx={{ width: 56, height: 56 }}
                  />
                </ListItemAvatar>
                <ListItemText
                  primary={msg.sender}
                  secondary={msg.message}
                  sx={{
                    textAlign: isPlanner ? "right" : "left",
                  }}
                />
              </ListItem>
            );
          })}
        </List>
      </Paper>
    </Box>
  );
}
