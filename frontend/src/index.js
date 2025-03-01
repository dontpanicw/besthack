import React from 'react';
import { useContext, createContext } from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';
import "./styles.css";
import { BrowserRouter } from 'react-router-dom';
import Store from './store/store_auth';

export const store = new Store();

export const Context = createContext({
  store
});




const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <Context.Provider value={{store}}>
  <BrowserRouter>
  <React.StrictMode>
    <App />
  </React.StrictMode>
  </BrowserRouter>
  </Context.Provider>
);

