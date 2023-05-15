Below are a list of the current endpoints

# Display Endpoints
## `GET /link/:lms_name`
Renders `templates/lms/login-<lms_name>.html`.

## `GET /login`
If the user is already logged in, redirects to `/dashboard`; otherwise, renders `templates/login.html`.

# Other Endpoints
TODO: Sort other endpoints into categories

## `GET /logout`
Logs out the currently logged in user and redirects to `/login`.

## `GET /unlink/:lms_name`
Unlinks the accounts from `lms_name` under the currently logged in user.

## `POST /link/:lms_name`
Links a UVL&ecirc; account to the currently logged in user. 
### JSON body parameters
| Name | Type | Description |
|---|---|---|
| `credentials`<br>(required) | string | The username and password of the account to be linked joined together with a colon, e.g. `"username:password"`.<br>~~TODO: Encrypt the credentials with the public key before sending.~~ |

## `GET /api/:lms/classes`
TODO: Returns a JSON. `lms` can be either `gclass` or `uvle`.
### Response Fields
| Name | Type | Description |
|---|---|---|
| `courses`                | array  | Array of classes |
| `courses[n].id`          | string | Course ID |
| `courses[n].name`        | string | Name of the course |
| `courses[n].url`         | string | URL to the course |
| `courses[n].description` | string | Description |

## `POST /api/:lms/deadlines`
TODO: Returns the deadlines in `:lms`. Allows you to filter by date, inclusive.

### JSON body parameters
| Name | Type | Description |
|---|---|---|
| `from`(optional) | int or string | If int, use epoch time; otherwise, use `YYYY/MM/DD` format. |
| `to`(optional) | int or string | If int, use epoch time; otherwise, use `YYYY/MM/DD` format. |

### Response Fields
| Name | Type | Description |
|---|---|---|
| `deadlines` | dict  | Array of deadlines |
| `deadlines[n].name` | string | Name/title of the assigment |
| `deadlines[n].url` | string | URL redirecting to the assignment description. |
| `deadlines[n].timestamp` | int | Epoch time of the deadline, zero if none is specified. |
| `deadlines[n].date` | string or null | If a string, format is `YYYY/MM/DD`; otherwise, the requirement has no deadline specified. This makes filtering and sorting the calendar by date easier. |

