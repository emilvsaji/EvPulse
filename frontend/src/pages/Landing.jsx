import { Link } from 'react-router-dom';
import { ArrowRight, Zap, Battery, Clock, DollarSign, Activity, TrendingUp, Wallet, BarChart3, Globe, Settings, Shield } from 'lucide-react';

const Landing = () => {
  return (
    <div className="min-h-screen flex flex-col bg-white">
      {/* Navigation */}
      <nav className="w-full bg-green-900 py-4 px-6">
        <div className="max-w-7xl mx-auto flex items-center justify-between">
          {/* Logo */}
          <div className="flex items-center gap-2">
            <Zap className="w-6 h-6 text-green-400" />
            <span className="text-xl font-bold text-white">EvPulse</span>
          </div>

          {/* Center Navigation Links */}
          <div className="hidden md:flex items-center bg-green-800/50 rounded-full px-2 py-1">
            <a href="#home" className="text-white hover:text-green-400 transition-colors px-4 py-2 rounded-full text-sm font-medium">Home</a>
            <a href="#features" className="text-white hover:text-green-400 transition-colors px-4 py-2 rounded-full text-sm font-medium">Features</a>
            <a href="#dashboard" className="text-white hover:text-green-400 transition-colors px-4 py-2 rounded-full text-sm font-medium">Dashboard</a>
            <a href="#contact" className="text-white hover:text-green-400 transition-colors px-4 py-2 rounded-full text-sm font-medium">Contact</a>
          </div>

          {/* Right Side - Login & Get Started */}
          <div className="flex items-center gap-4">
            <Link to="/login" className="text-white hover:text-green-400 transition-colors text-sm font-medium">
              Login
            </Link>
            <Link 
              to="/register" 
              className="bg-green-400 text-green-900 px-5 py-2 rounded-full text-sm font-semibold hover:bg-green-300 transition-colors"
            >
              Get Started
            </Link>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <section id="home" className="relative bg-green-900 overflow-hidden">
        {/* Background Pattern */}
        <div className="absolute inset-0 opacity-10">
          <div className="absolute top-20 left-10 w-64 h-64 bg-green-400 rounded-full blur-3xl"></div>
          <div className="absolute bottom-20 right-10 w-96 h-96 bg-green-400 rounded-full blur-3xl"></div>
        </div>

        <div className="max-w-7xl mx-auto px-6 py-16 lg:py-20">
          <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-center">
            {/* Left - Person Image */}
            <div className="lg:col-span-4 relative hidden lg:block">
              <div className="relative">
                {/* Person placeholder with EV charging */}
                <div className="w-full h-[450px] bg-gradient-to-br from-green-700/30 to-green-900/30 rounded-3xl overflow-hidden relative">
                  <div className="absolute inset-0 flex items-end justify-center">
                    <div className="w-full h-full bg-gradient-to-t from-green-800/50 to-transparent absolute bottom-0"></div>
                    {/* Stylized person silhouette */}
                    <div className="relative z-10 mb-8">
                      <div className="w-32 h-32 bg-green-600/40 rounded-full mx-auto mb-4"></div>
                      <div className="w-48 h-64 bg-green-600/30 rounded-t-full mx-auto"></div>
                    </div>
                  </div>
                  {/* EV Car representation */}
                  <div className="absolute bottom-8 right-4 bg-white/10 backdrop-blur-sm rounded-xl p-3">
                    <Battery className="w-8 h-8 text-green-400" />
                  </div>
                </div>
              </div>
            </div>

            {/* Center - Text Content */}
            <div className="lg:col-span-4 text-center lg:text-left z-10">
              <h1 className="text-4xl lg:text-5xl font-bold text-white leading-tight mb-6">
                Charge Smarter
                <br />
                <span className="text-green-400 italic">Drive Farther</span>
              </h1>
              <p className="text-green-100 text-base mb-8 max-w-md mx-auto lg:mx-0">
                Monitor, manage and optimize your EV charging stations with a unified SaaS platform built for efficiency and scale.
              </p>
              <Link 
                to="/register"
                className="inline-flex items-center gap-2 bg-white text-green-900 px-6 py-3 rounded-lg font-semibold hover:bg-green-50 transition-colors"
              >
                Get Started for Free
                <ArrowRight className="w-5 h-5" />
              </Link>
            </div>

            {/* Right - Charging Station Display */}
            <div className="lg:col-span-4 flex justify-center lg:justify-end">
              <div className="relative">
                {/* Charging Station */}
                <div className="w-64 bg-gradient-to-b from-gray-100 to-white rounded-3xl shadow-2xl overflow-hidden border-4 border-gray-200">
                  {/* Station Top */}
                  <div className="bg-gray-800 p-4 rounded-t-2xl">
                    <div className="text-center">
                      <span className="text-green-400 text-xs font-semibold tracking-wider">⚡CHARGING</span>
                    </div>
                  </div>

                  {/* Screen */}
                  <div className="bg-gray-900 mx-4 mt-2 rounded-xl p-4">
                    <div className="text-center mb-4">
                      <div className="text-5xl font-bold text-white">60%</div>
                      <div className="text-gray-400 text-xs mt-1">Battery Level</div>
                    </div>

                    {/* Progress Bar */}
                    <div className="h-2 bg-gray-700 rounded-full overflow-hidden mb-4">
                      <div className="h-full bg-green-500 rounded-full transition-all" style={{ width: '60%' }}></div>
                    </div>

                    {/* Stats */}
                    <div className="space-y-2">
                      <div className="flex justify-between items-center text-sm">
                        <span className="text-gray-400">Power</span>
                        <span className="text-white font-medium">7.2 kW</span>
                      </div>
                      <div className="flex justify-between items-center text-sm">
                        <span className="text-gray-400">Time Left</span>
                        <span className="text-white font-medium">45 min</span>
                      </div>
                      <div className="flex justify-between items-center text-sm">
                        <span className="text-gray-400">Cost</span>
                        <span className="text-green-400 font-medium">₹8.50</span>
                      </div>
                    </div>
                  </div>

                  {/* Station Body */}
                  <div className="p-4 space-y-3">
                    <div className="h-4 bg-gray-200 rounded"></div>
                    <div className="flex gap-2">
                      <div className="h-8 w-8 bg-green-500 rounded-full flex items-center justify-center">
                        <Zap className="w-4 h-4 text-white" />
                      </div>
                      <div className="h-8 flex-1 bg-gray-100 rounded"></div>
                    </div>
                  </div>
                </div>

                {/* Station Base */}
                <div className="w-32 h-8 bg-gradient-to-b from-gray-300 to-gray-400 rounded-b-xl mx-auto -mt-1 shadow-lg"></div>
                <div className="w-40 h-4 bg-gray-200 rounded-full mx-auto mt-2 shadow-inner"></div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section id="features" className="py-20 bg-gray-50">
        <div className="max-w-7xl mx-auto px-6">
          {/* Section Header */}
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold text-gray-900 mb-4">
              Smarter Charging
              <br />
              <span className="text-green-600">Seamless</span> Experience
            </h2>
            <p className="text-gray-600 max-w-2xl mx-auto">
              Everything you need to monitor, manage, and optimize your EV charging all from one intuitive dashboard.
            </p>
          </div>

          {/* Feature Cards Grid */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            {/* Smart Load Balancing */}
            <div className="bg-white rounded-2xl shadow-sm p-8 border border-gray-100 hover:shadow-lg transition-shadow">
              <div className="mb-6">
                <div className="relative h-48 flex items-center justify-center bg-gray-50 rounded-xl">
                  <svg className="w-full h-full p-4" viewBox="0 0 400 180">
                    {/* Source Node */}
                    <rect x="20" y="70" width="50" height="40" rx="6" fill="#10b981" />
                    <text x="45" y="95" textAnchor="middle" fill="white" fontSize="14" fontWeight="bold">A</text>
                    
                    {/* Center Distribution Node */}
                    <circle cx="180" cy="90" r="35" fill="#059669" />
                    <text x="180" y="85" textAnchor="middle" fill="white" fontSize="12" fontWeight="bold">32 kW</text>
                    <text x="180" y="100" textAnchor="middle" fill="white" fontSize="10">Total</text>

                    {/* Output Nodes */}
                    <rect x="300" y="20" width="70" height="35" rx="6" fill="#10b981" />
                    <text x="335" y="43" textAnchor="middle" fill="white" fontSize="11" fontWeight="bold">7 kW</text>
                    
                    <rect x="300" y="72" width="70" height="35" rx="6" fill="#059669" />
                    <text x="335" y="95" textAnchor="middle" fill="white" fontSize="11" fontWeight="bold">10 kW</text>
                    
                    <rect x="300" y="125" width="70" height="35" rx="6" fill="#10b981" />
                    <text x="335" y="148" textAnchor="middle" fill="white" fontSize="11" fontWeight="bold">15 kW</text>

                    {/* Connecting Lines */}
                    <path d="M 70 90 Q 120 90 145 90" stroke="#10b981" strokeWidth="2" fill="none" strokeDasharray="5,5" />
                    <path d="M 215 90 Q 250 50 300 38" stroke="#10b981" strokeWidth="2" fill="none" strokeDasharray="5,5" />
                    <path d="M 215 90 L 300 90" stroke="#059669" strokeWidth="2" fill="none" strokeDasharray="5,5" />
                    <path d="M 215 90 Q 250 130 300 142" stroke="#10b981" strokeWidth="2" fill="none" strokeDasharray="5,5" />

                    {/* Arrow markers */}
                    <circle cx="145" cy="90" r="4" fill="#10b981" />
                    <circle cx="295" cy="38" r="4" fill="#10b981" />
                    <circle cx="295" cy="90" r="4" fill="#059669" />
                    <circle cx="295" cy="142" r="4" fill="#10b981" />
                  </svg>
                </div>
              </div>
              <h3 className="text-xl font-bold text-gray-900 mb-3">Smart Load Balancing</h3>
              <p className="text-gray-600 text-sm">
                Manages power across all charging points to prevent grid overload and lower peak-time energy costs efficiently.
              </p>
            </div>

            {/* Centralized Billing */}
            <div className="bg-white rounded-2xl shadow-sm p-8 border border-gray-100 hover:shadow-lg transition-shadow">
              <div className="mb-6">
                <div className="relative h-48 flex items-center justify-center bg-gray-50 rounded-xl overflow-hidden">
                  {/* Center Circle */}
                  <div className="relative">
                    <div className="w-28 h-28 rounded-full bg-green-100 flex items-center justify-center border-2 border-green-200">
                      <div className="text-center">
                        <div className="text-xs font-semibold text-gray-900">Centralized EV</div>
                        <div className="text-xs font-semibold text-gray-900">Billing System</div>
                      </div>
                    </div>

                    {/* Orbiting Labels */}
                    <div className="absolute -top-8 left-1/2 transform -translate-x-1/2">
                      <div className="bg-green-500 text-white px-2 py-1 rounded text-[10px] font-medium whitespace-nowrap">
                        Regulatory Compliance Ready
                      </div>
                    </div>
                    <div className="absolute top-1/2 -right-24 transform -translate-y-1/2">
                      <div className="bg-green-500 text-white px-2 py-1 rounded text-[10px] font-medium whitespace-nowrap">
                        Scalable Monetization
                      </div>
                    </div>
                    <div className="absolute -bottom-8 right-0">
                      <div className="bg-green-500 text-white px-2 py-1 rounded text-[10px] font-medium whitespace-nowrap">
                        Faster Error-Free Invoicing
                      </div>
                    </div>
                    <div className="absolute -bottom-8 left-0">
                      <div className="bg-green-500 text-white px-2 py-1 rounded text-[10px] font-medium whitespace-nowrap">
                        Improved User Experience
                      </div>
                    </div>
                    <div className="absolute top-1/2 -left-24 transform -translate-y-1/2">
                      <div className="bg-green-500 text-white px-2 py-1 rounded text-[10px] font-medium whitespace-nowrap">
                        Future-Ready Infrastructure
                      </div>
                    </div>
                  </div>
                </div>
              </div>
              <h3 className="text-xl font-bold text-gray-900 mb-3">Centralized Billing</h3>
              <p className="text-gray-600 text-sm">
                Offers flexible tariffs and automated invoices, making payment management simple for both operators and users.
              </p>
            </div>

            {/* Energy Efficiency */}
            <div className="bg-white rounded-2xl shadow-sm p-8 border border-gray-100 hover:shadow-lg transition-shadow">
              <div className="mb-6">
                <div className="relative h-48 bg-gray-50 rounded-xl p-4">
                  {/* Legend */}
                  <div className="flex items-center gap-4 mb-4 text-xs">
                    <div className="flex items-center gap-1">
                      <div className="w-2 h-2 rounded-full bg-green-500"></div>
                      <span className="text-gray-600">50% Positive</span>
                    </div>
                    <div className="flex items-center gap-1">
                      <div className="w-2 h-2 rounded-full bg-red-400"></div>
                      <span className="text-gray-600">10% Negative</span>
                    </div>
                  </div>

                  {/* Chart */}
                  <svg viewBox="0 0 350 120" className="w-full h-28">
                    <defs>
                      <linearGradient id="chartGradient" x1="0%" y1="0%" x2="0%" y2="100%">
                        <stop offset="0%" stopColor="#10b981" stopOpacity="0.3" />
                        <stop offset="100%" stopColor="#10b981" stopOpacity="0.05" />
                      </linearGradient>
                    </defs>

                    {/* Grid lines */}
                    <line x1="0" y1="100" x2="350" y2="100" stroke="#e5e7eb" strokeWidth="1" />
                    <line x1="0" y1="70" x2="350" y2="70" stroke="#e5e7eb" strokeWidth="1" strokeDasharray="4,4" />
                    <line x1="0" y1="40" x2="350" y2="40" stroke="#e5e7eb" strokeWidth="1" strokeDasharray="4,4" />

                    {/* Area */}
                    <path
                      d="M 0 90 Q 50 85 100 75 T 200 55 T 300 35 L 350 30 L 350 100 L 0 100 Z"
                      fill="url(#chartGradient)"
                    />

                    {/* Line */}
                    <path
                      d="M 0 90 Q 50 85 100 75 T 200 55 T 300 35 L 350 30"
                      fill="none"
                      stroke="#10b981"
                      strokeWidth="2"
                    />

                    {/* Data points */}
                    <circle cx="100" cy="75" r="3" fill="#10b981" />
                    <circle cx="200" cy="55" r="3" fill="#10b981" />
                    <circle cx="300" cy="35" r="3" fill="#10b981" />
                  </svg>

                  {/* Y-axis label */}
                  <div className="text-[10px] text-gray-500 mt-1">Charging station status</div>
                </div>
              </div>
              <h3 className="text-xl font-bold text-gray-900 mb-3">Energy Efficiency</h3>
              <p className="text-gray-600 text-sm">
                Track real-time energy consumption and optimize charging schedules for maximum efficiency.
              </p>
            </div>

            {/* Revenue Integration */}
            <div className="bg-white rounded-2xl shadow-sm p-8 border border-gray-100 hover:shadow-lg transition-shadow">
              <div className="mb-6">
                <div className="relative h-48 bg-gray-50 rounded-xl flex items-center justify-center">
                  {/* Platform Headers */}
                  <div className="absolute top-4 left-1/2 transform -translate-x-1/2 flex gap-6 text-[10px] text-gray-500 font-medium">
                    <span>Smart Platforms</span>
                    <span>IoT Platforms</span>
                    <span>Energy Manager</span>
                  </div>

                  {/* Icons Grid */}
                  <div className="grid grid-cols-3 gap-4 mt-4">
                    <div className="w-16 h-14 bg-green-100/50 rounded-lg flex items-center justify-center border border-green-200/50">
                      <Globe className="w-6 h-6 text-green-600/50" />
                    </div>
                    <div className="w-16 h-14 bg-green-100/50 rounded-lg flex items-center justify-center border border-green-200/50">
                      <Settings className="w-6 h-6 text-green-600/50" />
                    </div>
                    <div className="w-16 h-14 bg-green-100/50 rounded-lg flex items-center justify-center border border-green-200/50">
                      <Activity className="w-6 h-6 text-green-600/50" />
                    </div>
                    <div className="col-span-3 flex justify-center">
                      <div className="w-16 h-14 bg-green-500 rounded-lg flex items-center justify-center shadow-lg">
                        <Zap className="w-8 h-8 text-white" />
                      </div>
                    </div>
                  </div>
                </div>
              </div>
              <h3 className="text-xl font-bold text-gray-900 mb-3">Revenue Integration</h3>
              <p className="text-gray-600 text-sm">
                Seamless payment integration with detailed analytics to track and optimize your revenue streams.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="w-full bg-green-950 text-white py-12">
        <div className="max-w-7xl mx-auto px-6">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
            {/* Logo & Description */}
            <div>
              <div className="flex items-center gap-2 mb-4">
                <Zap className="w-6 h-6 text-green-400" />
                <span className="text-xl font-bold">EvPulse</span>
              </div>
              <p className="text-green-200 text-sm">
                The complete EV charging management platform for the future.
              </p>
            </div>

            {/* Product Links */}
            <div>
              <h4 className="font-semibold mb-4">Product</h4>
              <ul className="space-y-2 text-sm text-green-200">
                <li><a href="#features" className="hover:text-green-400 transition-colors">Features</a></li>
                <li><a href="#" className="hover:text-green-400 transition-colors">Pricing</a></li>
                <li><a href="#dashboard" className="hover:text-green-400 transition-colors">Dashboard</a></li>
              </ul>
            </div>

            {/* Company Links */}
            <div>
              <h4 className="font-semibold mb-4">Company</h4>
              <ul className="space-y-2 text-sm text-green-200">
                <li><a href="#" className="hover:text-green-400 transition-colors">About</a></li>
                <li><a href="#" className="hover:text-green-400 transition-colors">Blog</a></li>
                <li><a href="#" className="hover:text-green-400 transition-colors">Careers</a></li>
              </ul>
            </div>

            {/* Support Links */}
            <div>
              <h4 className="font-semibold mb-4">Support</h4>
              <ul className="space-y-2 text-sm text-green-200">
                <li><a href="#" className="hover:text-green-400 transition-colors">Help Center</a></li>
                <li><a href="#contact" className="hover:text-green-400 transition-colors">Contact</a></li>
                <li><a href="#" className="hover:text-green-400 transition-colors">Privacy</a></li>
              </ul>
            </div>
          </div>

          {/* Copyright */}
          <div className="border-t border-green-800 mt-8 pt-8 text-center text-sm text-green-200">
            © 2026 EvPulse. All rights reserved.
          </div>
        </div>
      </footer>
    </div>
  );
};

export default Landing;
