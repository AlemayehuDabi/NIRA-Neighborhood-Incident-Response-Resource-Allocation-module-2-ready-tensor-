import { Outlet, Navigate } from 'react-router-dom';

const getToken = () => {
  return localStorage.getItem('token');
};

const ProtectedRoutes = () => {
  // Replace with your actual authentication check
  const isAuthenticated = getToken();

  return isAuthenticated ? <Outlet /> : <Navigate to="/login" replace />;
};

export default ProtectedRoutes;
