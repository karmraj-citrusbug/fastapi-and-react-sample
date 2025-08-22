import React from 'react';
import { Navbar, Footer } from '../atoms';

interface AuthPageTemplateProps {
  children: React.ReactNode;
  title?: string;
}

const AuthPageTemplate: React.FC<AuthPageTemplateProps> = ({ 
  children, 
  title = 'Authentication' 
}) => {
  return (
    <div className="min-h-screen bg-background">
      <Navbar />
      
      <main className="flex-1 flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
        <div className="max-w-md w-full space-y-8">
          <div className="text-center">
            <h1 className="text-3xl font-bold text-foreground">{title}</h1>
          </div>
          {children}
        </div>
      </main>
      
      <Footer />
    </div>
  );
};

export default AuthPageTemplate;
