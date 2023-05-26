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
| `from`(optional) | int, string, or null | Defaults to null (includes everything). If int, use epoch time; otherwise, use `YYYY/MM/DD` format. |
| `to`(optional) | int, string, or null | Defaults to null (includes everything). If int, use epoch time; otherwise, use `YYYY/MM/DD` format. |


### Response Fields
| Name | Type | Description |
|---|---|---|
| `deadlines` | array | Array of deadlines |
| `deadlines[n].course_name` | string | The course's name which should be the same as in `GET /api/:lms/classes` |
| `deadlines[n].course_url` | string | The course's URL which should be the same as in `GET /api/:lms/classes` |
| `deadlines[n].name` | string | Name/title of the assigment |
| `deadlines[n].url` | string | URL redirecting to the assignment description. |
| `deadlines[n].timestamp` | int | Epoch time of the deadline, zero if none is specified. |
| `deadlines[n].date` | string | `0` if no deadline specified; otherwise, format is `YYYY-MM-DD`. This makes filtering and sorting the calendar by date easier. |
| `deadlines[n].description` | string | The description of the assignment |
| `deadlines[n].moduletype`<br>(planned) | string | Currently only determined `assign`, `forum`, and possibly one for journal-type submissions in UVLe. TODO: determine the values for google |
| `deadlines[n].platform` | string | Either `uvle` or `gclass`. |

