const Badge = ({ children, variant = 'default', size = 'md', dot = false, className = '' }) => {
  const variants = {
    default: 'bg-secondary-100 text-secondary-700 ring-1 ring-inset ring-secondary-200',
    success: 'bg-green-50 text-green-700 ring-1 ring-inset ring-green-200',
    warning: 'bg-amber-50 text-amber-700 ring-1 ring-inset ring-amber-200',
    danger: 'bg-red-50 text-red-700 ring-1 ring-inset ring-red-200',
    info: 'bg-blue-50 text-blue-700 ring-1 ring-inset ring-blue-200',
    primary: 'bg-primary-50 text-primary-700 ring-1 ring-inset ring-primary-200',
    purple: 'bg-purple-50 text-purple-700 ring-1 ring-inset ring-purple-200',
  };

  const dotColors = {
    default: 'bg-secondary-500',
    success: 'bg-green-500',
    warning: 'bg-amber-500',
    danger: 'bg-red-500',
    info: 'bg-blue-500',
    primary: 'bg-primary-500',
    purple: 'bg-purple-500',
  };

  const sizes = {
    sm: 'px-2 py-0.5 text-xs',
    md: 'px-2.5 py-1 text-xs',
    lg: 'px-3 py-1.5 text-sm',
  };

  return (
    <span className={`inline-flex items-center gap-1.5 font-medium rounded-full ${variants[variant]} ${sizes[size]} ${className}`}>
      {dot && <span className={`w-1.5 h-1.5 rounded-full ${dotColors[variant]}`} />}
      {children}
    </span>
  );
};

export default Badge;
