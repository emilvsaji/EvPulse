import { X } from 'lucide-react';
import { useEffect, useState } from 'react';

const Modal = ({ 
  isOpen, 
  onClose, 
  title, 
  description,
  icon: Icon,
  iconBg = 'bg-primary-100',
  iconColor = 'text-primary-600',
  children, 
  size = 'md',
  showCloseButton = true,
  footer,
}) => {
  const [isAnimating, setIsAnimating] = useState(false);

  // Handle animations
  useEffect(() => {
    if (isOpen) {
      setIsAnimating(true);
    }
  }, [isOpen]);

  // Close on escape key
  useEffect(() => {
    const handleEscape = (e) => {
      if (e.key === 'Escape') onClose();
    };
    
    if (isOpen) {
      document.addEventListener('keydown', handleEscape);
      document.body.style.overflow = 'hidden';
    }
    
    return () => {
      document.removeEventListener('keydown', handleEscape);
      document.body.style.overflow = '';
    };
  }, [isOpen, onClose]);

  if (!isOpen) return null;

  const sizeClasses = {
    sm: 'max-w-md',
    md: 'max-w-lg',
    lg: 'max-w-2xl',
    xl: 'max-w-4xl',
    full: 'max-w-6xl',
  };

  return (
    <div className="fixed inset-0 z-50 overflow-y-auto">
      {/* Backdrop */}
      <div 
        className={`fixed inset-0 bg-secondary-900/60 backdrop-blur-sm transition-opacity duration-300 ${
          isAnimating ? 'opacity-100' : 'opacity-0'
        }`}
        onClick={onClose}
      />
      
      {/* Modal Container */}
      <div className="flex min-h-full items-center justify-center p-4">
        <div 
          className={`relative bg-white rounded-3xl shadow-2xl w-full ${sizeClasses[size]} transform transition-all duration-300 ${
            isAnimating ? 'opacity-100 scale-100 translate-y-0' : 'opacity-0 scale-95 translate-y-4'
          }`}
          onClick={(e) => e.stopPropagation()}
        >
          {/* Close Button - Floating */}
          {showCloseButton && (
            <button
              onClick={onClose}
              className="absolute -top-3 -right-3 w-10 h-10 bg-white rounded-full shadow-lg flex items-center justify-center hover:bg-secondary-50 transition-colors z-10 border border-secondary-100"
            >
              <X className="w-5 h-5 text-secondary-500" />
            </button>
          )}

          {/* Header */}
          {(title || Icon) && (
            <div className="px-6 pt-6 pb-4">
              {Icon && (
                <div className={`w-14 h-14 ${iconBg} rounded-2xl flex items-center justify-center mb-4`}>
                  <Icon className={`w-7 h-7 ${iconColor}`} />
                </div>
              )}
              {title && (
                <h2 className="text-xl font-bold text-secondary-900">{title}</h2>
              )}
              {description && (
                <p className="text-secondary-500 mt-1">{description}</p>
              )}
            </div>
          )}

          {/* Content */}
          <div className={`px-6 ${title || Icon ? 'pb-6' : 'py-6'}`}>
            {children}
          </div>

          {/* Footer */}
          {footer && (
            <div className="px-6 py-4 bg-secondary-50/50 border-t border-secondary-100 rounded-b-3xl flex items-center justify-end gap-3">
              {footer}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default Modal;
