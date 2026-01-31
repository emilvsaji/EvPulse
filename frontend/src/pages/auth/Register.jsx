import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../../context';
import { authAPI } from '../../services';
import { isValidEmail, isValidPassword, isValidPhone } from '../../utils';
import { Button, Input, Select } from '../../components';
import { Zap, Mail, Lock, User, Phone, Building2, ArrowRight, ChevronRight, Battery, MapPin, CreditCard } from 'lucide-react';

const Register = () => {
  const navigate = useNavigate();
  const { login } = useAuth();
  
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    phone: '',
    password: '',
    confirmPassword: '',
    role: 'user',
    company: '',
  });
  const [errors, setErrors] = useState({});
  const [loading, setLoading] = useState(false);
  const [apiError, setApiError] = useState('');
  const [agreedToTerms, setAgreedToTerms] = useState(false);

  const validateForm = () => {
    const newErrors = {};
    
    if (!formData.name.trim()) {
      newErrors.name = 'Name is required';
    }
    
    if (!formData.email) {
      newErrors.email = 'Email is required';
    } else if (!isValidEmail(formData.email)) {
      newErrors.email = 'Invalid email format';
    }
    
    if (!formData.phone) {
      newErrors.phone = 'Phone number is required';
    } else if (!isValidPhone(formData.phone)) {
      newErrors.phone = 'Invalid phone number';
    }
    
    if (!formData.password) {
      newErrors.password = 'Password is required';
    } else if (!isValidPassword(formData.password)) {
      newErrors.password = 'Password must be at least 6 characters';
    }
    
    if (formData.password !== formData.confirmPassword) {
      newErrors.confirmPassword = 'Passwords do not match';
    }
    
    if (formData.role === 'operator' && !formData.company.trim()) {
      newErrors.company = 'Company name is required for operators';
    }

    if (!agreedToTerms) {
      newErrors.terms = 'You must agree to the terms';
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
      const { confirmPassword, ...userData } = formData;
      const response = await authAPI.register(userData);
      
      if (response.success) {
        login(response.user);
        const rolePath = {
          user: '/dashboard',
          operator: '/operator',
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

  const benefits = [
    { icon: MapPin, title: 'Find Stations', description: 'Locate charging points near you' },
    { icon: Battery, title: 'Smart Charging', description: 'Optimize your charging schedule' },
    { icon: CreditCard, title: 'Easy Payments', description: 'Seamless payment experience' },
  ];

  const getPasswordStrength = () => {
    const password = formData.password;
    if (!password) return { level: 0, text: '', color: '' };
    if (password.length < 6) return { level: 1, text: 'Weak', color: 'bg-red-500' };
    if (password.length < 8) return { level: 2, text: 'Fair', color: 'bg-yellow-500' };
    if (password.length >= 8 && /[A-Z]/.test(password) && /[0-9]/.test(password)) {
      return { level: 4, text: 'Strong', color: 'bg-green-500' };
    }
    return { level: 3, text: 'Good', color: 'bg-primary-500' };
  };

  const passwordStrength = getPasswordStrength();

  return (
    <div className="min-h-screen flex">
      {/* Left Panel - Form */}
      <div className="flex-1 flex items-center justify-center p-6 lg:p-12 bg-gradient-to-br from-secondary-50 to-white overflow-y-auto">
        <div className="w-full max-w-lg py-8">
          {/* Header */}
          <div className="mb-8">
            <Link to="/" className="inline-flex items-center gap-2 text-secondary-500 hover:text-primary-600 transition-colors mb-6 group">
              <ChevronRight className="w-4 h-4 rotate-180 group-hover:-translate-x-1 transition-transform" />
              Back to home
            </Link>
            
            <div className="flex items-center gap-3 mb-4 lg:hidden">
              <div className="w-12 h-12 bg-gradient-to-br from-primary-500 to-primary-600 rounded-xl flex items-center justify-center shadow-lg shadow-primary-500/30">
                <Zap className="w-7 h-7 text-white" />
              </div>
              <span className="text-2xl font-bold text-secondary-900">EVPulse</span>
            </div>
            
            <h1 className="text-3xl font-bold text-secondary-900 mb-2">Create your account</h1>
            <p className="text-secondary-500">Join thousands of EV owners and operators</p>
          </div>

          {/* Form Card */}
          <div className="bg-white rounded-3xl shadow-xl shadow-secondary-200/50 p-8 border border-secondary-100">
            {apiError && (
              <div className="mb-6 p-4 bg-red-50 border border-red-100 rounded-2xl text-red-600 text-sm flex items-center gap-3">
                <div className="w-8 h-8 bg-red-100 rounded-full flex items-center justify-center flex-shrink-0">
                  <span>⚠️</span>
                </div>
                {apiError}
              </div>
            )}

            <form onSubmit={handleSubmit} className="space-y-5">
              {/* Account Type Selection */}
              <div className="space-y-3">
                <label className="block text-sm font-semibold text-secondary-700">I am a...</label>
                <div className="grid grid-cols-2 gap-3">
                  <button
                    type="button"
                    onClick={() => handleChange({ target: { name: 'role', value: 'user' } })}
                    className={`p-4 rounded-2xl border-2 transition-all duration-200 text-left ${
                      formData.role === 'user'
                        ? 'border-primary-500 bg-primary-50 ring-4 ring-primary-500/10'
                        : 'border-secondary-200 hover:border-secondary-300 hover:bg-secondary-50'
                    }`}
                  >
                    <div className={`w-10 h-10 rounded-xl flex items-center justify-center mb-3 ${
                      formData.role === 'user' ? 'bg-primary-500 text-white' : 'bg-secondary-100 text-secondary-500'
                    }`}>
                      <User className="w-5 h-5" />
                    </div>
                    <p className={`font-semibold ${formData.role === 'user' ? 'text-primary-700' : 'text-secondary-900'}`}>
                      EV Owner
                    </p>
                    <p className="text-xs text-secondary-500 mt-1">Find & book stations</p>
                  </button>
                  
                  <button
                    type="button"
                    onClick={() => handleChange({ target: { name: 'role', value: 'operator' } })}
                    className={`p-4 rounded-2xl border-2 transition-all duration-200 text-left ${
                      formData.role === 'operator'
                        ? 'border-primary-500 bg-primary-50 ring-4 ring-primary-500/10'
                        : 'border-secondary-200 hover:border-secondary-300 hover:bg-secondary-50'
                    }`}
                  >
                    <div className={`w-10 h-10 rounded-xl flex items-center justify-center mb-3 ${
                      formData.role === 'operator' ? 'bg-primary-500 text-white' : 'bg-secondary-100 text-secondary-500'
                    }`}>
                      <Building2 className="w-5 h-5" />
                    </div>
                    <p className={`font-semibold ${formData.role === 'operator' ? 'text-primary-700' : 'text-secondary-900'}`}>
                      Operator
                    </p>
                    <p className="text-xs text-secondary-500 mt-1">Manage stations</p>
                  </button>
                </div>
              </div>

              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <Input
                  label="Full Name"
                  name="name"
                  placeholder="John Doe"
                  value={formData.name}
                  onChange={handleChange}
                  error={errors.name}
                  icon={User}
                />

                <Input
                  label="Phone Number"
                  name="phone"
                  placeholder="+1 (555) 000-0000"
                  value={formData.phone}
                  onChange={handleChange}
                  error={errors.phone}
                  icon={Phone}
                />
              </div>

              <Input
                label="Email Address"
                type="email"
                name="email"
                placeholder="john@example.com"
                value={formData.email}
                onChange={handleChange}
                error={errors.email}
                icon={Mail}
              />

              {formData.role === 'operator' && (
                <Input
                  label="Company Name"
                  name="company"
                  placeholder="Your company name"
                  value={formData.company}
                  onChange={handleChange}
                  error={errors.company}
                  icon={Building2}
                />
              )}

              <div className="space-y-4">
                <Input
                  label="Password"
                  type="password"
                  name="password"
                  placeholder="Create a strong password"
                  value={formData.password}
                  onChange={handleChange}
                  error={errors.password}
                  icon={Lock}
                />
                
                {formData.password && (
                  <div className="space-y-2">
                    <div className="flex gap-1">
                      {[1, 2, 3, 4].map((level) => (
                        <div
                          key={level}
                          className={`h-1.5 flex-1 rounded-full transition-all duration-300 ${
                            level <= passwordStrength.level ? passwordStrength.color : 'bg-secondary-200'
                          }`}
                        />
                      ))}
                    </div>
                    <p className={`text-xs font-medium ${
                      passwordStrength.level <= 1 ? 'text-red-500' :
                      passwordStrength.level === 2 ? 'text-yellow-600' :
                      passwordStrength.level === 3 ? 'text-primary-600' : 'text-green-600'
                    }`}>
                      {passwordStrength.text} password
                    </p>
                  </div>
                )}
              </div>

              <Input
                label="Confirm Password"
                type="password"
                name="confirmPassword"
                placeholder="Confirm your password"
                value={formData.confirmPassword}
                onChange={handleChange}
                error={errors.confirmPassword}
                icon={Lock}
              />

              <div className="flex items-start gap-3 p-4 bg-secondary-50 rounded-2xl">
                <div className="relative flex items-center">
                  <input 
                    type="checkbox" 
                    id="terms"
                    checked={agreedToTerms}
                    onChange={(e) => {
                      setAgreedToTerms(e.target.checked);
                      if (errors.terms) setErrors(prev => ({ ...prev, terms: '' }));
                    }}
                    className="w-5 h-5 rounded-md border-2 border-secondary-300 text-primary-500 focus:ring-primary-500 focus:ring-offset-0 cursor-pointer" 
                  />
                </div>
                <label htmlFor="terms" className="text-sm text-secondary-600 cursor-pointer leading-relaxed">
                  I agree to the{' '}
                  <Link to="/terms" className="text-primary-600 hover:text-primary-700 font-semibold underline underline-offset-2">
                    Terms of Service
                  </Link>{' '}
                  and{' '}
                  <Link to="/privacy" className="text-primary-600 hover:text-primary-700 font-semibold underline underline-offset-2">
                    Privacy Policy
                  </Link>
                </label>
              </div>
              {errors.terms && (
                <p className="text-red-500 text-sm -mt-3 ml-1">{errors.terms}</p>
              )}

              <Button type="submit" fullWidth loading={loading} className="h-12 text-base">
                Create Account
                <ArrowRight className="w-5 h-5 ml-2" />
              </Button>
            </form>

            <p className="text-center text-secondary-600 mt-6">
              Already have an account?{' '}
              <Link to="/login" className="text-primary-600 hover:text-primary-700 font-semibold transition-colors">
                Sign in
              </Link>
            </p>
          </div>
        </div>
      </div>

      {/* Right Panel - Branding */}
      <div className="hidden lg:flex lg:w-5/12 bg-gradient-to-br from-primary-600 via-primary-500 to-green-500 p-12 flex-col justify-between relative overflow-hidden">
        {/* Background Pattern */}
        <div className="absolute inset-0 opacity-10">
          <div className="absolute top-10 right-10 w-64 h-64 bg-white rounded-full blur-3xl" />
          <div className="absolute bottom-10 left-10 w-80 h-80 bg-white rounded-full blur-3xl" />
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
            <h2 className="text-3xl font-bold text-white mb-4">
              Start Your Electric<br />Journey Today
            </h2>
            <p className="text-white/70 text-lg">
              Create an account and unlock a world of convenient EV charging.
            </p>
          </div>
          
          <div className="space-y-4">
            {benefits.map((benefit, index) => (
              <div key={index} className="flex items-center gap-4 text-white/90 bg-white/10 backdrop-blur-sm rounded-2xl p-4">
                <div className="w-12 h-12 bg-white/20 rounded-xl flex items-center justify-center">
                  <benefit.icon className="w-6 h-6" />
                </div>
                <div>
                  <p className="font-semibold">{benefit.title}</p>
                  <p className="text-sm text-white/70">{benefit.description}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
        
        <div className="relative z-10 flex items-center gap-3">
          <div className="flex -space-x-2">
            {[1, 2, 3, 4].map((i) => (
              <div key={i} className="w-8 h-8 rounded-full bg-white/30 border-2 border-white/50 flex items-center justify-center text-xs text-white font-medium">
                {String.fromCharCode(64 + i)}
              </div>
            ))}
          </div>
          <p className="text-white/80 text-sm">
            <span className="font-semibold text-white">10,000+</span> users already joined
          </p>
        </div>
      </div>
    </div>
  );
};

export default Register;
