// React imports.
import * as React from 'react';

// Material UI imports.
import { type Router } from '@toolpad/core/AppProvider';


function useRouter(initialPath: string): Router {
  const [pathname, setPathname] = React.useState(initialPath);
  const router = React.useMemo(
    () => {
      return {
        pathname,
        searchParams: new URLSearchParams(),
        navigate: (path: string | URL) => setPathname(String(path)),
      };
    }, [pathname]);

  return router;
}

export default useRouter
