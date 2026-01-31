import { Eye, EyeOff, AlertCircle } from 'lucide-react';
import { useState } from 'react';

const Input = ({
  label,
  type = 'text',
  error,
  icon: Icon,
  hint,
  className = '',
  ...props
}) => {
  const [showPassword, setShowPassword] = useState(false);
  const [focused, setFocused] = useState(false);
  const isPassword = type === 'password';

  return (
    <div className={className}>
      {label && (
        <label className="block text-sm font-semibold text-secondary-700 mb-2">
          {label}
        </label>
      )}
      <div className="relative group">
        {Icon && (
          <div className={`absolute left-4 top-1/2 -translate-y-1/2 transition-colors duration-200 ${
            focused ? 'text-primary-500' : error ? 'text-red-400' : 'text-secondary-400'
          }`}>
            <Icon className="w-5 h-5" />
          </div>
        )}
        <input
          type={isPassword ? (showPassword ? 'text' : 'password') : type}
          onFocus={() => setFocused(true)}
          onBlur={() => setFocused(false)}
          className={`
            w-full px-4 py-3 bg-white border-2 rounded-xl outline-none transition-all duration-200
            placeholder:text-secondary-400
            ${Icon ? 'pl-12' : ''} 
            ${isPassword ? 'pr-12' : ''} 
            ${error 
              ? 'border-red-300 focus:border-red-500 focus:ring-4 focus:ring-red-500/10 bg-red-50/30' 
              : 'border-secondary-200 hover:border-secondary-300 focus:border-primary-500 focus:ring-4 focus:ring-primary-500/10'
            }
          `}
          {...props}
        />
        {isPassword && (
          <button
            type="button"
            onClick={() => setShowPassword(!showPassword)}
            className="absolute right-4 top-1/2 -translate-y-1/2 text-secondary-400 hover:text-secondary-600 transition-colors p-1 rounded-lg hover:bg-secondary-100"
          >
            {showPassword ? <EyeOff className="w-5 h-5" /> : <Eye className="w-5 h-5" />}
          </button>
        )}
      </div>
      {error && (
        <div className="mt-2 flex items-center gap-1.5 text-red-500">
          <AlertCircle className="w-4 h-4 flex-shrink-0" />
          <p className="text-sm">{error}</p>
        </div>
      )}
      {hint && !error && (
        <p className="mt-2 text-sm text-secondary-500">{hint}</p>
      )}
    </div>
  );
};

export default Input;
