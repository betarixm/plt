interface Team {
    name: string,
    score: number,
    money?: number
}

interface Item {
    id: number
    name: string
    type: string
    description: string
    price: number
    already_bought: boolean
}

interface AttackLog {
    to_team: string;
    is_success: boolean
}

interface TeamInfo {
    teamname: string;
    score: number;
    attacks: {
        SQLi: AttackLog | null;
        XSS: AttackLog | null;
    }
}