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
                        status: "success"
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
                <>
                    <div>{this.item.name}</div>
                    <div>{this.item.description}</div>
                    <button onClick={this.onSubmit}>구매</button>
                </>
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
                <div>
                    {this.state.status === "error" && <Alert type={"warning"} message={this.state.error}/>}
                    {this.Item()}
                </div>
            )
        }
    }

    render() {
        return (
            <>
                <div>ITEM</div>
                {this.content()}
            </>
        )
    }
}

const Item = withRouter(ItemInner);

export default Item;