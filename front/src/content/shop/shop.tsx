import React from "react";
import {Link} from "react-router-dom";
import {getItemList} from "../../env/api";
import {GET_PATH_ITEM} from "../../env/path";
import Loading from "../../component/Loading";

interface ShopProps {

}

interface ShopStates {
    status: "loading"|"error"|"done";
    error?: string;
}

class Shop extends React.Component<ShopProps, ShopStates> {
    state: ShopStates = {
        status: "loading"
    }
    itemList: Array<Item> = [];

    componentDidMount = () => {
        this.setState({
            status: "loading"
        });
        getItemList()
            .then((res) => {
                this.itemList = res;
                this.setState({
                    status: "done"
                })
            })
            .catch((err) => {
                this.setState({
                    status: "error",
                    error: err.toString()
                })
            })
    }

    componentWillUnmount = () => {

    }

    content = () => {
        if(this.state.status === "loading") {
            return (
                <Loading description={"BnL 아이템 리스트를 불러오는 중..."} />
            )
        } else {
            const Items = this.itemList.map((item, index) => {
                return (
                    <div key={index} className={"item"}>
                        <div className={"info"}>
                            <div className={"name"}>{item.name}</div>
                            <div className={"type"}>{item.type}</div>
                        </div>
                        <div className={"wrapper"}>
                            <div> </div>
                            <Link to={GET_PATH_ITEM(item.id)}>{item.price} <span className={"material-icons-round"}>shopping_cart</span></Link>
                        </div>
                    </div>
                )
            })

            return(
                <div className={"shopBox"}>
                    {Items}
                </div>
            )
        }

    }

    render = () => {
        return (
            <div className={"shop"}>
                <div className={"reserved"}> </div>
                <div className={"title"}>Shop</div>
                {this.content()}
                <div className={"reserved"}> </div>
            </div>
        )
    }
}

export default Shop;