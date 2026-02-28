import { useState } from 'react'
import { Typography, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper, Button, Chip } from '@mui/material'

interface User { id: string; name: string; email: string; status: 'active' | 'inactive' }

const mockUsers: User[] = [
  { id: '1', name: 'John Doe', email: 'john@example.com', status: 'active' },
  { id: '2', name: 'Jane Smith', email: 'jane@example.com', status: 'active' },
  { id: '3', name: 'Bob Wilson', email: 'bob@example.com', status: 'inactive' }
]

export default function Users() {
  const [users] = useState<User[]>(mockUsers)

  return (
    <Box>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 3 }}>
        <Typography variant="h4">Users</Typography>
        <Button variant="contained">Add User</Button>
      </Box>
      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Name</TableCell>
              <TableCell>Email</TableCell>
              <TableCell>Status</TableCell>
              <TableCell>Actions</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {users.map((user) => (
              <TableRow key={user.id}>
                <TableCell>{user.name}</TableCell>
                <TableCell>{user.email}</TableCell>
                <TableCell><Chip label={user.status} color={user.status === 'active' ? 'success' : 'default'} size="small" /></TableCell>
                <TableCell><Button size="small">Edit</Button></TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
    </Box>
  )
}

import { Box } from '@mui/material'
