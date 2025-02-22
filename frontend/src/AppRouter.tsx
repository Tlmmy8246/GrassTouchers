import { ProtectedRoute } from 'components';
import { routePaths } from 'global/routePaths';
import useAuthenticated from 'hooks/useAuthenticated'
import { Suspense } from 'react'
import { BrowserRouter, Route, Routes } from 'react-router'
import { Login, Register } from 'pages';

const AppRouter = () => {
  const { isAuthenticated } = useAuthenticated();

  return (
    <Suspense fallback={<div>Loading...</div>}>
      <BrowserRouter>
        <Routes>
          <Route path={routePaths.auth.login} element={<Login />} />
          <Route path={routePaths.auth.register} element={<Register />} />

          {/* Protected Routes here */}
          <Route element={<ProtectedRoute isAuthenticated={isAuthenticated} />}>
            <Route path={routePaths.home} element={<div>HOME PAGE HERE</div>} />
            <Route path={routePaths.globalChat} element={<div>GLOBAL CHAT PAGE HERE</div>} />
          </Route>
        </Routes>
      </BrowserRouter>
    </Suspense>
  )
}

export default AppRouter
