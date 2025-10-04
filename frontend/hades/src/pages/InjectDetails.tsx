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
  Typography,
} from "@mui/material";
import { BACKEND } from "../constants";

type FunctionCall = {
  name: string;
  arguments?: Record<string, any>;
};

type ToolCall = {
  id: string;
  name: string;
  arguments?: Record<string, any>;
};

type ChatMessage = {
  sender: string;
  receiver?: string;
  message?: string;
  function_call?: FunctionCall[];
  tool_calls?: ToolCall[];
  timestamp?: string;
};

const avatarMap: Record<string, string> = {
  System: "/assets/logo.png",
  "HADES-Planner": "/assets/logo.png",
  "HADES-Operator": "/assets/logo.png",
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
        {
          sender: "System",
          receiver: "Client",
          message: "Connecting...",
          timestamp: new Date().toISOString(),
        },
      ]);
    };

    socket.onmessage = (event) => {
      const parsed: ChatMessage = JSON.parse(event.data);
      if (!parsed.timestamp) parsed.timestamp = new Date().toISOString();
      setMessages((prev) => [...prev, parsed]);
      console.log("Received:", JSON.stringify(parsed, null, 2));
    };

    socket.onclose = (event) => {
      setConnected(false);
      setMessages((prev) => [
        ...prev,
        {
          sender: "System",
          receiver: "Client",
          message: `Connection closed (Error: ${event.code}, Reason: ${
            event.reason || "Blame the distant end"
          })`,
          timestamp: new Date().toISOString(),
        },
      ]);
    };

    wsRef.current = socket;

    return () => {
      socket.onopen = null;
      socket.onmessage = null;
      socket.onclose = null;
      socket.onerror = null;
      wsRef.current = null;
    };
  }, [id]);

  return (
    <Box sx={{ p: 2, ml: 2, mt: 1, display: "grid", gap: 2, maxWidth: "100%" }}>
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
                  alignItems: "flex-start",
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
                  primary={
                    <Box
                      sx={{
                        display: "flex",
                        flexDirection: "column",
                        alignItems: isPlanner ? "flex-end" : "flex-start",
                      }}
                    >
                      <Typography variant="subtitle2">{msg.sender}</Typography>
                      {msg.timestamp && (
                        <Typography
                          variant="caption"
                          color="text.secondary"
                          sx={{ fontSize: "0.75rem" }}
                        >
                          {new Date(msg.timestamp).toLocaleTimeString()}
                        </Typography>
                      )}
                    </Box>
                  }
                  secondary={
                    msg.message ? (
                      msg.message
                    ) : msg.tool_calls ? (
                      <Box sx={{ mt: 1 }}>
                        {msg.tool_calls.map((tool, idx) => (
                          <Box
                            key={idx}
                            sx={{
                              mb: 1,
                              pl: 1.5,
                              borderLeft: "3px solid #ccc",
                            }}
                          >
                            <Typography variant="body2">
                              🧰 <b>{tool.name}</b>
                            </Typography>
                            {tool.arguments && (
                              <Box sx={{ mt: 0.5 }}>
                                {Object.entries(tool.arguments.args || {}).map(
                                  ([key, value]) => (
                                    <Typography
                                      key={key}
                                      variant="caption"
                                      sx={{
                                        fontFamily: "monospace",
                                        display: "block",
                                      }}
                                    >
                                      <b>{key}:</b>{" "}
                                      {Array.isArray(value)
                                        ? value.join(", ")
                                        : String(value)}
                                    </Typography>
                                  )
                                )}
                              </Box>
                            )}
                          </Box>
                        ))}
                      </Box>
                    ) : msg.function_call ? (
                      <Box sx={{ mt: 1 }}>
                        {msg.function_call.map((fn, idx) => (
                          <Box
                            key={idx}
                            sx={{
                              mb: 1,
                              pl: 1.5,
                              borderLeft: "3px solid #ccc",
                            }}
                          >
                            <Typography variant="body2">
                              🧩 <b>{fn.name}</b>
                            </Typography>
                            {fn.arguments && (
                              <Box sx={{ mt: 0.5 }}>
                                {Object.entries(fn.arguments || {}).map(
                                  ([key, value]) => (
                                    <Typography
                                      key={key}
                                      variant="caption"
                                      sx={{
                                        fontFamily: "monospace",
                                        display: "block",
                                      }}
                                    >
                                      <b>{key}:</b>{" "}
                                      {Array.isArray(value)
                                        ? value.join(", ")
                                        : String(value)}
                                    </Typography>
                                  )
                                )}
                              </Box>
                            )}
                          </Box>
                        ))}
                      </Box>
                    ) : ( "(no content)" )
                  }
                  sx={{
                    whiteSpace: "pre-wrap",
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
