import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import {
  Alert,
  Box,
  Button,
  Card,
  CardContent,
  Chip,
  Collapse,
  FormControl,
  IconButton,
  InputLabel,
  Link,
  MenuItem,
  Select,
  SelectChangeEvent,
  Step,
  StepContent,
  StepLabel,
  Stepper,
  TextField,
} from "@mui/material";
import { AlertColor } from "@mui/material/Alert";
import CloseIcon from "@mui/icons-material/Close";
import { BACKEND } from "../constants";

const TargetTypes = [
  { key: "Machine", value: "machine" },
  { key: "Persona", value: "persona" },
];

const Goals = [
  { key: "Scan", value: "scan" },
  { key: "Shutdown", value: "shutdown" },
];

const Techniques = [
  { key: "Exploiting known vulnerabilities", value: "exploiting-known-vulnerabilities" },
  { key: "Phishing via email", value: "phishing-via-email" },
  { key: "Denial-of-Service attacks", value: "denial-of-service-attacks" },
];

type Target = {
  type: string;
  address: string;
  goals: string[];
};

type System = {
  targets: Target[];
};

export type NewInject = {
  name: string;
  rules_of_engagement: {
    techniques: {
      allowed: string[];
      prohibited: string[];
    };
  };
  systems: System[];
};

