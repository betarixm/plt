import React from "react";
import Loading from "./Loading";
import {authFlag} from "../env/api";
import Alert from "./Alert";

interface FlagProps {
    onSuccess(score: number, point: number): void;
}

interface FlagStates {
    status: "loading" | "input" | "querying" | "success" | "error";
    message?: string;
    flag: string;
}

class Flag extends React.Component<FlagProps, FlagStates> {
    state: FlagStates = {
        status: "loading",
        flag: ""
    }

    componentDidMount() {
        this.setState({
            status: "input"
        })
    }

    componentWillUnmount() {

    }

    onFlagChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        this.setState({
            flag: e.target.value
        });
    }

    onSubmit = () => {
        this.setState({
            status: "querying"
        })
        authFlag(this.state.flag)
            .then((res) => {
                this.props.onSuccess(res, res);
                this.setState({
                    status: "success",
                    message: `ECHO-INDEX/POINT: ${res} 상승`
                });
            })
            .catch((err) => {
                this.setState({
                    status: "error",
                    message: err.toString()
                });
            })
    }


    content = () => {
        if(this.state.status === "loading") {
            return (
                <Loading description={"다른 행성에 쓰레기 투기 시도 중..."} />
            )
        } else {
            return (
                <>
                    <input placeholder={"Auth Flag..."} className={"query"} type={"text"} onChange={this.onFlagChange} value={this.state.flag} />
                    <button onClick={this.onSubmit}>Auth</button>
                </>
            )
        }
    }

    alert = () => {
        if(this.state.status === "success" || this.state.status === "error") {
            return (
                <Alert type={this.state.status === "success" ? "success" : "warning"} message={this.state.message}/>
            )
        }
    }

    render() {
        return (
            <>
                {this.alert()}
                <div className={"flagBox"}>
                    {this.content()}
                </div>
            </>
        );
    }
}

export default Flag;