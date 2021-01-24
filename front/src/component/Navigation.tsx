import React from "react";
import {Link, RouteComponentProps, withRouter} from "react-router-dom";
import {PATH_DASHBOARD, PATH_SCOREBOARD, PATH_SHOP, PATH_SQLI, PATH_XSS} from "../env/path";

interface NavigationProps extends RouteComponentProps {

}

interface NavigationStates {

}

class NavigationInner extends React.Component<NavigationProps, NavigationStates> {
    componentDidMount() {
        window.addEventListener('scroll', () => {
            const nav = document.getElementById("nav");
            if(nav) {
                if(window.scrollY > nav.clientHeight){
                    nav.style.background = "linear-gradient(#05003dff, #05003d66)"
                    // @ts-ignore
                    nav.style.backdropFilter = "blur(5px)";
                } else {
                    nav.style.background = "";
                    // @ts-ignore
                    nav.style.backdropFilter = "";
                }
            }
        })
    }

    scrollToTop = () => {
        window.scrollTo(0, 0);
    }

    render() {
        return (
            <div id="nav" className={"navigation"}>
                <Link to={PATH_DASHBOARD} className={"title"}>
                    <img src={"/static/img/logo-white.png"} />
                </Link>
                <div className={"links"}>
                    <Link onClick={this.scrollToTop} className={this.props.location.pathname === PATH_DASHBOARD ? "selected" : ""} to={PATH_DASHBOARD}>Dashboard</Link>
                    <Link onClick={this.scrollToTop} className={this.props.location.pathname.startsWith(PATH_SCOREBOARD) ? "selected" : ""} to={PATH_SCOREBOARD}>Scoreboard</Link>
                    <Link onClick={this.scrollToTop} className={this.props.location.pathname.startsWith(PATH_SQLI) ? "selected" : ""} to={PATH_SQLI}>SQL Injection</Link>
                    <Link onClick={this.scrollToTop} className={this.props.location.pathname.startsWith(PATH_XSS) ? "selected" : ""} to={PATH_XSS}>XSS</Link>
                    <Link onClick={this.scrollToTop} className={this.props.location.pathname.startsWith(PATH_SHOP) ? "selected" : ""} to={PATH_SHOP}>Shop</Link>
                </div>
            </div>
        )
    }
}

const Navigation= withRouter(NavigationInner);
export default Navigation;