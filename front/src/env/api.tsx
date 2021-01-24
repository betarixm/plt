import axios from "axios";
import {BACKEND} from "./url";
import Cookies from "universal-cookie";

const cookies = new Cookies();

axios.defaults.withCredentials = true;

export interface ItemListResult {
    XSS: Array<Item>,
    SQLi: Array<Item>
}

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
            cookies.set("sessionid", res.data.sessionid)
            resolve(res)
        }).catch((err) => {
            console.log("sadfasdf")
            if(err.response) {
                if(err.response.status === 400) {
                    reject("비정상적인 지구-접근 코드입니다. 비밀번호는 8글자 이상이어야 합니다.")
                } else if (err.response.status === 401) {
                    reject("해당 지구의 FIREWALL 접근에 실패했습니다.")
                }
            }

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
            reject("지구 생성에 실패했습니다. 다시 시도해주세요.")
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
    return new Promise<ItemListResult>((resolve, reject) => {
       GET_API("/shop/")
           .then((res) => {
               resolve({
                   XSS: res.data.item_list.XSS.map((e: any) => ({
                       ...e, type: "XSS"
                   })),
                   SQLi: res.data.item_list.SQLi.map((e: any) => ({
                       ...e, type: "SQL Injection"
                   }))
               });
           })
           .catch((err) => {
               reject(err.response.data.message);
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
                resolve("정상: FIREWALL 강화에 성공했습니다.");
            })
            .catch((err) => {
                const status = err.response.status;
                if(status === 404) {
                    reject("존재하지 않는 아이템입니다.")
                } else if (status === 409) {
                    reject("이미 구매한 아이템입니다.")
                } else if (status === 402) {
                    reject("ECHO POINT가 부족합니다.")
                } else {
                    reject("예기치 못한 에러입니다. 다시 시도해주세요.")
                }
            })
    })
}

export const querySql = (team: string, query: string) => {
    return new Promise<string>((resolve, reject) => {
        API("/sqli/", {
            query: query,
            team: team
        }).then((res) => {
            if(res.data.success) {
                resolve(res.data.message);
            } else {
                reject(res.data.message);
            }
        }).catch((err) => {
            if(err.response.data.message) {
                reject(err.response.data.message);
            } else {
                reject("예기치 못한 에러가 발생했습니다. 다시 시도해주세요.")
            }
        })
    })
}

export const queryXss = (team: string, query: string) => {
    return new Promise<any>((resolve, reject) => {
        API("/xss/", {
            query: query,
            team: team
        }).then((res) => {
            if(res.data.success) {
                resolve(res.data.message);
            } else {
                reject(res.data.message);
            }
        }).catch((err) => {
            if(err.response.data.message) {
                reject(err.response.data.message);
            } else {
                reject("예기치 못한 에러가 발생했습니다. 다시 시도해주세요.")
            }
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
    return new Promise<number>((resolve, reject) => {
        API("/flag/", {
            flag: flag
        }).then((res) => {
            if(res.data.message) {
                reject(res.data.message)
            } else {
                resolve(res.data.score)
            }
        }).catch((err) => {
            reject(err.toString());
        })
    })
}

export const ping = () => {
    return new Promise<boolean>((resolve, reject) => {
        GET_API("/ping/")
            .then((res) => {
                if(res.data.ok) {
                    resolve(true)
                } else {
                    reject(false)
                }
            })
            .catch((err) => {
                reject(err.toString())
            })
    })
}