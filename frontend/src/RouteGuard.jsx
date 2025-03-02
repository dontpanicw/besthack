import { useContext } from "react";
import { Navigate } from "react-router-dom";
import { store, Context } from ".";
import { observer } from "mobx-react-lite";
import Login from "./components/LoginPage/Login";

function RouteGuard({ children }) {
  const {store} = useContext(Context);

  if (store.isAuth) {
    return <>{children}</>;
  }

  else if (!store.isAuth) {
    return <Login/>;
  }
}

export default observer(RouteGuard);