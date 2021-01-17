import React from "react";
import {getTeamList} from "../env/api";
import Alert from "../component/Alert";
import Loading from "../component/Loading";

interface ScoreboardProps {

}

interface ScoreboardStates {
    status: "loading"|"success"|"error"
    error?: string
}

class Scoreboard extends React.Component<ScoreboardProps, ScoreboardStates> {
    state: ScoreboardStates = {
        status: "loading"
    }

    timer?: NodeJS.Timeout;
    isMount: boolean = false;
    teamList: Array<TeamInfo> = [];

    componentDidMount() {
        this.isMount = true;

        this.updateScore();
        this.timer = setInterval(this.updateScore, 5000);
    }

    componentWillUnmount() {
        this.isMount = false;
        if(this.timer) {
            clearInterval(this.timer);
        }
    }

    updateScore = () => {
        console.log("www")
        if(!this.isMount){
            if(this.timer) {
                clearInterval(this.timer);
            }
            return;
        }
        this.setState({
            status: "loading"
        })
        getTeamList()
            .then((res) => {
                this.teamList = res;
                this.setState({
                    status: "success"
                });
            })
            .catch((err) => {
                this.setState({
                    status: "error",
                    error: err.toString()
                })
            })
    }

    Attack = (team: TeamInfo) => {
        return (
            <div className={"attackBox"}>
                <div className={"attack"}>
                    <div className={"key"}>SQLi</div>
                    <div className={"value"}>
                        {team.attacks.SQLi ? "공격 있음" : "최근 공격 없음"}
                    </div>
                </div>
                <div className={"attack"}>
                    <div className={"key"}>XSS</div>
                    <div className={"value"}>
                        {team.attacks.XSS ? "공격 있음" : "최근 공격 없음"}
                    </div>
                </div>
            </div>
        )
    }
    List = () => {
        this.teamList.sort((a, b) => {
            // @ts-ignore
            return b.score - a.score;
        })
        const scoreList = this.teamList.map((team, index) => {
            return (
                <div key={index} className={"scoreEle"}>
                    <div className={"row"}>
                        <div className={"name"}>{team.teamname}</div>
                        <div className={"score"}>{team.score}</div>
                    </div>
                    {this.Attack(team)}
                </div>
            )
        })
        return (
            <div className={"scoreBox"}>
                {scoreList}
            </div>
        )
    }

    content = () => {
        return (
                <>
                    {this.List()}
                </>
            )
    }

    render() {
        return (
            <div className={"scoreboard"}>
                <div className={"title"}>Scoreboard</div>
                {this.state.status === "error" && <Alert type={"warning"} message={this.state.error} />}
                {this.content()}
            </div>
        )
    }
}

export default Scoreboard;