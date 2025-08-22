import React from 'react';
import DashboardTemplate from '../templates/DashboardTemplate';
import DashboardList from '../organisms/DashboardList';

const DashboardPage: React.FC = () => {
  return (
    <DashboardTemplate>
      <DashboardList />
    </DashboardTemplate>
  );
};

export default DashboardPage;
