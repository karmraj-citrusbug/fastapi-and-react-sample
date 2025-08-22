import React from 'react';
import AuthPageTemplate from '../templates/AuthPageTemplate';
import ForgotPasswordForm from '../organisms/ForgotPasswordForm';

const ForgotPasswordPage: React.FC = () => {
  return (
    <AuthPageTemplate title="Forgot Password">
      <ForgotPasswordForm />
    </AuthPageTemplate>
  );
};

export default ForgotPasswordPage;
