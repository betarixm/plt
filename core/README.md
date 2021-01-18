# api

## base
### Home
```http
GET /
```
| Parameter | Type | Description |
| :--- | :--- | :--- |

need token
**Response:** 
```javascript
{
  "name" : string,
  "score" : int,
  "money" : int
}
```

### Register
```http
POST /register
```
| Parameter | Type | Description |
| :--- | :--- | :--- |
| `username` | `string` |  |
| `password` | `string` |  |
| `email` | `string` |  |

**Response:** 
- Invalid Form : 400
- Success : 201

### Login
```http
POST /login
```
| Parameter | Type | Description |
| :--- | :--- | :--- |
| `username` | `string` |  |
| `password` | `string` |  |

**Response:** 
- Invalid Form : 400
- Login Failed : 401
- Success : 200
```javascript
{
  "sessionid" : string
}
```


### Dashboard
```http
GET /dashboard
```
| Parameter | Type | Description |
| :--- | :--- | :--- |

**Response:** 
```javascript
[
    {
        "teamname" : str,
        "score" : int,
        "attacks" : {
            "SQLi" : {
                "to_team" : string,
                "is_success" : bool
            }
            "XSS" : {
                "to_team" : string,
                "is_success" : bool
            }
        }
    },
    ...
]
```


## Shop
### Shop
```http
GET /shop
```
| Parameter | Type | Description |
| :--- | :--- | :--- |

needs token
**Response:** 
```javascript
{
    "money" : int,
    "item_list" : {
        "SQLi" : array
        "XSS" : array
    }
}
```
array of 
```javascript
{"name": x.title,"id": x.id, "price": x.price, "already_bought": x.already_bought}```

### Item_Info
```http
GET /shop/<item_id>
```
| Parameter | Type | Description |
| :--- | :--- | :--- |

needs token
**Response:** 
```javascript
{
    "id" : int,
    "name" : string,
    "description" : string,
    "type" : string,
    "price" : int,
    "already_bought" : bool
}
```
type is... `sqli` or `xss`

### Item_Buy
```http
POST /shop/<item_id>
```
| Parameter | Type | Description |
| :--- | :--- | :--- |

needs token
**Response:** 
- No Such Item : 404
- Already Bought : 409
- Not Enough balance : 402
- Success : 200


## Flag
### Auth
```http
POST /flag/
```
| Parameter | Type | Description |
| :--- | :--- | :--- |
| `flag` | `string` |  |

needs token
**Response:** 
- Invalid Form : 400
- No Such Flag : 404
- Success : 200
```javascript
{
    "score" : int
}
```


## SQLi
### Query
```http
POST /sqli/
```
| Parameter | Type | Description |
| :--- | :--- | :--- |
| `query` | `string` |  |
| `team` | `string` |  |

needs token
**Response:** 
- "Invalid Form" : 400
- "Attacked yourself" : 400
- "No Such Team" : 404
- "Too Long Query" : 400
- "Blocked by Regex" : 400
- Success : 200 -> with results!
```javascript
{
    'success': success,
    'message': result
}
```

## XSS
### Query
```http
POST /xss/
```
| Parameter | Type | Description |
| :--- | :--- | :--- |
| `query` | `string` |  |
| `team` | `string` |  |

needs token
**Response:** 
- "Invalid Form" : 400
- "Please wait {sec}seconds" : 400
- "Attacked yourself" : 400
- "No Such Team" : 404
- "Too Long Query" : 400
- "Blocked by Regex" : 400
- Success : 200 -> with FLAG!
```javascript
{
    'success': success,
    'message': result
}
```

