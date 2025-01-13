"""

Advantages of using APIRouter class for routing over FastAPI(that is defined in main.py):

1) Modularity: Using APIRouter allows you to define multiple routers for different parts of your application 
(e.g., users_router, auth_router, products_router). This makes it easy to separate functionality into modules.
- group related endpoints (e.g., user_routes, products_router) into separate routers for better code organization.

2) Reusability: You can define routers in different files/modules and include them in the main FastAPI app,
improving code organization ().

3) When you want to apply specific features like prefixes, tags, or dependencies to a group of routes.

Use APIRouter for Modular Applications: If you expect your application to grow, need separate modules, 
or want better organization, APIRouter is the better choice. It aligns with best practices for scalable applications.

--------------------------------------------------------------------------------

When to Use FastAPI for Routing Directly?
- If you have a small or simple application with a few routes, you can use FastAPI directly for routing.
- For quick prototypes or minimalistic APIs.

Example:
```
from fastapi import FastAPI       

# Create an instance(object) of the FastAPI class
app = FastAPI() 

@app.get("/")
async def welcome():
    return {"message": "Welcome to RAG-APP"}
    
@app.get("/login")
async def login():
    # Logic for login
    
@app.get("/products")
async def get_products():
    # Logic for getting products
```

Note that here, we use FastAPI class directly for routing instead of using APIRouter class, so
all the routes can be defined directly in the main FastAPI app which is not a good practice for larger applications.

"""




from fastapi import APIRouter, Depends       
from helpers.config import Settings, get_settings

# Create an instance(object) of the APIRouter class
base_router = APIRouter(
    prefix="/api/v1", # use the /api/v1 prefix for all routes in this file
    tags=["api_v1"],  
)


# Defone endpoint to handle the welcome request
@base_router.get("/")   # The path or endpoint is relative to the prefix "/api/v1" defined above
async def welcome(app_settings: Settings = Depends(get_settings)): # the use of async is optional, but recommended for better performance.

    
    app_name = app_settings.APP_NAME
    app_version =  app_settings.APP_VERSION
    app_description = app_settings.APP_DESCRIPTION
    app_author = app_settings.APP_AUTHOR
    
    # Return a customized JSON response
    return {
        "message": f"Welcome to {app_name}!", # A welcome message
        "details": {
            "name": app_name, # The app name
            "version": app_version, # The app version
            "description": app_description, # The app description
            "author": app_author # The app author
        },
        "note": "Thank you for using our application. If you have any questions, feel free to reach out to our support team."
    }



"""
In the above welcome() function, the function reads environment variables, which is very fast and not I/O-bound, 
so async isn’t strictly necessary here. However, it's good practice in case the function grows to include I/O operations later.

Even if the function doesn’t currently need async, using it ensures consistency across your FastAPI application.
And is a Good practice as It aligns with FastAPI's design and prepares your application for future scalability.
If you later add asynchronous calls (e.g., database queries or network requests) inside the function, you won’t need to refactor it.

With async, FastAPI can handle more requests simultaneously. If this route were part of a larger application, asynchronous programming would prevent blocking other routes.

--------------------------------------------------------------------------------
If you use a regular def function instead of async def:
--------------------------------------------------------------------------------
FastAPI can still handle it, but the route will block the server thread while executing.
This means other requests will have to wait if the function takes time (e.g., long computations or I/O).

"""





"""
--------------------------------------------------------------------------------
What is Depends in FastAPI?
--------------------------------------------------------------------------------
In FastAPI, Depends is a function provided by the framework to enable dependency injection mechanism. 
Dependency injection mechanism is a design pattern where objects or functions that a route (or function) depends on are "injected" automatically by the framework.
Dependencies are external requirements that your route or function needs to work properly.

What Does the Word "Depends" Mean?
- The word Depends literally means "something that is required" or "something your code depends on to work." 
- In FastAPI, it's used to define these requirements (dependencies) for your functions.

Why Is It Called Depends?
The name reflects the purpose:
- It declares dependencies for a route or function.
- These dependencies are something your route or function "depends" on to perform its task.

How Does It Work?
When you use Depends, you're telling FastAPI:
1) "I need this function (or object) to provide data or perform a task."
2) FastAPI will:
- Automatically call the dependency function.
- Pass its result into your route or function.

Dependencies can be anything your application requires, such as:
- Configurations (e.g., settings or environment variables)
- Database connections
- Security/authentication
- Business logic
- Preprocessing or validation logic

--------------------------------------------------------------------------------
How Depends Works in the above welcome() function
--------------------------------------------------------------------------------
1) When a user sends a GET request to /api/v1/, FastAPI calls the welcome function.
2) Before calling welcome, FastAPI sees that welcome has a dependency: Depends(get_settings).
3) FastAPI automatically calls get_settings() and passes the resulting Settings object to the app_settings parameter.
4) Inside the welcome function, you can now use app_settings to access the app configuration (e.g., APP_NAME, APP_VERSION, etc).

--------------------------------------------------------------------------------
Why use Depends?
--------------------------------------------------------------------------------
1) Code Reusability:
- Avoid repeating logic like reading settings, validating users, or initializing resources in multiple routes.
- Without Depends, you need to manually call the dependency function inside every route.

2) Clean Code:
- The dependency is injected as a parameter, making your route handlers simpler and easier to read.
- It helps keep your route handlers clean and focused on their primary tasks.

3) Caching:
- If get_settings() is decorated with @lru_cache, FastAPI ensures that the settings are created only once, and the same object is reused for every request.

4) Flexibility:
- Depends works with functions, classes, or even asynchronous logic, making it highly flexible.

5) Automatic Validation:
- If the dependency function has its own validations or requirements (e.g., checking environment variables), FastAPI will validate them before calling the route.


--------------------------------------------------------------------------------
What Happens Without Depends?
--------------------------------------------------------------------------------
If you don’t use Depends, you would need to manually call get_settings()
```
@base_router.get("/")  
async def welcome():
    app_settings = get_settings()  # Manually call the function
    app_name = app_settings.APP_NAME
    app_version = app_settings.APP_VERSION
    .....
```
No built-in caching or dependency injection features.
"""





