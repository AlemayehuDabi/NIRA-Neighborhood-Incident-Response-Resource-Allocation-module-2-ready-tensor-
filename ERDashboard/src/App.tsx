import ProtectedRoutes from './auth/protectedRoute';
import { SignIn } from './auth/signin';
import ERAdminDashboard from './ERDashboard';
import { BrowserRouter, Route, Routes } from 'react-router';
import { NotFound } from './NotFound';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route element={<SignIn />} path="/login" />
        <Route element={<ProtectedRoutes />}>
          <Route element={<ERAdminDashboard />} path="/" />
        </Route>
        <Route element={<NotFound />} path="*" />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
