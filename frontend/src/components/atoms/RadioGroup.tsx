import React from 'react';
import { RadioGroupProps, RadioGroupItemProps } from '../../types';
import { cn } from '../../utils/cn';

const RadioGroup: React.FC<RadioGroupProps> = ({
  value,
  onValueChange,
  disabled = false,
  className = '',
  children,
}) => {
  return (
    <div className={cn('grid gap-2', className)}>
      {React.Children.map(children, (child) => {
        if (React.isValidElement(child)) {
          return React.cloneElement(child, {
            ...child.props,
            checked: child.props.value === value,
            onCheckedChange: () => onValueChange?.(child.props.value),
            disabled: disabled || child.props.disabled,
          });
        }
        return child;
      })}
    </div>
  );
};

const RadioGroupItem: React.FC<RadioGroupItemProps> = ({
  value,
  id,
  disabled = false,
  className = '',
  checked = false,
  onCheckedChange,
  children,
}) => {
  const radioId = id || `radio-${value}-${Math.random().toString(36).substr(2, 9)}`;

  const handleChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    if (onCheckedChange) {
      onCheckedChange(event.target.checked);
    }
  };

  return (
    <div className="flex items-center space-x-2">
      <input
        id={radioId}
        type="radio"
        value={value}
        checked={checked}
        onChange={handleChange}
        disabled={disabled}
        className={cn(
          'h-4 w-4 shrink-0 rounded-full border border-primary ring-offset-background focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50',
          className
        )}
      />
      <label htmlFor={radioId} className="text-sm font-medium leading-none">
        {children}
      </label>
    </div>
  );
};

export { RadioGroup, RadioGroupItem };
export default RadioGroup;
