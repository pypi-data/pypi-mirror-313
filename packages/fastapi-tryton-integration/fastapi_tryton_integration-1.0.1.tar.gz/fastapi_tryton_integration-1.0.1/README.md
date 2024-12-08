# fastapi-tryton-integration

This package was created from the `fastapi-tryton-async <https://github.com/TinKurbatoff/fastapi-tryton-async>`_ repository developed by Constantine K.

Modifications and adaptations have been made to meet new requirements and extend its functionality.

## Key Benefits of the Current Codebase:

- **Improved Asynchronous Support**: Full compatibility with FastAPI’s asynchronous event loop.
- **Reduced Complexity**: Streamlined code by removing non-essential components.
- **Better Logging**: More detailed logs for transactions and error handling.
- **Focused Functionality**: A lighter, more focused API for Tryton-FastAPI integration.
- **Encouragement of Modern Practices**: Simplified testing and configuration align with modern Python development standards.


Install:
```
pip3 install fastapi-tryton-integration
```

Usage:
```
from fastapi import FastAPI
from fastapi import Request
from fastapi_tryton_integration import Tryton
from fastapi_tryton_integration import options

options.config['TRYTON_DATABASE'] = "my_database"  # What exact database name
options.config['TRYTON_CONFIG'] = "/etc/tryton.conf" # path to configuration file
options.config['TRYTON_CONNECTION'] = "postgresql://user:my_secret_password@localhost:5432"

app = FastAPI()

try:
    tryton = Tryton(options, configure_jinja=True)
except Exception as e:
    logger.error(f"Cannot initialize Tryton ERP: {e}")
    exit()
User = tryton.pool.get('res.user')  # Important class type - User

# ——— API endpoints
@app.post(f"/hello/")  
@tryton.transaction(readonly=False)
async def hello(request: Request):  # (request: Request) — required!
    user, = User.search([('login', '=', 'admin')])
    return '%s, Hello World!' % user.name

...

```
*NOTE*: request (fastapi Request class) not always is required for the decorated function parameters.

There are three configuration options available:

TRYTON_DATABASE: the Tryton’s database to connect.

TRYTON_USER: the Tryton user id to use, by default 0 (aka root).

TRYTON_CONFIG: the optional path to the Tryton’s configuration.

TRYTON_CONNECTION: full path (uri) to the database
