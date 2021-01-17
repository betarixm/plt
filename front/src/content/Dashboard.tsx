import React from "react";
import {getUserInfo} from "../env/api";
import Loading from "../component/Loading";

interface DashboardProps {

}

interface DashboardStates {
    status: "loading"|"success"|"error";
    error?: string;
}

class Dashboard extends React.Component<DashboardProps, DashboardStates> {
    team?: Team;

    state: DashboardStates = {
        status: "loading"
    }

    componentDidMount() {
        getUserInfo()
            .then((res) => {
                this.team = res;
                this.setState({
                    status: "success"
                })
            })
            .catch((err) => {
                this.setState({
                    status: "error",
                    error: err.toString()
                });
            })
    }

    componentWillUnmount() {

    }

    TeamInfo = () => {
        if(this.team) {
            return (
                <div className={"team"}>
                    <img src={"/static/img/plant.png"}/>
                    <div className={"info"}>
                        <div className={"tag"}>
                            <div className={"key"}>TEAM NAME</div>
                            <div className={"value"}>{this.team.name}</div>
                        </div>
                        <div className={"tag"}>
                            <div className={"key"}>FIREWALL-ECHO-SCORE</div>
                            <div className={"value"}>{this.team.score}</div>
                        </div>
                    </div>
                </div>
            )
        }
    }

    content = () => {
        if(this.state.status === "loading") {
            return (
                <Loading description={"사용자 지구 정보 불러오는 중..."} />
            )
        } else if (this.state.status === "success" && this.team) {
            return (
                <>
                    {this.TeamInfo()}
                </>
            )
        }
    }
    render() {
        return (
            <div className={"dashboard"}>
                {this.content()}
            </div>
        )
    }
}

export default Dashboard;