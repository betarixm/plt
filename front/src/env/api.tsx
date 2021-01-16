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
        }, {
            id: "test3", name: "test3", score: 200
        }, {
            id: "test4", name: "test4", score: 200
        }, {
            id: "test5", name: "test5", score: 200
        }, {
            id: "test6", name: "test6", score: 200
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
        reject("해당 지구로 쓰레기를 투기하는데 실패했습니다.");
    })
}

export const queryXss = (token: string, team: string, query: string) => {
    return new Promise<any>((resolve, reject) => {
        resolve("success");
    })
}