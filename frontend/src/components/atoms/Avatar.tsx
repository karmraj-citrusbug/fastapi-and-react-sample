import React from 'react';
import { AvatarProps } from '../../types';
import { cn } from '../../utils/cn';

const Avatar: React.FC<AvatarProps> = ({
  src,
  alt,
  fallback,
  size = 'md',
  className = '',
}) => {
  const sizeClasses = {
    sm: 'h-8 w-8',
    md: 'h-10 w-10',
    lg: 'h-12 w-12'
  };

  const textSizeClasses = {
    sm: 'text-xs',
    md: 'text-sm',
    lg: 'text-base'
  };

  return (
    <div className={cn('relative flex h-10 w-10 shrink-0 overflow-hidden rounded-full', sizeClasses[size], className)}>
      {src ? (
        <img
          className="aspect-square h-full w-full"
          src={src}
          alt={alt || 'Avatar'}
        />
      ) : (
        <div
          className={cn(
            'flex h-full w-full items-center justify-center rounded-full bg-muted',
            textSizeClasses[size]
          )}
        >
          {fallback || 'U'}
        </div>
      )}
    </div>
  );
};

export default Avatar;
