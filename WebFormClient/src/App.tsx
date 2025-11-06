import ProtectedRoutes from './auth/protectedRoute';
import { Register } from './auth/register';
import { SignIn } from './auth/signin';
import Dashboard from './Dashborad/page';
import { IncidentReportForm } from './Form';
import { Route, Routes, BrowserRouter } from 'react-router-dom';

function App() {
  return (
    <>
      <BrowserRouter>
        <Routes>
          <Route path="/login" element={<SignIn />} />
          <Route path="/register" element={<Register />} />
          <Route path="/" element={<IncidentReportForm />} />
          <Route element={<ProtectedRoutes />}>
            <Route path="/" element={<Dashboard />} />
          </Route>
        </Routes>
      </BrowserRouter>
    </>
  );
}

export default App;
