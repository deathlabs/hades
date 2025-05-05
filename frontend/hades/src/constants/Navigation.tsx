// Material UI imports.
import EditNoteIcon from '@mui/icons-material/EditNote';
import { type Navigation }  from '@toolpad/core/AppProvider';


const NAVIGATION: Navigation = [
  {
    kind: 'header',
    title: 'Create',
  },
  {
    segment: 'create-cyber-inject-request',
    title: 'Cyber Inject Request',
    icon: <EditNoteIcon />,
  },
];

export default NAVIGATION;
