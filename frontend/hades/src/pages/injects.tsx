import { useState } from "react";
import {
  Box,
  Button,
  Card,
  CardContent,
  FormControl,
  InputLabel,
  MenuItem,
  Select,
  SelectChangeEvent,
  TextField,
} from "@mui/material";
import Chip from '@mui/material/Chip';
import Stepper from "@mui/material/Stepper";
import Step from "@mui/material/Step";
import StepLabel from "@mui/material/StepLabel";
import StepContent from "@mui/material/StepContent";
import Alert from '@mui/material/Alert';
import { AlertColor } from "@mui/material/Alert";
import IconButton from '@mui/material/IconButton';
import Collapse from '@mui/material/Collapse';
import CloseIcon from '@mui/icons-material/Close';

const BACKEND_URL = import.meta.env.VITE_BACKEND_URL;

const DefaultInjectName = "Scan the network";

const DefaultNetworkId = "192.168.152.0";

const DefaultSubnetMask = "255.255.255.0";

const TargetTypes = [
  { key: "machine", value: "Machine" },
  { key: "persona", value: "Persona" },
]

const DefaultTargetId = "192.168.152.128";

const Goals = [
  { key: "shutdown", value: "Shutdown" },
]

const Techniques = [
  { key: "exploiting-known-vulnerabilities", value: "Exploiting known vulnerabilities" },
  { key: "phishing-via-email", value: "Phishing via email" },
  { key: "denial-of-service-attacks", value: "Denial of Service attacks" },
]

const DefaultInjectId = "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee"

const DefaultAlertSeverity = "info";

type ReportingRequirement = {
  requirement: string;
  channel: string;
  frequency: string;
};

type Target = {
  type: string;
  address: string;
  goals: string[];
};

type System = {
  network_id: string;
  subnet_mask: string;
  targets: Target[];
};

type Inject = {
  id: string;
  name: string;
  rules_of_engagement: {
    techniques: {
      allowed: string[];
      prohibited: string[];
    };
    reporting: {
      requirements: ReportingRequirement[];
    };
  };
  systems: System[];
};


