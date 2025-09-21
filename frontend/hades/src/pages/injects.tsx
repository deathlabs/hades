import { useEffect, useRef, useState } from "react";
import {
  Box,
  Button,
  Card,
  CardContent,
  MenuItem,
  Paper,
  Select,
  TextField,
  Typography,
} from "@mui/material";

const WS_URL = "ws://127.0.0.1:5174/ws";

export default function WsMissionSender() {
  const wsRef = useRef<WebSocket | null>(null);
  const [connected, setConnected] = useState(false);
  const [inbox, setInbox] = useState<string[]>([]);

  // Form state
  const [missionType, setMissionType] = useState("recon");
  const [target, setTarget] = useState("");
  const [priority, setPriority] = useState("normal");

  useEffect(() => {
    const ws = new WebSocket(WS_URL);
    wsRef.current = ws;

    ws.onopen = () => setConnected(true);
    ws.onclose = () => setConnected(false);
    ws.onmessage = (e) => setInbox((prev) => [...prev, e.data]);

    return () => ws.close();
  }, []);

  const sendMission = () => {
    if (wsRef.current && wsRef.current.readyState === WebSocket.OPEN) {
      const mission = {
        type: "mission",
        key: `missions.${missionType}`,
        payload: {
          target,
          priority,
        },
      };
      wsRef.current.send(JSON.stringify(mission));
    }
  };

  return (
    <Box sx={{ p: 2, display: "grid", gap: 2, maxWidth: 600 }}>
      <Typography variant="h6">WebSocket: {connected ? "🟢 Connected" : "🔴 Disconnected"}</Typography>

      <Card>
        <CardContent sx={{ display: "grid", gap: 2 }}>
          <Typography variant="subtitle1">Create Mission</Typography>

          <Select
            value={missionType}
            onChange={(e) => setMissionType(e.target.value)}
          >
            <MenuItem value="recon">Recon</MenuItem>
            <MenuItem value="attack">Attack</MenuItem>
            <MenuItem value="defend">Defend</MenuItem>
          </Select>

          <TextField
            label="Target"
            value={target}
            onChange={(e) => setTarget(e.target.value)}
            placeholder="10.0.0.5"
          />

          <Select
            value={priority}
            onChange={(e) => setPriority(e.target.value)}
          >
            <MenuItem value="low">Low</MenuItem>
            <MenuItem value="normal">Normal</MenuItem>
            <MenuItem value="high">High</MenuItem>
          </Select>

          <Button
            variant="contained"
            onClick={sendMission}
            disabled={!connected}
          >
            Send Mission
          </Button>
        </CardContent>
      </Card>

      <Typography variant="h6">Incoming Messages</Typography>
      <Paper
        sx={{
          p: 2,
          maxHeight: 300,
          overflowY: "auto",
          backgroundColor: "#f5f5f5",
        }}
      >
        {inbox.map((m, i) => {
          try {
            const obj = JSON.parse(m);
            return (
              <pre key={i} style={{ margin: 0 }}>
                {JSON.stringify(obj, null, 2)}
              </pre>
            );
          } catch {
            return (
              <Typography key={i} variant="body2">
                {m}
              </Typography>
            );
          }
        })}
      </Paper>
    </Box>
  );
}
