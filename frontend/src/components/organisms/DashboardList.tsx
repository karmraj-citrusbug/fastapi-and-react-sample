import React, { useState, useEffect } from 'react';
import Button from '../atoms/Button';

interface DashboardItem {
  id: string;
  title: string;
  description: string;
  status: 'active' | 'inactive' | 'pending';
  createdAt: string;
}

const DashboardList: React.FC = () => {
  const [items, setItems] = useState<DashboardItem[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    // Simulate API call to fetch dashboard items
    const fetchItems = async () => {
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      const mockItems: DashboardItem[] = [
        {
          id: '1',
          title: 'Project Alpha',
          description: 'A comprehensive project management system',
          status: 'active',
          createdAt: '2024-01-15'
        },
        {
          id: '2',
          title: 'Project Beta',
          description: 'An innovative mobile application',
          status: 'pending',
          createdAt: '2024-01-20'
        },
        {
          id: '3',
          title: 'Project Gamma',
          description: 'A data analytics platform',
          status: 'inactive',
          createdAt: '2024-01-10'
        }
      ];
      
      setItems(mockItems);
      setIsLoading(false);
    };

    fetchItems();
  }, []);

  const getStatusColor = (status: DashboardItem['status']) => {
    switch (status) {
      case 'active':
        return 'bg-green-100 text-green-800';
      case 'inactive':
        return 'bg-red-100 text-red-800';
      case 'pending':
        return 'bg-yellow-100 text-yellow-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  if (isLoading) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="text-gray-500">Loading...</div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h2 className="text-2xl font-bold text-gray-900">Dashboard</h2>
        <Button onClick={() => console.log('Add new item')}>
          Add New Item
        </Button>
      </div>
      
      <div className="grid gap-4">
        {items.map((item) => (
          <div
            key={item.id}
            className="bg-white p-6 rounded-lg shadow-sm border border-gray-200"
          >
            <div className="flex justify-between items-start">
              <div className="flex-1">
                <h3 className="text-lg font-medium text-gray-900 mb-2">
                  {item.title}
                </h3>
                <p className="text-gray-600 mb-3">{item.description}</p>
                <p className="text-sm text-gray-500">
                  Created: {item.createdAt}
                </p>
              </div>
              <div className="flex items-center space-x-2">
                <span className={`px-2 py-1 text-xs font-medium rounded-full ${getStatusColor(item.status)}`}>
                  {item.status}
                </span>
                <Button variant="outline" size="sm">
                  Edit
                </Button>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default DashboardList;
