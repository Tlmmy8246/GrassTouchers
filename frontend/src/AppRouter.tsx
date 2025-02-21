import { ProtectedRoute } from 'components';
import { routePaths } from 'global/routePaths';
import useAuthenticated from 'hooks/useAuthenticated'
import { Suspense } from 'react'
import { BrowserRouter, Route } from 'react-router'

const AppRouter = () => {
  const { isAuthenticated } = useAuthenticated();

  return (
    <Suspense fallback={<div>Loading...</div>}>
      <BrowserRouter>
        <Route path={routePaths.auth.login} element={<div>LOGIN PAGE HERE</div>} />

        {/* Protected Routes here */}
        <Route element={<ProtectedRoute isAuthenticated={isAuthenticated} />}>
          <Route path={routePaths.home} element={<div>HOME PAGE HERE</div>} />
          <Route path={routePaths.globalChat} element={<div>GLOBAL CHAT PAGE HERE</div>} />
        </Route>
      </BrowserRouter>
    </Suspense>
  )
}

export default AppRouter
