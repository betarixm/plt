export const login = (id: string, pw: string) => {
    return new Promise<string>((resolve, reject) => {
        resolve("token");
    })
}

export const getTeamList = () => {
    return new Promise<Array<Team>>((resolve, reject) => {
        resolve([]);
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