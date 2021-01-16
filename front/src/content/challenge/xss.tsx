import React from "react"
import Query from "../../component/Query";
import {queryXss} from "../../env/api";

interface XssProps {

}

interface XssStates {

}

class Xss extends React.Component<XssProps, XssStates> {
    render() {
        return (
            <Query id="xss" title={"XSS"} onSubmit={queryXss} />
        )
    }
}

export default Xss;