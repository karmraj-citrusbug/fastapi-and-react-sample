# React Atomic Auth App

A React TypeScript application built using Atomic Design principles with authentication features and a dashboard.

## Project Structure

```
src/
├── components/
│   ├── atoms/           # Basic UI primitives
│   │   └── Button.tsx
│   ├── molecules/       # Combinations of atoms
│   │   └── FormField.tsx
│   ├── organisms/       # Complex components
│   │   ├── LoginForm.tsx
│   │   ├── ForgotPasswordForm.tsx
│   │   ├── ResetPasswordForm.tsx
│   │   └── DashboardList.tsx
│   ├── templates/       # Layout wrappers
│   │   ├── AuthPageTemplate.tsx
│   │   └── DashboardTemplate.tsx
│   └── pages/          # Page components
│       ├── LoginPage.tsx
│       ├── ForgotPasswordPage.tsx
│       ├── ResetPasswordPage.tsx
│       └── DashboardPage.tsx
├── App.tsx             # Main app component with routing
└── index.tsx           # App entry point
```

## Features

- **Authentication System**: Login, Forgot Password, and Reset Password
- **Dashboard**: Simple listing page with mock data
- **Atomic Design**: Organized component hierarchy (atoms → molecules → organisms → templates → pages)
- **TypeScript**: Full type safety with interfaces and types
- **React Router**: Client-side routing between pages
- **SharedCN**: Reusable components, hooks, and utilities

## Getting Started

1. Install dependencies:
   ```bash
   npm install
   ```

2. Start the development server:
   ```bash
   npm start
   ```

3. Open [http://localhost:3000](http://localhost:3000) in your browser.

## Available Routes

- `/login` - User login page
- `/forgot-password` - Forgot password page
- `/reset-password` - Reset password page (requires token)
- `/dashboard` - Dashboard with listing page

## Component Architecture

### Atoms
- **Button**: Reusable button component with variants and states

### Molecules
- **FormField**: Labeled input field combining label and input atoms

### Organisms
- **LoginForm**: Complete login form with email and password fields
- **ForgotPasswordForm**: Form for requesting password reset
- **ResetPasswordForm**: Form for setting new password
- **DashboardList**: Dashboard listing with mock data

### Templates
- **AuthPageTemplate**: Layout for authentication pages
- **DashboardTemplate**: Layout for dashboard pages

### Pages
- **LoginPage**: Login page using AuthPageTemplate
- **ForgotPasswordPage**: Forgot password page using AuthPageTemplate
- **ResetPasswordPage**: Reset password page using AuthPageTemplate
- **DashboardPage**: Dashboard page using DashboardTemplate

## SharedCN (Shared Components)

### Components
- **Navbar**: Navigation bar with authentication state
- **Footer**: Application footer

### Hooks
- **useAuth**: Authentication hook with login, logout, forgot password, and reset password functions

### Utils
- **api.ts**: API utility functions for HTTP requests
- **constants.ts**: Application constants and configuration

### Styles
- **shared.module.css**: Shared CSS modules for consistent styling

## Technologies Used

- React 18
- TypeScript
- React Router DOM
- Tailwind CSS (for styling)
- Atomic Design principles

## Development Notes

- All components are fully typed with TypeScript
- Mock data and API calls are implemented for demonstration
- Responsive design with mobile-first approach
- Clean separation of concerns following Atomic Design principles
