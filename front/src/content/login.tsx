import React from "react"
import {Redirect} from "react-router-dom";
import Loading from "../component/Loading";
import {login} from "../env/api";
import Alert from "../component/Alert";

interface LoginProps {

}

interface LoginStates {
    status: "loading"|"input"|"querying"|"done"|"error";
    id: string;
    pw: string;
    error?: string;
}

class Login extends React.Component<LoginProps, LoginStates> {
    state: LoginStates ={
        id: "",
        pw: "",
        status: "loading"
    };

    componentDidMount() {
        this.setState({
            status: "input"
        })
    }

    componentWillUnmount() {

    }

    onIdChange = (e: React.ChangeEvent<HTMLInputElement>) => {this.setState({id: e.target.value})}

    onPwChange = (e: React.ChangeEvent<HTMLInputElement>) => {this.setState({pw: e.target.value})}

    onSubmit = () => {
        console.log("Asdf")
        this.setState({
            status: "querying"
        })

        login(this.state.id, this.state.pw)
            .then((res) => {
                this.setState({
                    status: "done"
                });
            })
            .catch((err) => {
                this.setState({
                    status: "error",
                    error: err.toString()
                });
            })
    }

    Input = () => {
        return (
            <div>
                <input type={"text"} onChange={this.onIdChange} value={this.state.id} />
                <input type={"password"} onChange={this.onPwChange} value={this.state.pw} />
                <button onClick={this.onSubmit}>로그인</button>
            </div>
        );
    }

    content = () => {
        if(this.state.status === "loading") {
            return (
                <Loading description={"BnL 인증 시스템 불러오는 중..."} />
            );
        } else if(this.state.status === "querying") {
            return (
                <Loading description={"지구-"+this.state.id + " 접근 가능성 조회 중..."} />
            )
        } else {
            return (
                <>
                    {this.Input()}
                </>
            );
        }
    }

    render() {
        if(this.state.status === "done") {
            return (
                <Redirect to={"/"} />
            )
        }
        return (
            <div>
                <div className={"title"}>LOG-IN</div>
                {this.state.status === "error" && <Alert type={"warning"} message={this.state.error} />}
                {this.content()}
            </div>
        );
    }
}

export default Login;