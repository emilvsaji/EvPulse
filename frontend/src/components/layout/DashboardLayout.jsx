import { useState } from 'react';
import { Outlet } from 'react-router-dom';
import Sidebar from './Sidebar';
import Navbar from './Navbar';
import Toast from '../ui/Toast';
import { useNotifications } from '../../context';

const DashboardLayout = ({ children }) => {
  const [mobileOpen, setMobileOpen] = useState(false);
  const { toasts, removeToast } = useNotifications();

  return (
    <div className="min-h-screen bg-gradient-to-br from-secondary-50 via-white to-secondary-50/50">
      {/* Sidebar */}
      <Sidebar 
        mobileOpen={mobileOpen} 
        onMobileClose={() => setMobileOpen(false)} 
      />

      {/* Main Content */}
      <div className="lg:pl-72 min-h-screen transition-all duration-300 flex flex-col">
        <Navbar onMenuClick={() => setMobileOpen(!mobileOpen)} />
        <main className="flex-1 w-full h-full">
          {children ?? <Outlet />}
        </main>
      </div>

      {/* Toasts */}
      <div className="fixed bottom-4 right-4 z-50 space-y-3">
        {toasts.map((toast) => (
          <Toast
            key={toast.id}
            type={toast.type}
            message={toast.message}
            onClose={() => removeToast(toast.id)}
          />
        ))}
      </div>
    </div>
  );
};

export default DashboardLayout;
