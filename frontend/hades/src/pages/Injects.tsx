import { useState, useEffect } from "react";
import { Box, Paper, Link, Chip, Stack } from "@mui/material";
import { DataGrid, GridColDef } from "@mui/x-data-grid";
import { Link as RouterLink } from "react-router-dom";
import { NewInject } from "./Inject";
import { BACKEND } from "../constants";

type Inject = Record<string, NewInject>;

export default function Injects() {
  const [rows, setRows] = useState<any[]>([]);

  useEffect(() => {
    (async () => {
      const response = await fetch(`http://${BACKEND}`);
      if (response.ok) {
        const data: Inject = await response.json();
        const formatted = Object.entries(data).map(([id, inject]) => ({
          id,
          name: inject.name,
          allowed: inject.rules_of_engagement.techniques.allowed ?? [],
          prohibited: inject.rules_of_engagement.techniques.prohibited ?? [],
          systems: inject.systems.length,
        }));
        setRows(formatted);
      }
    })();
  }, []);

  const columns: GridColDef[] = [
    {
      field: "id",
      headerName: "ID",
      flex: 1,
      minWidth: 200,
      renderCell: (params) => (
        <Link
          component={RouterLink}
          to={`/injects/${params.value}`}
          underline="hover"
          sx={{
            maxWidth: "100%",
            overflow: "hidden",
            textOverflow: "ellipsis",
            whiteSpace: "nowrap",
            display: "block",
          }}
        >
          {params.value}
        </Link>
      ),
    },
    { field: "name", headerName: "Name", flex: 1, minWidth: 150 },
    {
      field: "allowed",
      headerName: "Allowed Techniques",
      flex: 1,
      renderCell: (params) => {
        const values: string[] = Array.isArray(params.value) ? params.value : [];
        return (
          <Box
            sx={{
              display: "flex",
              alignItems: "center",
              height: "100%",
              flexWrap: "wrap",
            }}
          >
            {values.map((tech, idx) => (
              <Chip key={idx} label={tech} color="success" size="small" />
            ))}
          </Box>
        );
      },
    },
    {
      field: "prohibited",
      headerName: "Prohibited Techniques",
      flex: 1,
      renderCell: (params) => {
        const values: string[] = Array.isArray(params.value) ? params.value : [];
        return (
          <Box
            sx={{
              display: "flex",
              alignItems: "center",
              height: "100%",
              flexWrap: "wrap",
            }}
          >
            {values.map((tech, idx) => (
              <Chip key={idx} label={tech} color="error" size="small" />
            ))}
          </Box>
        );
      },
    },
    { field: "systems", headerName: "Systems" },
  ];

  return (
    <Box sx={{ p: 2 }}>
      <Paper sx={{ height: 400, width: "100%", alignItems: "center" }}>
        <DataGrid
          rows={rows}
          columns={columns}
          disableRowSelectionOnClick
          initialState={{
            pagination: { paginationModel: { page: 0, pageSize: 5 } },
          }}
          pageSizeOptions={[5, 10]}
          sx={{ border: 0 }}
        />
      </Paper>
    </Box>
  );
}
