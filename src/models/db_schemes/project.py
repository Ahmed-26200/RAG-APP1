from pydantic import BaseModel, Field, validator
from typing import Optional
from bson.objectid import ObjectId

class Project(BaseModel):
    
    id: Optional[ObjectId] = Field(None, alias="_id")
    
    project_id: str = Field(..., min_length=1)

    @validator('project_id')
    def validate_project_id(cls, value):
        
        if not value.isalnum():
            
            raise ValueError('project_id must be alphanumeric')
        
        return value

    class Config:
        arbitrary_types_allowed = True
        
        
    @classmethod            # decorator for static method
    def get_indexes(cls):
        return [
            {
                "key": [
                    ("project_id", 1)
                ],
                "name": "project_id_index_1",
                "unique": True
            }
        ]














r"""
This code is used to validate and organizing the data for a project. 
Think of it as a quality control system for project data. It checks that the data is correct before saving it or using it.

For example:
- It checks that the project_id is made of only letters and numbers.
- It makes sure the project_id is at least 1 character long.
- It can handle data that comes from a database, where IDs are saved as special types (like _id in MongoDB).

--------------------------------------------------------------------------------
The imports
--------------------------------------------------------------------------------
```
from pydantic import BaseModel, Field, validator
from typing import Optional
from bson.objectid import ObjectId
```
1) pydantic: This is a library that helps check if data is correct (validation).

2) BaseModel: The main or base class from Pydantic. Models inheriting from this class can validate and serialize/deserialize data.

3) Field: It allows us to set rules for fields in the data, like:
- min_length: The minimum length of the field.
- Default values for fields.

4) validator: A decorator for writing custom validation logic for model fields.

5) Optional: Indicates that a value can be empty (None).

6) ObjectId: This is used for MongoDB, where every record (document) has a unique ID called _id.

--------------------------------------------------------------------------------
Class: Project
--------------------------------------------------------------------------------
The Project class inherits from BaseModel and defines the structure of data with validation logic.
This class describes what the project data should look like. It has two main fields: id and project_id.

Attributes:

1) id field: `id: Optional[ObjectId] = Field(None, alias="_id")`
- This field represents the project ID in a MongoDB database.
- Type: Optional[ObjectId], The id can either be an instance of ObjectId or None(default).
- alias="_id": This maps the id field to the MongoDB _id field.

2) project_id field: `project_id: str = Field(..., min_length=1)`
- This field is required (no default value because of ...).
- It must be a string with at least 1 character (min_length=1).

Note: The part where you specify the type of the fields (Optional[ObjectId] and str) is called type annotation.
- Type annotation is a way to explicitly declare the data type of variables, function arguments, and return values in Python.
- It helps to improve code clarity and readability.

--------------------------------------------------------------------------------
The Validation Rule for project_id
--------------------------------------------------------------------------------
```
@validator("project_id")
def validate_project_id(cls, value):
    if not value.isalnum():
        raise ValueError("project_id must be alphanumeric")
    return value
```
This checks that the project_id only contains letters and numbers. 
If it contains special characters (like @, #, %, !), it will throw an error.

--------------------------------------------------------------------------------
The Config Class:
--------------------------------------------------------------------------------
```
class Config:
    arbitrary_types_allowed = True
```
This allows the ObjectId type to be used in the id field. Without this, Pydantic would complain that ObjectId is not a standard type.

--------------------------------------------------------------------------------
Purpose of the Code:
--------------------------------------------------------------------------------
This code is designed to:
1) Make sure project data is always valid before using it.
2) Prevent invalid or incomplete data from entering your system (e.g., database or API).

Why is this important?
Imagine storing data in a database. If the project_id is invalid (e.g., contains special characters), 
it could cause issues later when searching for projects or integrating with other systems.
"""


