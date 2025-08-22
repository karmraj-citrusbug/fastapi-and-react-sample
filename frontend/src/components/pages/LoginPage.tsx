import React from 'react';
import AuthPageTemplate from '../templates/AuthPageTemplate';
import LoginForm from '../organisms/LoginForm';

const LoginPage: React.FC = () => {
  return (
    <AuthPageTemplate title="Sign In">
      <LoginForm />
    </AuthPageTemplate>
  );
};

export default LoginPage;
