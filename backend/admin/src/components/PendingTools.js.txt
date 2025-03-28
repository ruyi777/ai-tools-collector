// backend/admin/src/components/PendingTools.js
import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Table, Button, Tag, message, Select } from 'antd';

const { Option } = Select;

const PendingTools = () => {
  const [tools, setTools] = useState([]);
  const [loading, setLoading] = useState(true);
  const [categories, setCategories] = useState([]);
  
  const fetchPendingTools = async () => {
    try {
      const res = await axios.get('/api/pending-tools');
      setTools(res.data.data);
    } catch (err) {
      message.error('Failed to fetch tools');
    } finally {
      setLoading(false);
    }
  };
  
  const handleApprove = async (id, selectedCategories) => {
    try {
      await axios.post(`/api/tools/${id}/approve`, {
        categories: selectedCategories
      });
      message.success('Tool approved');
      fetchPendingTools();
    } catch (err) {
      message.error('Approval failed');
    }
  };
  
  useEffect(() => {
    fetchPendingTools();
    // 加载预设分类
    setCategories(['Text&Writing', 'Image', 'Video', 'Chatbot', 'Productivity']);
  }, []);

  const columns = [
    {
      title: 'Name',
      dataIndex: 'name',
      key: 'name',
      render: (text, record) => (
        <a href={record.url} target="_blank" rel="noopener noreferrer">
          {text}
        </a>
      ),
    },
    {
      title: 'Description',
      dataIndex: 'description',
      key: 'description',
    },
    {
      title: 'Categories',
      key: 'categories',
      render: (_, record) => (
        <Select
          mode="multiple"
          style={{ width: '100%' }}
          placeholder="Select categories"
          onChange={(values) => {
            setTools(tools.map(t => 
              t.id === record.id ? {...t, selectedCategories: values} : t
            ));
          }}
        >
          {categories.map(cat => (
            <Option key={cat} value={cat}>{cat}</Option>
          ))}
        </Select>
      ),
    },
    {
      title: 'Action',
      key: 'action',
      render: (_, record) => (
        <Button
          type="primary"
          onClick={() => handleApprove(record.id, record.selectedCategories || [])}
        >
          Approve
        </Button>
      ),
    },
  ];

  return (
    <div>
      <h2>Pending Tools ({tools.length})</h2>
      <Table 
        columns={columns} 
        dataSource={tools} 
        loading={loading}
        rowKey="id"
      />
    </div>
  );
};

export default PendingTools;