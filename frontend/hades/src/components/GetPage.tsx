// Material UI imports.
import { PageContainer } from '@toolpad/core';

// Local component imports.
import CyberInjectRequest from './create/CyberInjectRequest';
import Home from './Home';


// Returns page content based on the path given.
function GetPage({ pathname }: { pathname: string}) {
  // Define page variables. 
  let breadcrumbs;
  let page;

  // Define breadcrumb constants.
  const create  = { path: "/create", title: "Create" };
  const home    = { path: "/",       title: ""       }; 

  // Parse the path given.
  switch (pathname) {
    case '/create-cyber-inject-request': {
      breadcrumbs = [ create ];
      page = <CyberInjectRequest />;
      break;
    }
    default: {
      breadcrumbs = [ home ];
      page = <Home />;
      break;
    }
  }
    
  return (
    <PageContainer breadcrumbs={breadcrumbs}>
      {page}
    </PageContainer>
  );
}

export default GetPage;
