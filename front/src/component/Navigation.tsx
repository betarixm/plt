import React from "react";
import {Link} from "react-router-dom";
import {PATH_DASHBOARD, PATH_SHOP, PATH_SQLI, PATH_XSS} from "../env/path";

interface NavigationProps {

}

interface NavigationStates {

}

class Navigation extends React.Component<NavigationProps, NavigationStates> {
    render() {
        return (
            <div className={"navigation"}>
                <Link to={PATH_DASHBOARD} className={"title"}>
                    <img src={"/static/img/logo-white.png"} />
                </Link>
                <div className={"links"}>
                    <Link to={PATH_DASHBOARD}>Dashboard</Link>
                    <Link to={PATH_SQLI}>SQL Injection</Link>
                    <Link to={PATH_XSS}>XSS</Link>
                    <Link to={PATH_SHOP}>Shop</Link>
                </div>
            </div>
        )
    }
}

export default Navigation;