# api

## base
### Home
```http
GET /
```
| Parameter | Type | Description |
| :--- | :--- | :--- |
| `token` | `string` | Your token |

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
201 / 400

### Login
```http
POST /Login
```
| Parameter | Type | Description |
| :--- | :--- | :--- |
| `username` | `string` |  |
| `password` | `string` |  |

**Response:** 
200 / 400, 401

See `Set-Cookie` header!


### Dashboard
```http
GET /dashboard
```
| Parameter | Type | Description |
| :--- | :--- | :--- |
| `username` | `string` |  |
| `password` | `string` |  |

**Response:** 
200 / 400, 401

