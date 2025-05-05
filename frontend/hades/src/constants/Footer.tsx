// Material UI imports.
import Typography from '@mui/material/Typography';
import { type SidebarFooterProps } from '@toolpad/core/DashboardLayout';


function FOOTER({ mini }: SidebarFooterProps) {
    return (
      <Typography
        variant="caption"
        sx={{
            m: 1,
            whiteSpace: 'nowrap',
            overflow: 'hidden'
        }}
      >
        {mini ? '© AI2C' : `© ${new Date().getFullYear()} AI2C - Infrastructure & Platforms`}
      </Typography>
    );
}

export default FOOTER