export default function InjectsCrudPage() {
  const [injectName, setInjectName] = useState(DefaultInjectName);
  const [networkId, setNetworkId] = useState(DefaultNetworkId);
  const [subnetMask, setSubnetMask] = useState(DefaultSubnetMask);
  const [targetType, setTargetType] = useState(TargetTypes[0].value);
  const [targetId, setTargetId] = useState(DefaultTargetId);
  const [goals, setGoals] = useState<string[]>([Goals[0].value]);
  const [allowed, setAllowed] = useState<string[]>([Techniques[0].value]);
  const [prohibited, setProhibited] = useState<string[]>([Techniques[Techniques.length - 1].value]);

  const [injectId, setInjectId] = useState(DefaultInjectId);
  const [activeStep, setActiveStep] = useState(0);
  const [loading, setLoading] = useState(false);
  const [alertSeverity, setAlertSeverity] = useState<AlertColor>(DefaultAlertSeverity);
  const [alertMessage, setAlertMessage] = useState("");
  const [showAlert, setShowAlert] = useState(false);
 
  const handleNext = () => {
    setActiveStep((prevActiveStep) => prevActiveStep + 1);
  };

  const handleBack = () => {
    setActiveStep((prevActiveStep) => prevActiveStep - 1);
  };

  const handleGoals = (event: SelectChangeEvent<typeof goals>) => {
    const { target: { value } } = event;
    setGoals(
      typeof value === 'string' ? value.split(',') : value,
    );
  };

  const handleAllowed = (event: SelectChangeEvent<typeof allowed>) => {
    const { target: { value } } = event;
    setAllowed(
      typeof value === 'string' ? value.split(',') : value,
    );
  };

  const handleProhibited = (event: SelectChangeEvent<typeof allowed>) => {
    const { target: { value } } = event;
    setProhibited(
      typeof value === 'string' ? value.split(',') : value,
    );
  };

  const resetForm = () => {
    setActiveStep(0);
    setInjectName(DefaultInjectName);
    setNetworkId(DefaultNetworkId);
    setSubnetMask(DefaultSubnetMask);
    setTargetType(TargetTypes[0].value);
    setTargetId(DefaultTargetId);
    setGoals([Goals[0].value]);
    setAllowed([Techniques[0].value]);
    setProhibited([Techniques[Techniques.length - 1].value]);
    setInjectId(DefaultInjectId);
    setAlertSeverity(DefaultAlertSeverity);
    setAlertMessage("");
  };

  const submitInject = async () => {
    setLoading(true);
    const inject: Inject = {
      id: injectId,
      name: injectName,
      rules_of_engagement: {
        techniques: {
          allowed: allowed,
          prohibited: prohibited,
        },
        reporting: {
          requirements: [
            {
              requirement: "",
              channel: "",
              frequency: "",
            },
          ],
        },
      },
      systems: [
        {
          network_id: networkId,
          subnet_mask: subnetMask,
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
      const response = await fetch(`${BACKEND_URL}`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(inject),
      });
      
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}`);
      }

      const text = await response.json();
      setActiveStep(0);
      setInjectId(text.uuid);
      setLoading(false);
      setAlertSeverity("success");
      setAlertMessage(injectId);
      setShowAlert(true);
    } catch (err) {
      setLoading(false);
      setAlertSeverity("error");
      setAlertMessage((err as Error).message);
      setShowAlert(true);
    }
  };

  const steps = [
    {
      label: "Identify the inject",
      content: <>
        <TextField
          label="Inject Name"
          required
          value={injectName}
          onChange={(e) => setInjectName(e.target.value)}
        />
      </>,
    },
    {
      label: "Identify the network",
      content: <>
        <TextField
          label="Network ID"
          required
          value={networkId}
          onChange={(e) => setNetworkId(e.target.value)}
        />
        <TextField
          label="Subnet Mask"
          required
          value={subnetMask}
          onChange={(e) => setSubnetMask(e.target.value)}
        />
      </>
    },
    {
      label: "Identify the target",
      content: <>
        <FormControl>
          <InputLabel>Target Type</InputLabel>
          <Select
            label="Target Type"
            required
            value={targetType}
            onChange={(e) => setTargetType(e.target.value)}
          >
            {TargetTypes.map((targetType) => (
            <MenuItem key={targetType.key} value={targetType.value}>
              {targetType.value}
            </MenuItem>
            ))}
          </Select>
        </FormControl>
        <TextField
          label="Target ID"
          required
          value={targetId}
          onChange={(e) => setTargetId(e.target.value)}
        />
      </>
    },
    {
      label: "Identify the Rules of Engagement",
      content: <>
        <FormControl>
          <InputLabel>Goals</InputLabel>
          <Select
            label="Goals"
            required
            multiple
            value={goals}
            onChange={handleGoals}
            renderValue={(selected) => (
            <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 0.5 }}>
              {selected.map((value) => (
                <Chip key={value} label={value} />
              ))}
            </Box>
          )}
          >
            {Goals.map((goal) => (
            <MenuItem key={goal.key} value={goal.value}>
              {goal.value}
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
            <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 0.5 }}>
              {selected.map((value) => (
                <Chip key={value} label={value} />
              ))}
            </Box>
          )}
          >
            {Techniques.map((technique) => (
            <MenuItem key={technique.key} value={technique.value}>
              {technique.value}
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
            <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 0.5 }}>
              {selected.map((value) => (
                <Chip key={value} label={value} />
              ))}
            </Box>
          )}
          >
            {Techniques.map((technique) => (
            <MenuItem key={technique.key} value={technique.value}>
              {technique.value}
            </MenuItem>
            ))}
          </Select>
        </FormControl>
      </>,
    },
    {
      label: "Submit the inject",
      content: ""
    }
  ];

  return (
    <Box sx={{ p: 2, ml: 2, mt: 0, display: "grid", gap: 2, maxWidth: 600 }}>
      <Collapse in={showAlert}>
        <Alert
          severity={alertSeverity}
          sx={{ m: 2 }}
          action={
            <IconButton
              aria-label="close"
              color="inherit"
              size="small"
              onClick={() => { setShowAlert(false); }}
            >
              <CloseIcon fontSize="inherit" />
            </IconButton>
          }
          
        >
          {alertMessage}
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
                      loading={loading}
                      onClick={() => {
                        if (index === steps.length - 1) {
                          submitInject();
                        } else {
                          handleNext();
                        }
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
