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
            cookies.set("sessionid", res.data.sessionid);
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
    return new Promise<Array<TeamInfo>>((resolve, reject) => {
        GET_API("/dashboard/")
            .then((res) => {
                resolve(res.data);
            })
            .catch((err) => {
                reject(err);
            })
    })
}

export const getItemList = () => {
    return new Promise<Array<Item>>((resolve, reject) => {
       GET_API("/shop/")
           .then((res) => {
               resolve(res.data.item_list.SQLi + res.data.item_list.XSS);
           })
           .catch((err) => {
               reject(err.toString());
           })
    })
}

export const getItem = (id: number) => {
    return new Promise<Item>((resolve, reject) => {
        GET_API(`/shop/${id}/`)
            .then((res) => {
                resolve(res.data)
            })
            .catch((err) => {
                reject(err.toString());
            })
    })
}

export const buyItem = (id: number) => {
    return new Promise<any>((resolve, reject) => {
        API(`/shop/${id}/`, {})
            .then((res) => {
                resolve(res);
            })
            .catch((err) => {
                reject(err.toString())
            })
    })
}

export const querySql = (team: string, query: string) => {
    return new Promise<any>((resolve, reject) => {
        API("/sqli/", {
            query: query,
            team: team
        }).then((res) => {
            resolve(res.data)
        }).catch((err) => {
            reject(err.toString())
        })
    })
}

export const queryXss = (team: string, query: string) => {
    return new Promise<any>((resolve, reject) => {
        API("/xss/", {
            query: query,
            team: team
        }).then((res) => {
            resolve(res.data)
        }).catch((err) => {
            reject(err.toString())
        })
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
        API("/flag/", {
            flag: flag
        }).then((res) => {
            resolve(res);
        }).catch((err) => {
            reject(err.toString());
        })
    })
}