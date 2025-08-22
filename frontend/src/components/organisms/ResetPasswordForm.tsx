import React, { useState } from 'react';
import FormField from '../molecules/FormField';
import Button from '../atoms/Button';
import { useAuth } from '../../hooks/useAuth';

const ResetPasswordForm: React.FC = () => {
  const [newPassword, setNewPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [isSubmitted, setIsSubmitted] = useState(false);
  const { resetPassword, isLoading } = useAuth();

  // Get token from URL params (in real app, use react-router hooks)
  const token = new URLSearchParams(window.location.search).get('token') || '';

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (newPassword !== confirmPassword) {
      alert('Passwords do not match');
      return;
    }
    
    try {
      await resetPassword({ token, newPassword });
      setIsSubmitted(true);
    } catch (error) {
      console.error('Failed to reset password:', error);
    }
  };

  if (isSubmitted) {
    return (
      <div className="text-center">
        <h3 className="text-lg font-medium text-gray-900 mb-2">
          Password Reset Successful
        </h3>
        <p className="text-gray-600 mb-4">
          Your password has been reset successfully.
        </p>
        <Button onClick={() => window.location.href = '/login'} variant="default">
          Go to Sign In
        </Button>
      </div>
    );
  }

  if (!token) {
    return (
      <div className="text-center">
        <h3 className="text-lg font-medium text-gray-900 mb-2">
          Invalid Reset Link
        </h3>
        <p className="text-gray-600 mb-4">
          This password reset link is invalid or has expired.
        </p>
        <Button onClick={() => window.location.href = '/forgot-password'} variant="outline">
          Request New Reset Link
        </Button>
      </div>
    );
  }

  return (
    <form onSubmit={handleSubmit} className="w-full max-w-md">
      <h2 className="text-2xl font-bold text-center mb-6">Reset Password</h2>
      
      <FormField
        label="New Password"
        type="password"
        value={newPassword}
        onChange={setNewPassword}
        placeholder="Enter new password"
        required
      />
      
      <FormField
        label="Confirm Password"
        type="password"
        value={confirmPassword}
        onChange={setConfirmPassword}
        placeholder="Confirm new password"
        required
      />
      
      <Button
        type="submit"
        disabled={isLoading}
        className="w-full"
      >
        {isLoading ? 'Resetting...' : 'Reset Password'}
      </Button>
    </form>
  );
};

export default ResetPasswordForm;
