interface Team {
    name: string,
    score: number
}

export const login = (id: string, pw: string) => {
    return new Promise<string>((resolve, reject) => {
        resolve("token");
    })
}

export const teamList = () => {
    return new Promise<Array<Team>>((resolve, reject) => {
        resolve([]);
    })
}