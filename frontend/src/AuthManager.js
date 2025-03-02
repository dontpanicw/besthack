let storeInstance = null;

export const setStore = (store) => {
  storeInstance = store;
};

export const handleUnauthorized = () => {
  if (storeInstance) {
    storeInstance.setAuth(false);
    localStorage.removeItem('token');
    window.location.href = '/Login';
  }
};