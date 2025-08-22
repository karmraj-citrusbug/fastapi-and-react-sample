import React from 'react';
import { SwitchProps } from '../../types';
import { cn } from '../../utils/cn';

const Switch: React.FC<SwitchProps> = ({
  checked = false,
  onCheckedChange,
  disabled = false,
  required = false,
  id,
  name,
  className = '',
}) => {
  const switchId = id || name || `switch-${Math.random().toString(36).substr(2, 9)}`;

  const handleChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    onCheckedChange?.(event.target.checked);
  };

  return (
    <div className="flex items-center space-x-2">
      <input
        id={switchId}
        type="checkbox"
        role="switch"
        checked={checked}
        onChange={handleChange}
        disabled={disabled}
        required={required}
        name={name}
        className="peer sr-only"
      />
      <label
        htmlFor={switchId}
        className={cn(
          'peer inline-flex h-6 w-11 shrink-0 cursor-pointer items-center rounded-full border-2 border-transparent transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 focus-visible:ring-offset-background disabled:cursor-not-allowed disabled:opacity-50 data-[state=checked]:bg-primary data-[state=unchecked]:bg-input',
          checked ? 'bg-primary' : 'bg-input',
          disabled && 'cursor-not-allowed opacity-50',
          className
        )}
      >
        <span
          className={cn(
            'pointer-events-none block h-5 w-5 rounded-full bg-background shadow-lg ring-0 transition-transform data-[state=checked]:translate-x-5 data-[state=unchecked]:translate-x-0',
            checked ? 'translate-x-5' : 'translate-x-0'
          )}
        />
      </label>
    </div>
  );
};

export default Switch;
