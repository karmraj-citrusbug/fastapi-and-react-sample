import React from 'react';
import AuthPageTemplate from '../templates/AuthPageTemplate';
import ResetPasswordForm from '../organisms/ResetPasswordForm';

const ResetPasswordPage: React.FC = () => {
  return (
    <AuthPageTemplate title="Reset Password">
      <ResetPasswordForm />
    </AuthPageTemplate>
  );
};

export default ResetPasswordPage;
