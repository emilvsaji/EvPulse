import { Link } from 'react-router-dom';
import { ArrowRight, Zap, TrendingUp, DollarSign, BarChart3, Wallet, Activity } from 'lucide-react';

const Landing = () => {
  return (
    <div className="min-h-screen flex flex-col bg-gradient-to-br from-green-900 via-green-800 to-green-900">
      {/* Navigation */}
      <nav className="bg-green-900/50 backdrop-blur-sm border-b border-green-700/30">
        <div className="max-w-7xl mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <Zap className="w-6 h-6 text-green-400" />
              <span className="text-xl font-bold text-white">ChargeEase</span>
            </div>
            <div className="hidden md:flex items-center gap-8">
              <a href="#home" className="text-white hover:text-green-400 transition-colors">Home</a>
              <a href="#features" className="text-white hover:text-green-400 transition-colors">Features</a>
              <a href="#dashboard" className="text-white hover:text-green-400 transition-colors">Dashboard</a>
              <a href="#contact" className="text-white hover:text-green-400 transition-colors">Contact</a>
            </div>
            <div className="flex items-center gap-4">
              <Link to="/login" className="text-white hover:text-green-400 transition-colors">
                Login
              </Link>
              <Link 
                to="/register" 
                className="bg-green-400 text-green-900 px-6 py-2 rounded-lg font-medium hover:bg-green-300 transition-colors"
              >
                Get Started
              </Link>
            </div>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="relative flex-1 flex flex-col justify-center overflow-hidden w-full">
        <div className="w-full px-0 sm:px-6 py-20 flex-1 flex flex-col justify-center">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
            {/* Left Content */}
            <div className="space-y-8">
              <div className="space-y-4">
                <h1 className="text-5xl lg:text-6xl font-bold text-white leading-tight">
                  Charge Smarter<br />
                  <span className="text-green-400">Drive Farther</span>
                </h1>
                <p className="text-lg text-green-100 max-w-xl">
                  Monitor, manage and optimize your EV charging stations with a unified SaaS platform built for efficiency and scale.
                </p>
              </div>
              <div className="flex items-center gap-4">
                <button className="bg-white text-green-900 px-8 py-3 rounded-lg font-medium hover:bg-green-50 transition-colors flex items-center gap-2">
                  Get Started for Free <ArrowRight className="w-5 h-5" />
                </button>
              </div>

              {/* Person Image Placeholder */}
              <div className="relative">
                <div className="absolute -left-10 top-0 w-64 h-80 bg-gradient-to-br from-green-600/30 to-green-800/30 rounded-3xl backdrop-blur-sm border border-green-500/20">
                  <div className="absolute inset-0 flex items-center justify-center">
                    <div className="text-center text-green-300">
                      <div className="w-32 h-32 mx-auto mb-4 bg-green-700/50 rounded-full flex items-center justify-center">
                        <Zap className="w-16 h-16" />
                      </div>
                      <p className="text-sm">EV User</p>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            {/* Right Content - Charging Station */}
            <div className="relative flex justify-center lg:justify-end">
              <div className="relative">
                {/* Charging Station Display */}
                <div className="w-80 h-[500px] bg-gradient-to-b from-gray-800 to-gray-900 rounded-3xl shadow-2xl border-8 border-white/10 p-6">
                  <div className="h-full flex flex-col">
                    {/* Screen Header */}
                    <div className="text-center mb-6">
                      <div className="inline-block bg-green-500 text-white px-4 py-1 rounded-full text-sm font-medium mb-2">
                        CHARGING
                      </div>
                      <div className="text-6xl font-bold text-white">80%</div>
                      <div className="text-gray-400 text-sm mt-2">Battery Level</div>
                    </div>

                    {/* Stats */}
                    <div className="space-y-3 mb-6">
                      <div className="bg-gray-700/50 rounded-lg p-3">
                        <div className="flex justify-between items-center">
                          <span className="text-gray-300 text-sm">Power</span>
                          <span className="text-white font-medium">7.2 kW</span>
                        </div>
                      </div>
                      <div className="bg-gray-700/50 rounded-lg p-3">
                        <div className="flex justify-between items-center">
                          <span className="text-gray-300 text-sm">Time Remaining</span>
                          <span className="text-white font-medium">45 min</span>
                        </div>
                      </div>
                      <div className="bg-gray-700/50 rounded-lg p-3">
                        <div className="flex justify-between items-center">
                          <span className="text-gray-300 text-sm">Cost</span>
                          <span className="text-green-400 font-medium">$8.50</span>
                        </div>
                      </div>
                    </div>

                    {/* Progress Bar */}
                    <div className="mt-auto">
                      <div className="h-2 bg-gray-700 rounded-full overflow-hidden mb-4">
                        <div className="h-full bg-green-500 rounded-full" style={{ width: '80%' }}></div>
                      </div>
                      <button className="w-full bg-red-500 text-white py-3 rounded-lg font-medium hover:bg-red-600 transition-colors">
                        Stop Charging
                      </button>
                    </div>
                  </div>
                </div>

                {/* Base */}
                <div className="absolute -bottom-8 left-1/2 transform -translate-x-1/2 w-40 h-40 bg-gradient-to-b from-gray-200 to-white rounded-full shadow-xl">
                  <div className="absolute inset-4 bg-gray-300 rounded-full flex items-center justify-center">
                    <div className="w-16 h-16 bg-gray-400 rounded-full"></div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section id="features" className="py-20 bg-white">
        <div className="max-w-7xl mx-auto px-6">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold text-gray-900 mb-4">
              Smarter Charging<br />
              <span className="text-green-600">Seamless</span> Experience
            </h2>
            <p className="text-gray-600 max-w-2xl mx-auto">
              Everything you need to monitor, manage, and optimize your EV charging ad from one intuitive dashboard.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            {/* Smart Load Balancing */}
            <div className="bg-white rounded-2xl shadow-lg p-8 border border-gray-100 hover:shadow-xl transition-shadow">
              <div className="mb-6">
                <div className="relative h-48 flex items-center justify-center">
                  <svg className="w-full h-full" viewBox="0 0 400 200">
                    {/* Flow diagram */}
                    <rect x="50" y="80" width="60" height="40" rx="8" fill="#10b981" />
                    <text x="80" y="105" textAnchor="middle" fill="white" fontSize="12" fontWeight="bold">A</text>
                    
                    <rect x="280" y="20" width="60" height="40" rx="8" fill="#10b981" />
                    <text x="310" y="45" textAnchor="middle" fill="white" fontSize="12" fontWeight="bold">MAX</text>
                    
                    <rect x="280" y="80" width="60" height="40" rx="8" fill="#059669" />
                    <text x="310" y="105" textAnchor="middle" fill="white" fontSize="12" fontWeight="bold">48 kW</text>
                    
                    <rect x="280" y="140" width="60" height="40" rx="8" fill="#10b981" />
                    <text x="310" y="165" textAnchor="middle" fill="white" fontSize="12" fontWeight="bold">STOP</text>

                    {/* Center node */}
                    <circle cx="200" cy="100" r="30" fill="#059669" />
                    <text x="200" y="105" textAnchor="middle" fill="white" fontSize="14" fontWeight="bold">48 kW</text>

                    {/* Connecting lines */}
                    <path d="M 110 100 L 170 100" stroke="#10b981" strokeWidth="3" fill="none" markerEnd="url(#arrowhead)" />
                    <path d="M 230 100 L 280 40" stroke="#10b981" strokeWidth="3" fill="none" markerEnd="url(#arrowhead)" />
                    <path d="M 230 100 L 280 100" stroke="#10b981" strokeWidth="3" fill="none" markerEnd="url(#arrowhead)" />
                    <path d="M 230 100 L 280 160" stroke="#10b981" strokeWidth="3" fill="none" markerEnd="url(#arrowhead)" />

                    <defs>
                      <marker id="arrowhead" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
                        <polygon points="0 0, 10 3, 0 6" fill="#10b981" />
                      </marker>
                    </defs>
                  </svg>
                  
                  {/* Legend */}
                  <div className="absolute bottom-0 left-0 flex items-center gap-4 text-xs">
                    <div className="flex items-center gap-2">
                      <div className="w-3 h-3 rounded-full bg-green-500"></div>
                      <span className="text-gray-600">50% Tracked</span>
                    </div>
                    <div className="flex items-center gap-2">
                      <div className="w-3 h-3 rounded-full bg-red-500"></div>
                      <span className="text-gray-600">50% Negated</span>
                    </div>
                  </div>
                </div>
              </div>
              <h3 className="text-2xl font-bold text-gray-900 mb-3">Smart Load Balancing</h3>
              <p className="text-gray-600">
                Manages power across all charging points to prevent grid overload and lower peak-time energy costs efficiently.
              </p>
            </div>

            {/* Centralized Billing */}
            <div className="bg-white rounded-2xl shadow-lg p-8 border border-gray-100 hover:shadow-xl transition-shadow">
              <div className="mb-6">
                <div className="relative h-48">
                  <div className="absolute inset-0 flex items-center justify-center">
                    <div className="relative w-48 h-48">
                      {/* Center circle */}
                      <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-32 h-32 rounded-full bg-green-100 flex items-center justify-center z-10">
                        <div className="text-center">
                          <DollarSign className="w-8 h-8 text-green-600 mx-auto mb-1" />
                          <div className="text-sm font-semibold text-gray-900">Centralized EV</div>
                          <div className="text-sm font-semibold text-gray-900">Billing System</div>
                        </div>
                      </div>

                      {/* Orbiting elements */}
                      <div className="absolute top-0 left-1/2 transform -translate-x-1/2 -translate-y-1/2">
                        <div className="bg-green-500 text-white px-3 py-1 rounded-lg text-xs font-medium whitespace-nowrap">
                          <Activity className="w-4 h-4 inline mr-1" />
                          Regulatory Compliance Monitoring
                        </div>
                      </div>
                      <div className="absolute right-0 top-1/2 transform translate-x-1/2 -translate-y-1/2">
                        <div className="bg-green-500 text-white px-3 py-1 rounded-lg text-xs font-medium whitespace-nowrap">
                          <BarChart3 className="w-4 h-4 inline mr-1" />
                          Revenue Simulation
                        </div>
                      </div>
                      <div className="absolute bottom-0 right-1/4 transform translate-y-1/2">
                        <div className="bg-green-500 text-white px-3 py-1 rounded-lg text-xs font-medium whitespace-nowrap">
                          <TrendingUp className="w-4 h-4 inline mr-1" />
                          Energy Pricing
                        </div>
                      </div>
                      <div className="absolute bottom-0 left-1/4 transform translate-y-1/2">
                        <div className="bg-green-500 text-white px-3 py-1 rounded-lg text-xs font-medium whitespace-nowrap">
                          <Wallet className="w-4 h-4 inline mr-1" />
                          Improved User Experience
                        </div>
                      </div>
                      <div className="absolute left-0 top-1/2 transform -translate-x-1/2 -translate-y-1/2">
                        <div className="bg-green-500 text-white px-3 py-1 rounded-lg text-xs font-medium whitespace-nowrap">
                          <Activity className="w-4 h-4 inline mr-1" />
                          Future-Ready Infrastructure
                        </div>
                      </div>

                      {/* Connection lines */}
                      <svg className="absolute inset-0 w-full h-full pointer-events-none">
                        <line x1="50%" y1="0" x2="50%" y2="30%" stroke="#10b981" strokeWidth="1" strokeDasharray="3,3" />
                        <line x1="100%" y1="50%" x2="70%" y2="50%" stroke="#10b981" strokeWidth="1" strokeDasharray="3,3" />
                        <line x1="75%" y1="100%" x2="60%" y2="75%" stroke="#10b981" strokeWidth="1" strokeDasharray="3,3" />
                        <line x1="25%" y1="100%" x2="40%" y2="75%" stroke="#10b981" strokeWidth="1" strokeDasharray="3,3" />
                        <line x1="0" y1="50%" x2="30%" y2="50%" stroke="#10b981" strokeWidth="1" strokeDasharray="3,3" />
                      </svg>
                    </div>
                  </div>
                </div>
              </div>
              <h3 className="text-2xl font-bold text-gray-900 mb-3">Centralized Billing</h3>
              <p className="text-gray-600">
                Offers flexible tariffs and automated invoices, making payment management simple for both operators and users.
              </p>
            </div>

            {/* Energy Efficiency Chart */}
            <div className="bg-white rounded-2xl shadow-lg p-8 border border-gray-100 hover:shadow-xl transition-shadow">
              <div className="mb-6">
                <div className="relative h-48">
                  <svg viewBox="0 0 400 180" className="w-full h-full">
                    {/* Grid lines */}
                    <line x1="40" y1="150" x2="360" y2="150" stroke="#e5e7eb" strokeWidth="1" />
                    <line x1="40" y1="110" x2="360" y2="110" stroke="#e5e7eb" strokeWidth="1" />
                    <line x1="40" y1="70" x2="360" y2="70" stroke="#e5e7eb" strokeWidth="1" />
                    <line x1="40" y1="30" x2="360" y2="30" stroke="#e5e7eb" strokeWidth="1" />

                    {/* Area gradient */}
                    <defs>
                      <linearGradient id="areaGradient" x1="0%" y1="0%" x2="0%" y2="100%">
                        <stop offset="0%" stopColor="#10b981" stopOpacity="0.3" />
                        <stop offset="100%" stopColor="#10b981" stopOpacity="0.05" />
                      </linearGradient>
                    </defs>

                    {/* Area path */}
                    <path
                      d="M 40 140 L 100 130 L 160 115 L 220 105 L 280 95 L 340 85 L 360 80 L 360 150 L 40 150 Z"
                      fill="url(#areaGradient)"
                    />

                    {/* Line */}
                    <path
                      d="M 40 140 L 100 130 L 160 115 L 220 105 L 280 95 L 340 85 L 360 80"
                      fill="none"
                      stroke="#10b981"
                      strokeWidth="3"
                    />

                    {/* Y-axis label */}
                    <text x="10" y="155" fontSize="10" fill="#6b7280">Charging station status</text>
                  </svg>
                  
                  {/* Legend */}
                  <div className="absolute bottom-0 left-0 flex items-center gap-4 text-xs">
                    <div className="flex items-center gap-2">
                      <div className="w-3 h-3 rounded-full bg-green-500"></div>
                      <span className="text-gray-600">50% Tracked</span>
                    </div>
                    <div className="flex items-center gap-2">
                      <div className="w-3 h-3 rounded-full bg-red-500"></div>
                      <span className="text-gray-600">50% Negated</span>
                    </div>
                  </div>
                </div>
              </div>
              <h3 className="text-2xl font-bold text-gray-900 mb-3">Energy Efficiency</h3>
              <p className="text-gray-600">
                Track real-time energy consumption and optimize charging schedules for maximum efficiency.
              </p>
            </div>

            {/* Revenue Integration */}
            <div className="bg-white rounded-2xl shadow-lg p-8 border border-gray-100 hover:shadow-xl transition-shadow">
              <div className="mb-6">
                <div className="relative h-48 flex items-center justify-center">
                  <div className="grid grid-cols-3 gap-4">
                    {/* Payment icons */}
                    <div className="w-20 h-16 bg-gradient-to-br from-green-100 to-green-50 rounded-lg flex items-center justify-center border border-green-200 opacity-40">
                      <Wallet className="w-8 h-8 text-green-600" />
                    </div>
                    <div className="w-20 h-16 bg-gradient-to-br from-green-100 to-green-50 rounded-lg flex items-center justify-center border border-green-200 opacity-40">
                      <DollarSign className="w-8 h-8 text-green-600" />
                    </div>
                    <div className="w-20 h-16 bg-gradient-to-br from-green-100 to-green-50 rounded-lg flex items-center justify-center border border-green-200 opacity-40">
                      <BarChart3 className="w-8 h-8 text-green-600" />
                    </div>
                    <div className="w-20 h-16 bg-gradient-to-br from-green-500 to-green-600 rounded-lg flex items-center justify-center border-2 border-green-700 shadow-lg col-start-2">
                      <Zap className="w-10 h-10 text-white" />
                    </div>
                  </div>
                </div>
              </div>
              <h3 className="text-2xl font-bold text-gray-900 mb-3">Revenue Integration</h3>
              <p className="text-gray-600">
                Seamless payment integration with detailed analytics to track and optimize your revenue streams.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-green-950 text-white py-12">
        <div className="max-w-7xl mx-auto px-6">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
            <div>
              <div className="flex items-center gap-2 mb-4">
                <Zap className="w-6 h-6 text-green-400" />
                <span className="text-xl font-bold">ChargeEase</span>
              </div>
              <p className="text-green-200 text-sm">
                The complete EV charging management platform for the future.
              </p>
            </div>
            <div>
              <h4 className="font-semibold mb-4">Product</h4>
              <ul className="space-y-2 text-sm text-green-200">
                <li><a href="#" className="hover:text-green-400 transition-colors">Features</a></li>
                <li><a href="#" className="hover:text-green-400 transition-colors">Pricing</a></li>
                <li><a href="#" className="hover:text-green-400 transition-colors">Dashboard</a></li>
              </ul>
            </div>
            <div>
              <h4 className="font-semibold mb-4">Company</h4>
              <ul className="space-y-2 text-sm text-green-200">
                <li><a href="#" className="hover:text-green-400 transition-colors">About</a></li>
                <li><a href="#" className="hover:text-green-400 transition-colors">Blog</a></li>
                <li><a href="#" className="hover:text-green-400 transition-colors">Careers</a></li>
              </ul>
            </div>
            <div>
              <h4 className="font-semibold mb-4">Support</h4>
              <ul className="space-y-2 text-sm text-green-200">
                <li><a href="#" className="hover:text-green-400 transition-colors">Help Center</a></li>
                <li><a href="#" className="hover:text-green-400 transition-colors">Contact</a></li>
                <li><a href="#" className="hover:text-green-400 transition-colors">Privacy</a></li>
              </ul>
            </div>
          </div>
          <div className="border-t border-green-800 mt-8 pt-8 text-center text-sm text-green-200">
            © 2026 ChargeEase. All rights reserved.
          </div>
        </div>
      </footer>
    </div>
  );
};

export default Landing;
