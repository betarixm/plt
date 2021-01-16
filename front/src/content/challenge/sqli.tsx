import React from "react"
import Query from "../../component/Query";
import {querySql} from "../../env/api";

interface SqliProps {

}

interface SqliStates {

}

class Sqli extends React.Component<SqliProps, SqliStates> {
    render() {
        return (
            <Query id="sqli" title={"SQL Injection"} onSubmit={querySql} />
        )
    }
}

export default Sqli;