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
  "username" : string,
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
POST /Login
```
| Parameter | Type | Description |
| :--- | :--- | :--- |
| `username` | `string` |  |
| `password` | `string` |  |

**Response:** 
- Invalid Form : 400
- Login Failed : 401
- Success : 200

See `Set-Cookie` header!


### Dashboard
```http
GET /dashboard
```
| Parameter | Type | Description |
| :--- | :--- | :--- |

**Response:** 
```javascript
{
  "<teamname1>" : {
      "score" : int
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
}
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
