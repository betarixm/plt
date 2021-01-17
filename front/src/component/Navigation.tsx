import React from "react";
import {Link, RouteComponentProps, withRouter} from "react-router-dom";
import {PATH_DASHBOARD, PATH_SHOP, PATH_SQLI, PATH_XSS} from "../env/path";

interface NavigationProps extends RouteComponentProps {

}

interface NavigationStates {

}

class NavigationInner extends React.Component<NavigationProps, NavigationStates> {
    render() {
        return (
            <div className={"navigation"}>
                <Link to={PATH_DASHBOARD} className={"title"}>
                    <img src={"/static/img/logo-white.png"} />
                </Link>
                <div className={"links"}>
                    <Link className={this.props.location.pathname === PATH_DASHBOARD ? "selected" : ""} to={PATH_DASHBOARD}>Dashboard</Link>
                    <Link className={this.props.location.pathname.startsWith(PATH_SQLI) ? "selected" : ""} to={PATH_SQLI}>SQL Injection</Link>
                    <Link className={this.props.location.pathname.startsWith(PATH_XSS) ? "selected" : ""} to={PATH_XSS}>XSS</Link>
                    <Link className={this.props.location.pathname.startsWith(PATH_SHOP) ? "selected" : ""} to={PATH_SHOP}>Shop</Link>
                </div>
            </div>
        )
    }
}

const Navigation= withRouter(NavigationInner);
export default Navigation;