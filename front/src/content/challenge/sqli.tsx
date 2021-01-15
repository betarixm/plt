import React from 'react'
import Loading from "../../component/Loading";

interface SqliProps {

}

interface SqliStates {
    status: "loading";
}

class Sqli extends React.Component<SqliProps, SqliStates> {
    state: SqliStates = {
        status: "loading"
    };

    componentWillUnmount() {

    }

    render() {
        if(this.state.status === "loading") {
            return (
                <Loading description={"다른 행성의 취약점 정보 수집 중..."} />
            )
        }
        return undefined;
    }
}

export default Sqli;