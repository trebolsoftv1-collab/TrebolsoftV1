import api from '../axios';

export const clientsAPI = {
  // Listar clientes
  getClients: async (params = {}) => {
    const response = await api.get('/api/v1/clients/', { params });
    return response.data;
  },

  // Obtener cliente por ID
  getClient: async (id) => {
    const response = await api.get(`/api/v1/clients/${id}`);
    return response.data;
  },

  // Crear cliente
  createClient: async (data) => {
    const response = await api.post('/api/v1/clients/', data);
    return response.data;
  },

  // Actualizar cliente
  updateClient: async (id, data) => {
    const response = await api.put(`/api/v1/clients/${id}`, data);
    return response.data;
  },

  // Eliminar cliente (soft delete)
  deleteClient: async (id) => {
    await api.delete(`/api/v1/clients/${id}`);
  },

  // Subir foto de la casa
  uploadPhoto: async (clientId, file) => {
    const formData = new FormData();
    formData.append('file', file);
    
    const response = await api.post(
      `/api/v1/clients/${clientId}/upload-photo`,
      formData,
      {
        headers: { 'Content-Type': 'multipart/form-data' }
      }
    );
    return response.data;
  },
};
