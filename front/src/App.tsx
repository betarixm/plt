import React from 'react';

import {
    BrowserRouter as Router,
    Switch,
    Route,
    Link
} from "react-router-dom";

import './App.scss';
import {
    PATH_SQLI,
    PATH_XSS,
    PATH_LOGIN,
    PATH_REGISTER,
    PATH_SHOP,
    PATH_ITEM,
    PATH_DASHBOARD,
    PATH_SCOREBOARD
} from "./env/path";
import Sqli from "./content/challenge/sqli";
import Xss from "./content/challenge/xss";
import Login from "./content/login";
import Register from "./content/register";
import Shop from "./content/shop/shop";
import Item from "./content/shop/item";
import Dashboard from "./content/Dashboard";
import Navigation from "./component/Navigation";
import Scoreboard from "./content/scoreboard";
import {ping} from "./env/api";
import Loading from "./component/Loading";

interface AppProps {

}

interface AppStates {
    status: "loading"|"login"|"logout"
}

class App extends React.Component<AppProps, AppStates> {
    state: AppStates = {
        status: "loading"
    }

    componentDidMount() {
        console.log("wow")
        ping().then((res) => {
            this.setState({
                status: "login"
            })
        }).catch((err) => {
            this.setState({
                status: "logout"
            })
        })
    }

    componentWillUnmount() {

    }

    onLoginSuccess = () => {
        this.setState({
            status: "login"
        });
    }

    render() {
        if (this.state.status === "loading") {
            return (
                <Loading description={"지구 무결성 검증 중..."} />
            )
        }

        return (
            <Router>
                <div className="App">
                    <Navigation />
                    <Switch>
                        {this.state.status === "logout" && (
                            <Route path={"*"}>
                                <Login onLogin={this.onLoginSuccess}/>
                            </Route>
                        )}
                        <Route exact path={PATH_LOGIN}>
                            <Login onLogin={this.onLoginSuccess}/>
                        </Route>
                        <Route exact path={PATH_SQLI}>
                            <Sqli />
                        </Route>
                        <Route exact path={PATH_XSS}>
                            <Xss />
                        </Route>
                        <Route exact path={PATH_REGISTER}>
                            <Register />
                        </Route>
                        <Route exact path={PATH_SHOP}>
                            <Shop />
                        </Route>
                        <Route exact path={PATH_ITEM}>
                            <Item />
                        </Route>
                        <Route exact path={PATH_SCOREBOARD}>
                            <Scoreboard />
                        </Route>
                        <Route exact path={PATH_DASHBOARD}>
                            <Dashboard />
                        </Route>
                    </Switch>
                </div>
            </Router>

        );
    }
}

export default App;
