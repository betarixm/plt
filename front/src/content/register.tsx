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
    id: string;
    pw: string;
    name: string;
    error?: string;
}

class Register extends React.Component<RegisterProps, RegisterStates> {
    state: RegisterStates = {
        status: "loading",
        id: "",
        pw: "",
        name: ""
    }

    componentDidMount() {
        this.setState({
            status: "input"
        });
    }

    componentWillUnmount() {

    }

    onIdChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        this.setState({id: e.target.value})
    }
    onPwChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        this.setState({pw: e.target.value})
    }
    onNameChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        this.setState({name: e.target.value})
    }

    onSubmit = () => {
        this.setState({
            status: "querying"
        });

        register(this.state.id, this.state.pw, this.state.name)
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
                <input type={"text"} placeholder={"ID"} onChange={this.onIdChange} value={this.state.id}/>
                <input type={"password"} placeholder={"PASSWORD"} onChange={this.onPwChange} value={this.state.pw}/>
                <input type={"text"} placeholder={"TEAM NAME"} onChange={this.onNameChange} value={this.state.name}/>
                <button className={this.state.status === "querying" ? "disabled" : ""} onClick={this.onSubmit}>{this.state.status === "querying" ? "지구-" + this.state.id + " 생성 요청 중..." : "SUBMIT"}</button>
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