"""
--------------------------------------------------------------------------------
For more readability:
--------------------------------------------------------------------------------
Instead of using this syntax: `welcome(app_settings = Depends(get_settings)):`

we use the following syntax: `welcome(app_settings: Settings = Depends(get_settings)):`
So we can make the code more readable, as when i see the get_settings function, i know that it returns a Settings object,
and i easly search or go to Settings class to know what it does or what it returns for example if i don't know or remember.

The difference between these two declarations lies in type annotations and explicitness, 
and the better choice depends on your use case. Here's a breakdown of each approach and their names:

--------------------------------------------------------------------------------
1) app_settings = Depends(get_settings)
--------------------------------------------------------------------------------
This is a simple way to declare a dependency without specifying the type of the argument. 
It uses the Depends function directly to inject the result of get_settings into the app_settings parameter.

Key Features:
- No Type Annotation: The app_settings parameter does not explicitly declare its type.
- Implicit Typing: The type of app_settings is inferred based on what get_settings returns.
- Common Use Case: This is acceptable when type checking or validation is not critical.

Pros:
- Shorter and simpler to write.
- Useful for cases where you don't need strong type hints.

Cons:
- Less Explicit: The type of app_settings is not immediately clear without looking at get_settings.
- Might confuse developers unfamiliar with the codebase.

--------------------------------------------------------------------------------
2) app_settings: Settings = Depends(get_settings)
--------------------------------------------------------------------------------
This explicitly declares the type of the app_settings parameter (Settings) and assigns it a dependency (Depends(get_settings)).

Key Features:
- Type Annotation: app_settings is explicitly declared as Settings.
- Explicit Typing: The parameter's type is immediately clear.
- Preferred for Clarity: This is considered best practice in most cases.

Pros:
- Improves code readability and maintainability.
- Makes it easier for tools (e.g., linters, IDEs, type checkers) to validate the type and catch errors.
- Useful when working in teams or with complex projects.

Cons:
- Slightly longer to write.

--------------------------------------------------------------------------------
What Are These Ways of Declaration Called?
--------------------------------------------------------------------------------
Both methods are part of Python's function parameter declaration. Here are the key terms:

1) Without Type Annotation (app_settings = Depends(...)):
- This is a parameter with a default value (using Depends as the default).
- The type is inferred dynamically.

2) With Type Annotation (app_settings: Settings = Depends(...)):
- This is a type-annotated parameter with a default value.
- The Settings annotation explicitly declares the expected type.

--------------------------------------------------------------------------------
Which Is Better?
--------------------------------------------------------------------------------
The second approach (app_settings: Settings = Depends(get_settings)) is generally better because:
1) Explicit Is Better Than Implicit: It's a fundamental principle in Python programming (PEP 20, The Zen of Python).
2) Type Safety: It helps you and others understand what type the app_settings parameter is supposed to be.
3) Integration with Tools:
  - IDEs like VSCode can provide better autocompletion and hints.
  - Static type checkers (like mypy) can validate types and catch errors.

--------------------------------------------------------------------------------
Conclusion:
--------------------------------------------------------------------------------
-> Use app_settings = Depends(get_settings) for quick prototypes or simple cases where type clarity isn't critical.
-> Use app_settings: Settings = Depends(get_settings) in production code, team projects, or complex applications, as it's more explicit and readable.

--------------------------------------------------------------------------------
Explicit Is Better Than Implicit: It's a fundamental principle in Python programming (PEP 20, The Zen of Python).
--------------------------------------------------------------------------------
This sentence refers to a guiding principle in Python development that comes from PEP 20 (The Zen of Python). 
This principle emphasizes that code should be clear and easy to understand, even if it takes a little more effort to write.

Explicit: This means being clear, specific, and unambiguous. 
When something is explicit, it's directly stated or defined, leaving no room for assumptions.

Implicit: This means something is implied, inferred, or not directly stated. 
While it might save time or effort initially, it can make the code harder to understand.

In programming, being explicit often involves:
1) Writing code that clearly shows its intention.
2) Using type annotations or descriptive variable names.
3) Avoiding "magic" or assumptions that others may not understand.

Why Does This Matter in Python?
Python emphasizes readability and maintainability. 
Code is often read more times than it's written, so making it clear for others (and your future self!) is crucial. 

By being explicit, you:
1) Reduce the chances of misunderstandings.
2) Make your code easier to debug and maintain.
3) Help other developers (or tools like linters) understand your intent.

Here’s an example comparing implicit and explicit code:
1) Implicit: 
`settings = Depends(get_settings)`
- The type of settings is not clear unless you check the get_settings function.
- Another developer (or you, after a while) may not immediately understand what settings represents.

2)Explicit:
`app_settings: Settings = Depends(get_settings)`
- The type of settings is explicitly stated as Settings.
- It's immediately clear what type of object settings will be.
"""

