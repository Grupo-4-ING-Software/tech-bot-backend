export const getChatToken = async (): Promise<string> => {
  const response = await fetch(`${API_BASE_URL}/api/chat/token`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${getAccessToken()}` // Si usas token de autenticación
    },
    credentials: 'include' // Si usas cookies
  });

  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  }

  const data = await response.json();
  return data.token;
}; 