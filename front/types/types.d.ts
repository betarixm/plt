interface Team {
    username: string,
    score: number,
    money?: number
}

interface Item {
    id: number,
    name: string,
    type: "sqli"|"xss",
    description: string,
    price: number
}