r"""
--------------------------------------------------------------------------------
Why Use ObjectId?
--------------------------------------------------------------------------------
ObjectId is a special type provided by MongoDB. It is used as a unique identifier for each document (record) in a MongoDB collection.

--------------------------------------------------------------------------------
Features of ObjectId:
--------------------------------------------------------------------------------
1) Uniqueness:
- Every ObjectId is globally unique, meaning no two documents will have the same ID, even in different databases.

2) Structure:
An ObjectId is a 12-byte value that includes:
- Timestamp (first 4 bytes): Encodes the creation time.
- Machine ID (next 3 bytes): Ensures uniqueness across machines.
- Process ID (next 2 bytes): Differentiates processes on the same machine.
- Counter (last 3 bytes): A random counter to avoid collisions.
- Example: 64b7f1d44c3e3e30987275cd

3) Compact Size:
- Compared to UUIDs (16 bytes), an ObjectId is smaller (12 bytes), which helps with storage efficiency.

4) Useful Metadata:
- You can extract information from an ObjectId (e.g., the timestamp of creation).

--------------------------------------------------------------------------------
Why Is ObjectId Non-Standard?
--------------------------------------------------------------------------------
Pydantic (or Python in general) considers "standard types" to be:
- Common Python types: int, str, float, bool, list, dict, etc.
- Types defined in Python's type hints: Optional, Union, Any, etc.

Since ObjectId is specific to MongoDB and not part of Python's built-in types, it’s considered non-standard. 
This is why you need to enable it explicitly in Pydantic using:
```
class Config:
    arbitrary_types_allowed = True
```
Without this, Pydantic will raise an error when you try to use ObjectId in your model.

--------------------------------------------------------------------------------
What Are the Alternatives to ObjectId?
--------------------------------------------------------------------------------
If you’re not using MongoDB or don’t want to use ObjectId, you can use other types for unique identifiers:

1) str (String)
- The most common alternative.
- You can use a UUID (Universally Unique Identifier) as a string:
```
import uuid
project_id = str(uuid.uuid4())
print(project_id) # Example: "550e8400-e29b-41d4-a716-446655440000"
```

Advantages:
- UUIDs are standard across databases and systems.
- Human-readable and easy to work with as strings.

Disadvantages:
- Takes more storage (16 bytes compared to 12 bytes for ObjectId).
- Lacks embedded metadata like ObjectId (e.g., creation timestamp).

2) int (Integer):
- You can use a sequential integer ID:
```
project_id = 1

Advantages:
- Very compact (4 or 8 bytes, depending on the size of the integer).
- Easy to read and understand.

Disadvantages:
- No global uniqueness across systems.
- Vulnerable to ID conflicts if not managed carefully (e.g., in distributed systems).

3) Custom String IDs:
- You can define your own custom string IDs (e.g., a combination of project name and a random number):
```
project_id = "project123-5678"
```

Advantages:
- Flexible and human-readable.
- Doesn’t require specific database support.

Disadvantages:
- Requires you to handle uniqueness manually.
- Less efficient for indexing and storage.


--------------------------------------------------------------------------------
When Should You Use ObjectId?
--------------------------------------------------------------------------------
You should use ObjectId when:
- You are working with MongoDB, as it is the default ID type in MongoDB.
- You want to take advantage of its metadata (e.g., creation timestamp).
- You need globally unique IDs without relying on external systems.

--------------------------------------------------------------------------------
When Should You Use Other Types?
--------------------------------------------------------------------------------
Use alternatives like str or UUID when:
- You are not using MongoDB.
- You need compatibility with other databases (e.g., MySQL, PostgreSQL).
- You don’t need the metadata provided by ObjectId.

--------------------------------------------------------------------------------
Example: Using str Instead of ObjectId:
--------------------------------------------------------------------------------
If you don’t want to use ObjectId, your Project model could look like this:
```
from pydantic import BaseModel, Field, validator
from typing import Optional

class Project(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    project_id: str = Field(..., min_length=1)

    @validator("project_id")
    def validate_project_id(cls, value):
        if not value.isalnum():
            raise ValueError("project_id must be alphanumeric")
        return value
```

"""