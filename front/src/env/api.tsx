export const getSession = () => {
    localStorage.getItem('token');
}

export const setSession = (token: string) => {
   localStorage.setItem('token', token);
}

export const login = (id: string, pw: string) => {
    return new Promise<string>((resolve, reject) => {
        setTimeout(() => {
            reject("해당 지구에는 접근할 수 없습니다!")
        }, 2000);
    });
}

export const register = (id: string, pw: string, name: string) => {
    return new Promise<any>((resolve, reject) => {
        setTimeout(() => {
            reject("token")
        }, 2000);
    });
}

export const getTeamList = () => {
    return new Promise<Array<Team>>((resolve, reject) => {
        resolve([{
            id: "test1", name: "test1", score: 100
        }, {
            id: "test2", name: "test2", score: 200
        }]);
    })
}

export const getItemList = () => {
    return new Promise<Array<Item>>((resolve, reject) => {
        resolve([{
            id: 3, name: "item name", description: "item des", type: "sqli"
        }])
    })
}

export const getItem = (id: number) => {
    return new Promise<Item>((resolve, reject) => {
        resolve({
            id: 3, name: "item name", description: "item", type: "xss"
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
        reject("success");
    })
}

export const queryXss = (token: string, team: string, query: string) => {
    return new Promise<any>((resolve, reject) => {
        resolve("success");
    })
}