// React imports.
import React from 'react';

// Material UI imports.
import { AppProvider, type Session } from '@toolpad/core/AppProvider';
import { DashboardLayout } from '@toolpad/core/DashboardLayout';

// Local component imports.
import GetPage from './components/GetPage';

// Local hook imports.
import useRouter from './hooks/Router';

// Local constant imports.
import FOOTER from './constants/Footer';
import NAVIGATION from './constants/Navigation';
import THEME from './constants/Theme';

// Local asset imports.
import Logo from './assets/hades.png'
import ProfileImage from './assets/profile.jpg';

const PROFILE = {
  user: {
    name: 'CW3 Vic Fernandez',
    email: 'victor.fernandez19.mil@army.mil',
    image: ProfileImage,
  },
}

function App() {
    const router = useRouter('/'); 
    const [profile, setProfile] = React.useState<Session | null>(PROFILE);
    const authentication = React.useMemo(
      () => {
        return {
          signIn: () => {
            setProfile(PROFILE);
          },
          signOut: () => {
            //
          },
        };
      },
      []
    );
    return (
      <AppProvider 
        theme={THEME}
        branding={{
          title: 'HADES',
          logo: <img src={Logo} alt="HADES Logo"/>,
        }}
        navigation={NAVIGATION}
        router={router}
        session={profile}
        authentication={authentication}
      >
        <DashboardLayout
          defaultSidebarCollapsed
          slots={{
            sidebarFooter: FOOTER,
          }}
          slotProps={{
            toolbarAccount: {
              localeText: {
                signOutLabel: 'Exit'
              },
            }
          }}
        >
          <GetPage pathname={router.pathname}/>
        </DashboardLayout>
      </AppProvider>
    )
}

export default App
