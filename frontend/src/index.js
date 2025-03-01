import React from 'react';
import { useContext, createContext } from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';
import "./styles.css";
import "./fonts.css";
import { BrowserRouter } from 'react-router-dom';
import Store from './store/store_auth';
import StoreLots from './store/store_lots';

export const store = new Store(),
storelots = new StoreLots();

export const Context = createContext({
  store,
  storelots
});

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <Context.Provider value={{store, storelots}}>
  <BrowserRouter>
  <React.StrictMode>
    <App />
  </React.StrictMode>
  </BrowserRouter>
  </Context.Provider>
);

