import React from "react";

interface AlertProps {
    type: "success"|"warning";
    message: string;
}

interface AlertStates {

}

class Alert extends React.Component<AlertProps, AlertStates> {
    render() {
        return (
            <div className={"alert " + this.props.type}>
                <span className={"material-icons-round"}>
                    {this.props.type === "warning" ? "warning" : ""}
                </span>
                <div className={"message"}>
                    {this.props.message}
                </div>
            </div>
        )
    }
}

export default Alert;