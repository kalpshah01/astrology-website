import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Home from './pages/Home';
import Prediction from './pages/Prediction';
import AdminDashboard from './pages/AdminDashboard';
import AdminLogin from './pages/AdminLogin';
import AdminPredictionDetails from './pages/AdminPredictionDetails';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/prediction/:id" element={<Prediction />} />
        <Route path="/admin" element={<AdminDashboard />} />
        <Route path="/admin/login" element={<AdminLogin />} />
        <Route path="/admin/predictions/:id" element={<AdminPredictionDetails />} />
      </Routes>
    </BrowserRouter>
  )
}

export default App;
