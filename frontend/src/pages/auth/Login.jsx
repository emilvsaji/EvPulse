import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../../context';
import { authAPI } from '../../services';
import { isValidEmail } from '../../utils';
import { Button, Input } from '../../components';
import { Zap, Mail, Lock, ArrowRight, Sparkles, Shield, Clock } from 'lucide-react';

const Login = () => {
  const navigate = useNavigate();
  const { login } = useAuth();
  
  const [formData, setFormData] = useState({
    email: '',
    password: '',
  });
  const [errors, setErrors] = useState({});
  const [loading, setLoading] = useState(false);
  const [apiError, setApiError] = useState('');

  const validateForm = () => {
    const newErrors = {};
    
    if (!formData.email) {
      newErrors.email = 'Email is required';
    } else if (!isValidEmail(formData.email)) {
      newErrors.email = 'Invalid email format';
    }
    
    if (!formData.password) {
      newErrors.password = 'Password is required';
    }
    
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
    if (errors[name]) {
      setErrors(prev => ({ ...prev, [name]: '' }));
    }
    if (apiError) setApiError('');
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!validateForm()) return;
    
    setLoading(true);
    try {
      const response = await authAPI.login(formData.email, formData.password);
      
      if (response.success) {
        login(response.user);
        const rolePath = {
          user: '/dashboard',
          operator: '/operator',
          admin: '/admin',
        };
        navigate(rolePath[response.user.role] || '/dashboard');
      } else {
        setApiError(response.error);
      }
    } catch (error) {
      setApiError('An unexpected error occurred. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const demoCredentials = [
    { role: 'User', email: 'user@evpulse.com', password: 'user123', icon: '👤' },
    { role: 'Operator', email: 'operator@evpulse.com', password: 'operator123', icon: '🔧' },
    { role: 'Admin', email: 'admin@evpulse.com', password: 'admin123', icon: '👑' },
  ];

  const fillDemoCredentials = (email, password) => {
    setFormData({ email, password });
    setErrors({});
    setApiError('');
  };

  const features = [
    { icon: Sparkles, text: 'Find nearby stations instantly' },
    { icon: Shield, text: 'Secure payment processing' },
    { icon: Clock, text: 'Real-time availability updates' },
  ];

  return (
    <div className="min-h-screen flex">
      {/* Left Panel - Branding */}
      <div className="hidden lg:flex lg:w-1/2 bg-gradient-to-br from-primary-600 via-primary-500 to-green-500 p-12 flex-col justify-between relative overflow-hidden">
        {/* Background Pattern */}
        <div className="absolute inset-0 opacity-10">
          <div className="absolute top-20 left-20 w-72 h-72 bg-white rounded-full blur-3xl" />
          <div className="absolute bottom-20 right-20 w-96 h-96 bg-white rounded-full blur-3xl" />
        </div>
        
        {/* Content */}
        <div className="relative z-10">
          <div className="flex items-center gap-3">
            <div className="w-12 h-12 bg-white/20 backdrop-blur-sm rounded-xl flex items-center justify-center">
              <Zap className="w-7 h-7 text-white" />
            </div>
            <span className="text-2xl font-bold text-white">EVPulse</span>
          </div>
        </div>
        
        <div className="relative z-10 space-y-8">
          <div>
            <h1 className="text-4xl font-bold text-white mb-4">
              Power Your Journey<br />
              <span className="text-white/80">With Smart Charging</span>
            </h1>
            <p className="text-white/70 text-lg max-w-md">
              Join thousands of EV owners who trust EVPulse for reliable, fast, and convenient charging solutions.
            </p>
          </div>
          
          <div className="space-y-4">
            {features.map((feature, index) => (
              <div key={index} className="flex items-center gap-3 text-white/90">
                <div className="w-10 h-10 bg-white/20 backdrop-blur-sm rounded-lg flex items-center justify-center">
                  <feature.icon className="w-5 h-5" />
                </div>
                <span>{feature.text}</span>
              </div>
            ))}
          </div>
        </div>
        
        <div className="relative z-10">
          <p className="text-white/60 text-sm">
            © 2026 EVPulse. All rights reserved.
          </p>
        </div>
      </div>

      {/* Right Panel - Login Form */}
      <div className="flex-1 flex items-center justify-center p-8 bg-gradient-to-br from-secondary-50 to-white">
        <div className="w-full max-w-md">
          {/* Mobile Logo */}
          <div className="lg:hidden text-center mb-8">
            <div className="inline-flex items-center justify-center w-16 h-16 bg-gradient-to-br from-primary-500 to-primary-600 rounded-2xl shadow-lg shadow-primary-500/30 mb-4">
              <Zap className="w-9 h-9 text-white" />
            </div>
            <h1 className="text-3xl font-bold text-secondary-900">
              EV<span className="text-primary-500">Pulse</span>
            </h1>
          </div>

          {/* Login Card */}
          <div className="bg-white rounded-3xl shadow-xl shadow-secondary-200/50 p-8 border border-secondary-100">
            <div className="text-center mb-8">
              <h2 className="text-2xl font-bold text-secondary-900">Welcome back</h2>
              <p className="text-secondary-500 mt-2">Sign in to continue to your dashboard</p>
            </div>
            
            {apiError && (
              <div className="mb-6 p-4 bg-red-50 border border-red-100 rounded-2xl text-red-600 text-sm flex items-center gap-3">
                <div className="w-8 h-8 bg-red-100 rounded-full flex items-center justify-center flex-shrink-0">
                  <span>⚠️</span>
                </div>
                {apiError}
              </div>
            )}

            <form onSubmit={handleSubmit} className="space-y-5">
              <Input
                label="Email Address"
                type="email"
                name="email"
                placeholder="Enter your email"
                value={formData.email}
                onChange={handleChange}
                error={errors.email}
                icon={Mail}
              />

              <Input
                label="Password"
                type="password"
                name="password"
                placeholder="Enter your password"
                value={formData.password}
                onChange={handleChange}
                error={errors.password}
                icon={Lock}
              />

              <div className="flex items-center justify-between text-sm">
                <label className="flex items-center gap-2 cursor-pointer group">
                  <input type="checkbox" className="w-4 h-4 rounded border-secondary-300 text-primary-500 focus:ring-primary-500 focus:ring-offset-0" />
                  <span className="text-secondary-600 group-hover:text-secondary-900 transition-colors">Remember me</span>
                </label>
                <Link to="/forgot-password" className="text-primary-600 hover:text-primary-700 font-medium transition-colors">
                  Forgot password?
                </Link>
              </div>

              <Button type="submit" fullWidth loading={loading} className="h-12 text-base">
                Sign In
                <ArrowRight className="w-5 h-5 ml-2" />
              </Button>
            </form>

            <div className="relative my-8">
              <div className="absolute inset-0 flex items-center">
                <div className="w-full border-t border-secondary-200"></div>
              </div>
              <div className="relative flex justify-center text-sm">
                <span className="px-4 bg-white text-secondary-500">or continue with</span>
              </div>
            </div>

            <p className="text-center text-secondary-600">
              Don't have an account?{' '}
              <Link to="/register" className="text-primary-600 hover:text-primary-700 font-semibold transition-colors">
                Sign up for free
              </Link>
            </p>
          </div>

          {/* Demo Credentials */}
          <div className="mt-6 p-5 bg-white/80 backdrop-blur-sm rounded-2xl border border-secondary-200 shadow-lg shadow-secondary-200/30">
            <p className="text-sm font-semibold text-secondary-700 mb-4 flex items-center gap-2">
              <span className="w-6 h-6 bg-primary-100 rounded-full flex items-center justify-center text-xs">🔑</span>
              Demo Credentials
            </p>
            <div className="grid gap-2">
              {demoCredentials.map((cred) => (
                <button
                  key={cred.role}
                  onClick={() => fillDemoCredentials(cred.email, cred.password)}
                  className="w-full text-left px-4 py-3 bg-secondary-50 hover:bg-primary-50 hover:border-primary-200 border border-transparent rounded-xl text-sm transition-all duration-200 flex items-center gap-3 group"
                >
                  <span className="text-lg">{cred.icon}</span>
                  <div>
                    <span className="font-semibold text-secondary-900 group-hover:text-primary-700">{cred.role}</span>
                    <span className="text-secondary-500 ml-2">{cred.email}</span>
                  </div>
                </button>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Login;
