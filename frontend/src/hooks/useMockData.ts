import { useState, useCallback } from 'react';
import {
  MockButtonData,
  MockInputData,
  MockUserData,
  MockNavigationData,
  ButtonProps,
  InputProps
} from '../types';

export const useMockData = () => {
  const [mockButtonData] = useState<MockButtonData[]>([
    {
      id: 'btn-1',
      label: 'Primary Button',
      variant: 'default',
      size: 'default',
      disabled: false,
      loading: false
    },
    {
      id: 'btn-2',
      label: 'Secondary Button',
      variant: 'secondary',
      size: 'default',
      disabled: false,
      loading: false
    },
    {
      id: 'btn-3',
      label: 'Destructive Button',
      variant: 'destructive',
      size: 'default',
      disabled: false,
      loading: false
    },
    {
      id: 'btn-4',
      label: 'Outline Button',
      variant: 'outline',
      size: 'default',
      disabled: false,
      loading: false
    },
    {
      id: 'btn-5',
      label: 'Ghost Button',
      variant: 'ghost',
      size: 'default',
      disabled: false,
      loading: false
    },
    {
      id: 'btn-6',
      label: 'Link Button',
      variant: 'link',
      size: 'default',
      disabled: false,
      loading: false
    },
    {
      id: 'btn-7',
      label: 'Small Button',
      variant: 'default',
      size: 'sm',
      disabled: false,
      loading: false
    },
    {
      id: 'btn-8',
      label: 'Large Button',
      variant: 'default',
      size: 'lg',
      disabled: false,
      loading: false
    },
    {
      id: 'btn-9',
      label: 'Disabled Button',
      variant: 'default',
      size: 'default',
      disabled: true,
      loading: false
    },
    {
      id: 'btn-10',
      label: 'Loading Button',
      variant: 'default',
      size: 'default',
      disabled: false,
      loading: true
    }
  ]);

  const [mockInputData] = useState<MockInputData[]>([
    {
      id: 'input-1',
      type: 'text',
      placeholder: 'Enter your name',
      label: 'Name',
      value: '',
      error: undefined
    },
    {
      id: 'input-2',
      type: 'email',
      placeholder: 'Enter your email',
      label: 'Email',
      value: '',
      error: undefined
    },
    {
      id: 'input-3',
      type: 'password',
      placeholder: 'Enter your password',
      label: 'Password',
      value: '',
      error: undefined
    },
    {
      id: 'input-4',
      type: 'text',
      placeholder: 'Enter your username',
      label: 'Username',
      value: '',
      error: 'Username is required'
    },
    {
      id: 'input-5',
      type: 'tel',
      placeholder: 'Enter your phone number',
      label: 'Phone Number',
      value: '',
      error: undefined
    },
    {
      id: 'input-6',
      type: 'url',
      placeholder: 'Enter your website',
      label: 'Website',
      value: '',
      error: undefined
    },
    {
      id: 'input-7',
      type: 'search',
      placeholder: 'Search...',
      label: 'Search',
      value: '',
      error: undefined
    }
  ]);

  const [mockUserData] = useState<MockUserData[]>([
    {
      id: 'user-1',
      name: 'John Doe',
      email: 'john.doe@example.com',
      avatar: 'https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=150&h=150&fit=crop&crop=face',
      role: 'Admin'
    },
    {
      id: 'user-2',
      name: 'Jane Smith',
      email: 'jane.smith@example.com',
      avatar: 'https://images.unsplash.com/photo-1494790108755-2616b612b786?w=150&h=150&fit=crop&crop=face',
      role: 'User'
    },
    {
      id: 'user-3',
      name: 'Bob Johnson',
      email: 'bob.johnson@example.com',
      avatar: 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=150&h=150&fit=crop&crop=face',
      role: 'Moderator'
    }
  ]);

  const [mockNavigationData] = useState<MockNavigationData[]>([
    {
      id: 'nav-1',
      label: 'Dashboard',
      href: '/dashboard',
      icon: '📊'
    },
    {
      id: 'nav-2',
      label: 'Profile',
      href: '/profile',
      icon: '👤'
    },
    {
      id: 'nav-3',
      label: 'Settings',
      href: '/settings',
      icon: '⚙️'
    },
    {
      id: 'nav-4',
      label: 'Help',
      href: '/help',
      icon: '❓'
    }
  ]);

  const getButtonProps = useCallback((id: string): ButtonProps => {
    const buttonData = mockButtonData.find(btn => btn.id === id);
    if (!buttonData) {
      return {
        children: 'Button',
        variant: 'default',
        size: 'default'
      };
    }

    return {
      children: buttonData.label,
      variant: buttonData.variant,
      size: buttonData.size,
      disabled: buttonData.disabled,
      loading: buttonData.loading
    };
  }, [mockButtonData]);

  const getInputProps = useCallback((id: string): InputProps => {
    const inputData = mockInputData.find(input => input.id === id);
    if (!inputData) {
      return {
        type: 'text',
        placeholder: 'Input',
        label: 'Input'
      };
    }

    return {
      type: inputData.type,
      placeholder: inputData.placeholder,
      label: inputData.label,
      value: inputData.value,
      error: inputData.error
    };
  }, [mockInputData]);

  const updateMockButtonData = useCallback((id: string, updates: Partial<MockButtonData>) => {
    // In a real app, this would update the state
    console.log(`Updating button ${id} with:`, updates);
  }, []);

  const updateMockInputData = useCallback((id: string, updates: Partial<MockInputData>) => {
    // In a real app, this would update the state
    console.log(`Updating input ${id} with:`, updates);
  }, []);

  return {
    mockButtonData,
    mockInputData,
    mockUserData,
    mockNavigationData,
    getButtonProps,
    getInputProps,
    updateMockButtonData,
    updateMockInputData
  };
};
