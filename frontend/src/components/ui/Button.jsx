const Button = ({ 
  children, 
  variant = 'primary', 
  size = 'md', 
  icon: Icon,
  iconPosition = 'left',
  fullWidth = false,
  loading = false,
  disabled = false,
  className = '',
  ...props 
}) => {
  const variants = {
    primary: 'bg-gradient-to-r from-primary-500 to-primary-600 hover:from-primary-600 hover:to-primary-700 text-white shadow-lg shadow-primary-500/25 hover:shadow-xl hover:shadow-primary-500/30 active:shadow-md',
    secondary: 'bg-secondary-100 hover:bg-secondary-200 text-secondary-900 shadow-sm hover:shadow-md',
    outline: 'border-2 border-secondary-200 hover:border-primary-500 hover:bg-primary-50 text-secondary-700 hover:text-primary-700',
    ghost: 'hover:bg-secondary-100 text-secondary-700 hover:text-secondary-900',
    danger: 'bg-gradient-to-r from-red-500 to-red-600 hover:from-red-600 hover:to-red-700 text-white shadow-lg shadow-red-500/25',
    success: 'bg-gradient-to-r from-green-500 to-green-600 hover:from-green-600 hover:to-green-700 text-white shadow-lg shadow-green-500/25',
  };

  const sizes = {
    xs: 'py-1.5 px-3 text-xs',
    sm: 'py-2 px-4 text-sm',
    md: 'py-2.5 px-5 text-sm',
    lg: 'py-3 px-6 text-base',
    xl: 'py-4 px-8 text-lg',
  };

  return (
    <button
      disabled={disabled || loading}
      className={`
        inline-flex items-center justify-center gap-2 font-semibold rounded-xl transition-all duration-200 transform
        ${variants[variant]}
        ${sizes[size]}
        ${fullWidth ? 'w-full' : ''}
        ${disabled || loading ? 'opacity-60 cursor-not-allowed scale-100' : 'hover:scale-[1.02] active:scale-[0.98]'}
        ${className}
      `}
      {...props}
    >
      {loading ? (
        <svg className="animate-spin w-5 h-5" viewBox="0 0 24 24">
          <circle
            className="opacity-25"
            cx="12"
            cy="12"
            r="10"
            stroke="currentColor"
            strokeWidth="4"
            fill="none"
          />
          <path
            className="opacity-75"
            fill="currentColor"
            d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"
          />
        </svg>
      ) : (
        <>
          {Icon && iconPosition === 'left' && <Icon className="w-5 h-5" />}
          {children}
          {Icon && iconPosition === 'right' && <Icon className="w-5 h-5" />}
        </>
      )}
    </button>
  );
};

export default Button;
