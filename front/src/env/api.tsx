import axios from "axios";
import {BACKEND} from "./url";
import Cookies from "universal-cookie";

const cookies = new Cookies();

axios.defaults.withCredentials = true;

export const API = (url: string, data: object) => {
    return axios.post(`${BACKEND}${url}`, data, {
        withCredentials: true,
    })
}

export const GET_API = (url: string) => {
    return axios.get(`${BACKEND}${url}`, {
        withCredentials: true,
    })
}

export const getSession = () => {
    localStorage.getItem('sessionid');
}

export const setSession = (token: string) => {
   localStorage.setItem('sessionid', token);
}

export const login = (id: string, pw: string) => {
    return new Promise<any>((resolve, reject) => {
        API("/login/", {
            username: id,
            password: pw
        }).then((res) => {
            setSession(res.data.sessionid);
            cookies.set("sessionid", res.data.sessionid, {
                domain: ".postech.studio"
            });
            resolve(res)
        }).catch((err) => {
            if(!err) {
                err = "비정상적인 지구-접근 코드입니다."
            }
            reject(err.toString())
        })
    });
}

export const register = (email: string, password: string, username: string) => {
    return new Promise<any>((resolve, reject) => {
        API("/register/", {
            username: username,
            password: password,
            email: email
        }).then((res) => {
            resolve(res);
        }).catch((err) => {
            if(!err) {
                err = "에러 "
            }
            reject(err.toString());
        })
    });
}

export const getTeamList = () => {
    return new Promise<Array<Team>>((resolve, reject) => {
        resolve([{
            username: "test1", score: 100
        }, {
            username: "test2", score: 200
        }, {
            username: "test3", score: 200
        }, {
            username: "test4", score: 200
        }, {
            username: "test5", score: 200
        }, {
            username: "test6", score: 200
        }]);
    })
}

export const getItemList = () => {
    return new Promise<Array<Item>>((resolve, reject) => {
        resolve([{
            id: 3, name: "iaaaatem name", description: "item des", type: "sqli", price: 3000
        }, {
            id: 3, name: "item name", description: "item des", type: "sqli", price: 3000
        }, {
            id: 3, name: "item name", description: "item des", type: "sqli", price: 3000
        }, {
            id: 3, name: "item name", description: "item des", type: "sqli", price: 3000
        }, {
            id: 3, name: "iaaaatem name", description: "item des", type: "sqli", price: 3000
        }, {
            id: 3, name: "item name", description: "item des", type: "sqli", price: 3000
        }, {
            id: 3, name: "item name", description: "item des", type: "sqli", price: 3000
        }, {
            id: 3, name: "item name", description: "item des", type: "sqli", price: 3000
        }, {
            id: 3, name: "iaaaatem name", description: "item des", type: "sqli", price: 3000
        }, {
            id: 3, name: "item name", description: "item des", type: "sqli", price: 3000
        }, {
            id: 3, name: "item name", description: "item des", type: "sqli", price: 3000
        }, {
            id: 3, name: "item name", description: "item des", type: "sqli", price: 3000
        }])
    })
}

export const getItem = (id: number) => {
    return new Promise<Item>((resolve, reject) => {
        resolve({
            id: 3, name: "item name", description: "item", type: "xss", price: 3000
        })
    })
}

export const buyItem = (id: number) => {
    return new Promise<any>((resolve, reject) => {
        resolve("success");
    })
}

export const querySql = (token: string, team: string, query: string) => {
    return new Promise<any>((resolve, reject) => {
        resolve("해당 지구로 쓰레기를 투기하는데 실패했습니다.");
    })
}

export const queryXss = (token: string, team: string, query: string) => {
    return new Promise<any>((resolve, reject) => {
        resolve("success");
    })
}

export const getUserInfo = () => {
    return new Promise<Team>((resolve, reject) => {
        GET_API("/")
            .then((res) => {
                resolve(res.data);
            })
            .catch((err) => {
                reject(err.toString());
            })
    })
}

export const authFlag = (flag: string) => {
    return new Promise<any>((resolve, reject) => {
        resolve("success");
    })
}