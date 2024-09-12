import React, { useCallback, useEffect, useState } from 'react'
import { Table } from "antd"
import axios from "axios"


const DetailPage = () => {
  const columns = [
    {
      title: '테스트다',
      dataIndex: 'complex_id',
      key: 'complex_id',
    },
    {
      title: '단지명',
      dataIndex: 'complex_name',
      key: 'complex_name',
    },

    {
      title: '단지 주소',
      dataIndex: 'complex_addr',
      key: 'complex_addr',
    },
    {
      title: '평수',
      dataIndex: 'complex_width',
      key: 'complex_width',
    },
    {
      title: '세대수',
      dataIndex: 'complex_num',
      key: 'complex_num',
    },

    {
      title: '건설사',
      dataIndex: 'complex_company',
      key: 'complex_company',
    },
    {
      title: '등록일자',
      dataIndex: 'user_registration_date',
      key: 'user_registration_date',
    },
    {
      title: '사용여부',
      dataIndex: 'usage_status',
      key: 'usage_status',
    },
  ];

  const [complexItems, setComplexItems] = useState([])

  const fetchComplexItems = useCallback(async () => {
    const response = await axios.post("http://localhost:8000/complex_list")

    if (response.status === 200) {
      setComplexItems(response.data)
    }

  }, [])

  useEffect(() => {
    fetchComplexItems()
  }, [])


  return (
    <div>
      <Table dataSource={complexItems} columns={columns}></Table>
    </div>
  )
}

export default DetailPage
