import React from 'react';
import { useAuth } from '../../hooks/useAuth';
import Button from './Button';
import { NavbarProps } from '../../types';
import { cn } from '../../utils/cn';

const Navbar: React.FC<NavbarProps> = ({ className = '' }) => {
  const { isAuthenticated, logout, user } = useAuth();

  return (
    <nav className={cn('bg-background shadow-sm border-b border-border', className)}>
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          <div className="flex items-center">
            <h1 className="text-xl font-bold text-foreground">
              React Atomic App
            </h1>
          </div>
          
          <div className="flex items-center space-x-4">
            {isAuthenticated ? (
              <>
                <span className="text-muted-foreground">
                  Welcome, {user?.name}
                </span>
                <Button variant="outline" onClick={logout}>
                  Logout
                </Button>
              </>
            ) : (
              <Button onClick={() => window.location.href = '/login'}>
                Sign In
              </Button>
            )}
          </div>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
