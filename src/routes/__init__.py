"""

--------------------------------------------------------------------------------
Purpose of __init__.py
--------------------------------------------------------------------------------
1) Marks a Directory as a Package:
The presence of a __init__.py file in a directory tells Python that the directory should be treated as a package. 
This is necessary for importing modules or sub-packages from that directory.

2) The __init__.py file can include code to initialize the package or define what gets imported when you use `from package import *`

--------------------------------------------------------------------------------
Example Project Structure:
--------------------------------------------------------------------------------

my_project/
│
├── routes/
│   ├── __init__.py
│   ├── user_routes.py
│   ├── admin_routes.py
│
├── main.py

Code in routes/user_routes.py:
```
def get_user():
    return "User Route: Get User"
```

Code in routes/admin_routes.py:
```
def get_admin():
    return "Admin Route: Get Admin"
```

code in routes/__init__.py:
```
from .user_routes import get_user
from .admin_routes import get_admin

# Specify what gets imported when using "from routes import *"
__all__ = ["get_user", "get_admin"]
```

Finally using the Code in main.py [with help of __init__.py]:
```
# Importing from the `routes` package
from routes import get_user, get_admin
```

Code in main.py [Without __init__.py]:
```
from routes.user_routes import get_user
from routes.admin_routes import get_admin
```

--------------------------------------------------------------------------------
Key Difference
--------------------------------------------------------------------------------
Without __init__.py: Import each module individually.
With __init__.py: Import the entire package and access its components directly.

--------------------------------------------------------------------------------
Terminology Overview:
--------------------------------------------------------------------------------
1) Package: 
- A directory containing a special file called __init__.py (optional in Python 3.3+).
- A package can contain modules (files) or sub-packages (nested directories).

2) Sub-package:
- A directory within a package, treated as a package itself, also containing a special file called __init__.py (optional in Python 3.3+).

3) Module:
- A single .py file containing Python code (functions, classes, or variables).

4) Sub-Module:
- A .py file (module) that resides inside a package.
- It is essentially the same as a module, but we call it a sub-module to indicate its relation to a package.
- So the sub-module is just a module that is part of a package.
- If the module is standalone (not inside a package), we simply call it a module.

my_package/
├── __init__.py
├── sub_module1.py  # This is a sub-module
├── sub_module2.py  # This is another sub-module

Example Project and Terms:

my_project/                # Not a package (no __init__.py)
│
├── routes/                # Package
│   ├── __init__.py        # Initializes the package
│   ├── user_routes.py     # Module in the routes package.
│   ├── admin_routes.py    # Module in the routes package.
│
├── models/                # Package
│   ├── __init__.py        # Initializes the package
│   ├── user_model.py      # Module in the models package.
│   ├── product_model.py   # Module in the models package.

--------------------------------------------------------------------------------
Implicit Namespace Packages in Python 3.3+
--------------------------------------------------------------------------------
In Python 3.3 and later, you can create a package without including an __init__.py file in the directory. 
This is because Python now supports implicit namespace packages.

You don’t need special arrangements to use implicit namespace packages.
Just place .py files in a directory, ensure it’s in the module search path, and avoid adding __init__.py.
And python will treat that directory as a package automatically in Python 3.3+.
- Note: Python 3.3 was released on September 29, 2012.

What Does This Mean?
- Before Python 3.3: A directory must have an __init__.py file to be treated as a package.
- Python 3.3 and Later: A directory can be treated as a package even without __init__.py.

However, adding __init__.py is still useful and common for:
- Explicit Initialization: Run setup code when the package is imported.
- Grouping Imports: Simplify and manage imports within the package.
- Backward Compatibility: Support older Python versions.

"""



from .base import base_router
from .data import data_router