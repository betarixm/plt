export const getSession = () => {
    localStorage.getItem('token');
}

export const setSession = (token: string) => {
   localStorage.setItem('token', token);
}

export const login = (id: string, pw: string) => {
    return new Promise<string>((resolve, reject) => {
        setTimeout(() => {
            resolve("token")
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

export const querySql = (token: string, team: string, query: string) => {
    return new Promise<any>((resolve, reject) => {
        resolve("success");
    })
}

export const queryXss = (token: string, team: string, query: string) => {
    return new Promise<any>((resolve, reject) => {
        resolve("success");
    })
}