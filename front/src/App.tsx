import React from 'react';

import {
    BrowserRouter as Router,
    Switch,
    Route,
    Link
} from "react-router-dom";

import './App.css';
import {PATH_SQLI, PATH_XSS} from "./env/path";
import Sqli from "./content/challenge/sqli";
import Xss from "./content/challenge/xss";

interface AppProps {

}

interface AppStates {

}

class App extends React.Component<AppProps, AppStates> {
    render() {
        return (
            <Router>
                <div className="App">
                    <Switch>
                        <Route exact path={PATH_SQLI}>
                            <Sqli />
                        </Route>
                        <Route exact path={PATH_XSS}>
                            <Xss />
                        </Route>
                    </Switch>
                </div>
            </Router>

        );
    }
}

export default App;