export default function Inject() {
  const [injectName, setInjectName] = useState("");
  const [targetType, setTargetType] = useState(TargetTypes[0]?.value || "");
  const [targetId, setTargetId] = useState("");
  const [goals, setGoals] = useState<string[]>([]);
  const [allowed, setAllowed] = useState<string[]>([]);
  const [prohibited, setProhibited] = useState<string[]>([]);
  const [activeStep, setActiveStep] = useState(0);
  const [loading, setLoading] = useState(false);
  const [alertSeverity, setAlertSeverity] = useState<AlertColor>("info");
  const [alertMessage, setAlertMessage] = useState("");
  const [showAlert, setShowAlert] = useState(false);
  const navigate = useNavigate();

  const hasConflict = allowed.some((v) => prohibited.includes(v));

  const handleNext = () => {
    setShowAlert(false);
    setActiveStep((prev) => prev + 1);
  };

  const handleBack = () => setActiveStep((prev) => prev - 1);

  const handleGoals = (event: SelectChangeEvent<typeof goals>) => {
    const { value } = event.target;
    setGoals(typeof value === "string" ? value.split(",") : value);
  };

  const handleAllowed = (event: SelectChangeEvent<typeof allowed>) => {
    const { value } = event.target;
    setAllowed(typeof value === "string" ? value.split(",") : value);
  };

  const handleProhibited = (event: SelectChangeEvent<typeof prohibited>) => {
    const { value } = event.target;
    setProhibited(typeof value === "string" ? value.split(",") : value);
  };

  const resetForm = () => {
    setActiveStep(0);
    setInjectName("");
    setTargetType(TargetTypes[0]?.value || "");
    setTargetId("");
    setGoals([]);
    setAllowed([]);
    setProhibited([]);
  };

  useEffect(() => {
    if (hasConflict) {
      setAlertSeverity("error");
      setAlertMessage("A technique cannot be both allowed and prohibited.");
      setShowAlert(true);
    } else if (alertSeverity === "error") {
      setShowAlert(false);
      setAlertMessage("");
    }
  }, [allowed, prohibited]);

  const submitInject = async () => {
    setLoading(true);
    const inject: NewInject = {
      name: injectName,
      rules_of_engagement: {
        techniques: { allowed, prohibited },
      },
      systems: [
        {
          targets: [
            {
              type: targetType,
              address: targetId,
              goals: goals,
            },
          ],
        },
      ],
    };

    try {
      const response = await fetch(`http://${BACKEND}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(inject),
      });

      if (!response.ok) throw new Error(`HTTP ${response.status}`);

      const text = await response.json();
      setLoading(false);
      navigate(`/injects/${text.id}`);
    } catch (err) {
      setLoading(false);
      setAlertSeverity("error");
      setAlertMessage((err as Error).message);
      setShowAlert(true);
    }
  };

  const stepValid = [
    !!injectName.trim(),
    !!targetType.trim() && !!targetId.trim(),
    goals.length > 0 && allowed.length > 0 && prohibited.length > 0 && !hasConflict,
    true,
  ];

  const steps = [
    {
      label: "Name the inject",
      content: (
        <TextField
          label="Inject Name"
          placeholder="Hack the planet"
          required
          value={injectName}
          onChange={(e) => setInjectName(e.target.value)}
        />
      ),
    },
    {
      label: "Identify a target on the network",
      content: (
        <>
          <FormControl>
            <InputLabel>Target Type</InputLabel>
            <Select
              label="Target Type"
              required
              value={targetType}
              onChange={(e) => setTargetType(e.target.value)}
            >
              {TargetTypes.map((t) => (
                <MenuItem key={t.value} value={t.value}>
                  {t.key}
                </MenuItem>
              ))}
            </Select>
          </FormControl>
          <TextField
            label="Target ID"
            placeholder="192.168.177.128"
            required
            value={targetId}
            onChange={(e) => setTargetId(e.target.value)}
          />
        </>
      ),
    },
    {
      label: "Identify the rules of engagement",
      content: (
        <>
          <FormControl>
            <InputLabel>Goals</InputLabel>
            <Select
              label="Goals"
              required
              multiple
              value={goals}
              onChange={handleGoals}
              renderValue={(selected) => (
                <Box sx={{ display: "flex", flexWrap: "wrap", gap: 0.5 }}>
                  {selected.map((value) => {
                    const g = Goals.find((goal) => goal.value === value);
                    return <Chip key={value} label={g ? g.key : value} />;
                  })}
                </Box>
              )}
            >
              {Goals.map((goal) => (
                <MenuItem key={goal.value} value={goal.value}>
                  {goal.key}
                </MenuItem>
              ))}
            </Select>
          </FormControl>
          <FormControl>
            <InputLabel>Allowed Techniques</InputLabel>
            <Select
              label="Allowed Techniques"
              required
              multiple
              value={allowed}
              onChange={handleAllowed}
              renderValue={(selected) => (
                <Box sx={{ display: "flex", flexWrap: "wrap", gap: 0.5 }}>
                  {selected.map((value) => {
                    const t = Techniques.find((tech) => tech.value === value);
                    return <Chip key={value} label={t ? t.key : value} />;
                  })}
                </Box>
              )}
            >
              {Techniques.map((technique) => (
                <MenuItem key={technique.value} value={technique.value}>
                  {technique.key}
                </MenuItem>
              ))}
            </Select>
          </FormControl>
          <FormControl>
            <InputLabel>Prohibited Techniques</InputLabel>
            <Select
              label="Prohibited Techniques"
              required
              multiple
              value={prohibited}
              onChange={handleProhibited}
              renderValue={(selected) => (
                <Box sx={{ display: "flex", flexWrap: "wrap", gap: 0.5 }}>
                  {selected.map((value) => {
                    const t = Techniques.find((tech) => tech.value === value);
                    return <Chip key={value} label={t ? t.key : value} />;
                  })}
                </Box>
              )}
            >
              {Techniques.map((technique) => (
                <MenuItem key={technique.value} value={technique.value}>
                  {technique.key}
                </MenuItem>
              ))}
            </Select>
          </FormControl>
        </>
      ),
    },
    { label: "Submit the inject", content: "" },
  ];

  return (
    <Box sx={{ p: 2, ml: 2, mt: 1, display: "grid", gap: 2, maxWidth: 600 }}>
      <Collapse in={showAlert}>
        <Alert
          severity={alertSeverity}
          sx={{ m: 2 }}
          action={
            <IconButton color="inherit" size="small" onClick={() => setShowAlert(false)}>
              <CloseIcon fontSize="inherit" />
            </IconButton>
          }
        >
          {alertMessage.startsWith("inject-") ? (
            <Link href={`/injects/${alertMessage.replace(/^inject-/, "")}`}>Inject submitted!</Link>
          ) : (
            alertMessage
          )}
        </Alert>
      </Collapse>

      <Stepper activeStep={activeStep} orientation="vertical">
        {steps.map((step, index) => (
          <Step key={step.label}>
            <StepLabel>{step.label}</StepLabel>
            <StepContent>
              <Card>
                <CardContent sx={{ m: 2, display: "grid", gap: 2, maxWidth: 600 }}>
                  {step.content}
                  <Box sx={{ mb: 2 }}>
                    <Button
                      variant="contained"
                      disabled={!stepValid[index] || hasConflict || loading}
                      onClick={() => {
                        if (index === steps.length - 1) submitInject();
                        else handleNext();
                      }}
                      sx={{ mt: 1, mr: 1 }}
                    >
                      {index === steps.length - 1 ? "Submit" : "Next"}
                    </Button>
                    <Button
                      disabled={index === 0}
                      onClick={handleBack}
                      sx={{ mt: 1, mr: 1 }}
                    >
                      Back
                    </Button>
                    <Button onClick={resetForm} sx={{ mt: 1, mr: 1 }}>
                      Reset
                    </Button>
                  </Box>
                </CardContent>
              </Card>
            </StepContent>
          </Step>
        ))}
      </Stepper>
    </Box>
  );
}
