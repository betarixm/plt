interface Team {
    id: string,
    name: string,
    score?: number
}

interface Item {
    id: number,
    name: string,
    type: "sqli"|"xss",
    description: string,
    price: number
}