import Introduction from "../Introduction/Introduction";
import Footer from "../Footer/Footer";
import Main from "../Main/Main";
import "./App.css";
import {
  BrowserRouter,
  Switch,
  Route,
} from "react-router-dom/cjs/react-router-dom.min";
const App = () => {
  return (
    <BrowserRouter>
      <div className="app">
        <Route exact path="/">
          <Introduction />
        </Route>
        <Switch>
          <Route path="/Main">
            <Main />
            <Footer />
          </Route>
        </Switch>
      </div>
    </BrowserRouter>
  );
};

export default App;
