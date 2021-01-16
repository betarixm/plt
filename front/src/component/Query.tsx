import React from 'react'
import Loading from "./Loading";
import {getTeamList} from "../env/api";

interface QueryProps {
    title: string;
    id?: string;

    onSubmit(token: string, team: string, query: string): Promise<any>;
}

interface QueryStates {
    status: "loading" | "error" | "input" | "querying" | "done";
    error?: string;
    target?: string;
    result?: string;
    query?: string;
}

class Query extends React.Component<QueryProps, QueryStates> {
    state: QueryStates = {
        status: "loading"
    };

    teamList: Array<Team> = [];

    componentDidMount() {
        getTeamList()
            .then((res) => {
                this.teamList = res;
                this.setState({
                    status: "input"
                })
            })
            .catch((err) => [
                this.setState({
                    status: "error",
                    error: err.toString()
                })
            ]);
    }

    componentWillUnmount() {

    }

    onSubmit = () => {
        this.props.onSubmit("", "", "")
            .then((res) => {
                this.setState({
                    status: "done"
                });
            })
            .catch((err) => {
                this.setState({
                    error: err.toString()
                })
            })
    }

    onTeamSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
        this.setState({
            target: e.target.value
        });
    }

    onQueryChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        this.setState({
            query: e.target.value
        })
    }

    TeamSelector = () => {
        const teamRadio = this.teamList.map((team, index) => {
            const id = "teamRadio" + index.toString();
            return (
                <div key={team.id} className={"radio"}>
                    <input type={"radio"} id={id} name="team" value={team.id} onChange={this.onTeamSelect}
                           checked={this.state.target === team.id}/>
                    <label htmlFor={id}>{team.name}</label>
                </div>
            )
        });

        return (
            <div className={"teamSelector"}>
                {teamRadio}
            </div>
        )
    }

    Input = () => {
        return (
            <div className={"queryForm"}>
                <input className={"query"} type={"text"} onChange={this.onQueryChange} value={this.state.query}/>
                {this.TeamSelector()}
            </div>
        );
    }

    content = () => {
        if (this.state.status === "loading") {
            return (
                <Loading description={"다른 행성의 취약점 정보 수집 중..."}/>
            );
        } else {
            return (
                <>{this.Input()}</>
            );
        }
    }

    render() {
        return (
            <>
                <div className={"title"}>
                    {this.props.title}
                </div>
                {this.content()}
            </>
        );
    }
}

export default Query;