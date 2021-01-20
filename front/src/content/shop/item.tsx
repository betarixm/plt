import React from "react";
import {withRouter, RouteComponentProps} from "react-router-dom";
import {buyItem, getItem} from "../../env/api";
import Loading from "../../component/Loading";
import Alert from "../../component/Alert";

interface ItemParams {
    id: string
}

interface ItemProps extends RouteComponentProps<ItemParams>{

}

interface ItemStates {
    status: "loading" | "input" | "querying" | "success" | "error";
    message?: string;
    error?: string;
}

class ItemInner extends React.Component<ItemProps, ItemStates> {
    state: ItemStates = {
        status: "loading"
    }

    item?: Item;

    componentDidMount() {
        this.setState({
            status: "loading"
        });

        getItem(parseInt(this.props.match.params.id))
            .then((res) => {
                this.item = res;
                this.setState({
                    status: "input"
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

    onSubmit = () => {
        if(this.item) {
            this.setState({
                status: "querying"
            });
            buyItem(this.item.id)
                .then((res) => {
                    this.setState({
                        status: "success",
                        message: res
                    })
                })
                .catch((err) => {
                    this.setState({
                        status: "error",
                        error: err.toString()
                    })
                })
        } else {
            this.setState({
                status: "error",
                error: "잘못된 요청-E"
            })
        }
    }

    Item = () => {
        if(this.item) {
            return (
                <div className={"itemBox"}>
                    <div className={"chips"}>
                        <div className={"chip"}>{this.item.type.toUpperCase()}</div>
                        <div className={"chip"}>{this.item.price} ECHO POINT</div>
                    </div>
                    <div className={"description"}>{this.item.description}</div>
                    <button className={this.state.status === "querying" ? "disabled" : ""} onClick={this.onSubmit}>{this.state.status === "querying" ? this.item.name + " 다운로드 및 장착 시도 중..." : "구매"}</button>
                </div>
            )
        }

    }

    content = () => {
        if(this.state.status === "loading") {
            return (
                <Loading description={"아이템 정보 다운로드 중..."} />
            )
        } else {
            return (
                <>
                    {this.Item()}
                </>
            )
        }
    }

    render() {
        return (
            <div className={"item"}>
                <div className={"title"}>{this.item ? this.item.name : "ITEM"}</div>
                {this.state.status === "error" && <Alert type={"warning"} message={this.state.error}/>}
                {this.state.status === "success" && <Alert type={"success"} message={this.state.message}/>}
                {this.content()}
            </div>
        )
    }
}

const Item = withRouter(ItemInner);

export default Item;