import React from 'react';
import { FooterProps } from '../../types';
import { cn } from '../../utils/cn';

const Footer: React.FC<FooterProps> = ({ className = '' }) => {
  return (
    <footer className={cn('bg-background border-t border-border mt-auto', className)}>
      <div className="max-w-7xl mx-auto py-6 px-4 sm:px-6 lg:px-8">
        <div className="text-center text-muted-foreground">
          <p>&copy; 2024 React Atomic App. Built with Atomic Design principles.</p>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
