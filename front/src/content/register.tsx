import React from "react";
import {register} from "../env/api";
import Loading from "../component/Loading";
import {Redirect} from "react-router-dom";
import {PATH_LOGIN} from "../env/path";
import Alert from "../component/Alert";

interface RegisterProps {

}

interface RegisterStates {
    status: "loading" | "input" | "querying" | "done" | "error";
    email: string;
    pw: string;
    username: string;
    error?: string;
}

class Register extends React.Component<RegisterProps, RegisterStates> {
    state: RegisterStates = {
        status: "loading",
        email: "",
        pw: "",
        username: ""
    }

    componentDidMount() {
        this.setState({
            status: "input"
        });
    }

    componentWillUnmount() {

    }

    onEmailChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        this.setState({email: e.target.value})
    }
    onPwChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        this.setState({pw: e.target.value})
    }
    onUsernameChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        this.setState({username: e.target.value})
    }

    onSubmit = () => {
        this.setState({
            status: "querying"
        });

        register(this.state.email, this.state.pw, this.state.username)
            .then((res) => {
                this.setState({
                    status: "done"
                })
            })
            .catch((err) => {
                this.setState({
                    status: "error",
                    error: err.toString()
                })
            })
    }

    Input = () => {
        return (
            <div className={"inputBox"}>
                <input type={"text"} placeholder={"EMAIL"} onChange={this.onEmailChange} value={this.state.email}/>
                <input type={"password"} placeholder={"PASSWORD"} onChange={this.onPwChange} value={this.state.pw}/>
                <input type={"text"} placeholder={"TEAM NAME"} onChange={this.onUsernameChange} value={this.state.username}/>
                <button className={this.state.status === "querying" ? "disabled" : ""} onClick={this.onSubmit}>{this.state.status === "querying" ? "지구-" + this.state.email + " 생성 요청 중..." : "SUBMIT"}</button>
            </div>
        );
    }

    content = () => {
        if (this.state.status === "loading") {
            return (
                <Loading description={"BnL 지구 생성 도우미 불러오는 중..."}/>
            );
        } else {
            return (
                <>
                    {this.Input()}
                </>
            )
        }
    }

    render() {
        if(this.state.status === "done") {
            return (
                <Redirect to={PATH_LOGIN} />
            )
        }

        return (
            <div className={"register"}>
                <div className={"title"}>REGISTER</div>
                {this.state.status === "error" && <Alert type={"warning"} message={this.state.error} /> }
                {this.content()}
            </div>
        );
    }
}

export default Register