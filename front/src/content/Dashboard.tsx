import React from "react";
import {getUserInfo} from "../env/api";
import Loading from "../component/Loading";
import Flag from "../component/Flag";

interface DashboardProps {

}

interface DashboardStates {
    status: "loading"|"success"|"error";
    error?: string;
    score?: number;
    point?: number;
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
                    status: "success",
                    score: this.team.score,
                    point: this.team.money
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

    onAuthSuccess = (score: number, point: number) => {
        this.setState({
            score: (this.state.score ? this.state.score : 0) + score,
            point: (this.state.point ? this.state.point : 0) + point
        })
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
                            <div className={"key"}>FIREWALL ECO INDEX</div>
                            <div className={"value"}>{this.state.score}</div>
                        </div>
                        <div className={"tag"}>
                            <div className={"key"}>ECO POINT</div>
                            <div className={"value"}>{this.state.point}</div>
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
                    <Flag onSuccess={this.onAuthSuccess} />
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