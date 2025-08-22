import React, { useState } from 'react';
import FormField from '../molecules/FormField';
import Button from '../atoms/Button';
import { useAuth } from '../../hooks/useAuth';

const ForgotPasswordForm: React.FC = () => {
  const [email, setEmail] = useState('');
  const [isSubmitted, setIsSubmitted] = useState(false);
  const { forgotPassword, isLoading } = useAuth();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    try {
      await forgotPassword({ email });
      setIsSubmitted(true);
    } catch (error) {
      console.error('Failed to send reset email:', error);
    }
  };

  if (isSubmitted) {
    return (
      <div className="text-center">
        <h3 className="text-lg font-medium text-gray-900 mb-2">
          Check your email
        </h3>
        <p className="text-gray-600 mb-4">
          We've sent a password reset link to {email}
        </p>
        <Button onClick={() => setIsSubmitted(false)} variant="outline">
          Try another email
        </Button>
      </div>
    );
  }

  return (
    <form onSubmit={handleSubmit} className="w-full max-w-md">
      <h2 className="text-2xl font-bold text-center mb-6">Forgot Password</h2>
      
      <p className="text-gray-600 text-center mb-6">
        Enter your email address and we'll send you a link to reset your password.
      </p>
      
      <FormField
        label="Email"
        type="email"
        value={email}
        onChange={setEmail}
        placeholder="Enter your email"
        required
      />
      
      <Button
        type="submit"
        disabled={isLoading}
        className="w-full"
      >
        {isLoading ? 'Sending...' : 'Send Reset Link'}
      </Button>
      
      <div className="text-center mt-4">
        <a href="/login" className="text-blue-600 hover:underline">
          Back to Sign In
        </a>
      </div>
    </form>
  );
};

export default ForgotPasswordForm;
