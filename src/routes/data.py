import os
import aiofiles
from fastapi import APIRouter, Depends, UploadFile, status, Request     
from fastapi.responses import JSONResponse
from helpers.config import Settings, get_settings
from controllers import DataController, ProjectController, ProcessController
from models import ResponseSignal
import logging
from .schemes.data import ProcessRequest
from models import ProjectModel
from models import ChunkModel
from models.db_schemes import DataChunk

logger = logging.getLogger("uvicorn.error")

# Create an instance(object) of the APIRouter class
data_router = APIRouter(
    prefix="/api/v1/data", # use the /api/v1/data prefix for all routes in this file
    tags=["api_v1", "data"],  
)

# endpoint to receive the files and save them in the server
@data_router.post("/upload/{project_id}")   # The path or endpoint is relative to the prefix "/api/v1/data" defined above
async def upload_data(request: Request, 
                      project_id: str,      # the use of async is optional, but recommended for better performance.
                      file: UploadFile,  
                      app_settings: Settings = Depends(get_settings)):

    project_model = await ProjectModel.create_instance(
        db_client=request.app.db_client
        )    
    
    project = await project_model.get_project_or_create_one(
        project_id=project_id
        )
        
    # Validate the file type and size (properties)
    data_controller = DataController()
    is_valid, result_signal = data_controller.validate_uploaded_file(file=file)
    
    # change the status code from 200 to 400 if the file is not valid
    if not is_valid:
        return JSONResponse(
            content={"signal": result_signal}, 
            status_code=status.HTTP_400_BAD_REQUEST
            )
    
    """
    Now if the file is valid, we need to save the file using it's id (project_id):
    assets/files/project_id/file_name
    for example if the file id (project_id) is 1, then the file will be saved at assets/files/1/file_name
    """
    
    # Get the project directory, or create it if it does not exist
    # project_dir_path = ProjectController().get_project_path(project_id=project_id)
    
    # Generate a unique file path
    # Example output: f:\LLM\LLMProjects\RAG-APP-1\src\assets\files\1\mw1178534nx8_Projectname.txt
    file_path, file_id = data_controller.generate_unique_filepath(  # file_id is the file name
        orig_file_name=file.filename, 
        project_id=project_id
        )
    
    
    try:
        # Save the file in the project directory
        async with aiofiles.open(file_path, "wb") as f:  # Open the destination file in binary write mode
            while chunk := await file.read(app_settings.FILE_DEFAULT_CHUNK_SIZE):  # Read 512 KB (512,000 bytes) from the uploaded file
                await f.write(chunk)  # Write the 512 KB chunk to the destination file
                
    except Exception as e:
        
        logger.error(f"An error occurred while saving the file: {e}")
        
        return JSONResponse(
            content={"signal": ResponseSignal.FILE_UPLOAD_FAILED.value}, 
            status_code=status.HTTP_400_BAD_REQUEST
            )
        
        
    return JSONResponse(
            content={
                "signal": ResponseSignal.FILE_UPLOAD_SUCCESS.value,
                "file_id": file_id,
                "file_path": file_path,
                "project_id": str(project.id)
                }, 
            
            # status_code=status.HTTP_200_OK   # default
        )
    
    
####################### File Processing #######################
    
@data_router.post("/process/{project_id}")    
async def process_endpoint(project_id: str, process_request: ProcessRequest, request:Request):
    
    file_id = process_request.file_id
    chunk_size = process_request.chunk_size
    overlap_size = process_request.overlap_size
    do_reset = process_request.do_reset
    
    project_model = await ProjectModel.create_instance(
        db_client=request.app.db_client
        )    
    
    project = await project_model.get_project_or_create_one(
        project_id=project_id
        )    
    
    process_controller = ProcessController(project_id=project_id)

    # get the file content
    file_content = process_controller.get_file_content(file_id=file_id)
    
    file_chunks = process_controller.process_file_content(
        file_content=file_content,
        file_id=file_id,
        chunk_size=chunk_size,
        overlap_size=overlap_size
    )
    
    # if i want to see the file chunks
    # return file_chunks
    
    if file_chunks is None or len(file_chunks) == 0:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "signal": ResponseSignal.FILE_PROCESS_FAILED.value
            }
        )
        
    file_chunks_records = [
        DataChunk(
            chunk_text=chunk.page_content,
            chunk_metadata=chunk.metadata,
            chunk_order=i+1,
            chunk_project_id=project.id
            
            )
        for i, chunk in enumerate(file_chunks)            
    ]
    
    chunk_model = await ChunkModel.create_instance(
            db_client=request.app.db_client
        )
    
    if do_reset == 1:
        _ = await chunk_model.delete_chunks_by_project_id(
            project_id=project.id
        )


    no_records = await chunk_model.insert_many_chunks(chunks=file_chunks_records)
    
    return JSONResponse(
        content={
            "signal": ResponseSignal.FILE_PROCESS_SUCCESS.value,
            "inserted_chunks": no_records,
        }
    )   
    
    
    
    
    
r"""
```
    # Save the file in the project directory
    async with aiofiles.open(file_path, "wb") as f:
        while chunk := await file.read(512000):
            await f.write(chunk)
```

file_path:
- Represents the location where the file will be saved on the server.
- Example: f:\LLM\LLMProjects\RAG-APP-1\src\assets\files\1\file.txt

aiofiles library:
- aiofiles is an asynchronous file I/O library in Python.
- It allows file operations (like read, write, open) to be performed without blocking the main event loop.
- This is particularly useful in applications that handle multiple concurrent operations, like web servers.

--------------------------------------------------------------------------------
The Objective
--------------------------------------------------------------------------------
The code is saving an uploaded file to the server using asynchronous chunking, 
which is part of an asynchronous file handling operation where a file uploaded by a user is saved 
to the server in chunks rather than being written directly all at once. Let's explain each part and why this approach is used:

--------------------------------------------------------------------------------
How the Code Works?
--------------------------------------------------------------------------------
1) File Upload (User Perspective):
- The user uploads a file to the server (e.g., via a web form).

3) Open File in Binary Write Mode: (` async with aiofiles.open(file_path, "wb") as f:`)
- The server opens a new file (file_path) to save the uploaded content.
- `aiofiles.open()` opens the file asynchronously, meaning the server can continue processing other tasks while this file operation happens.
- The `async with` ensures the file is properly closed after the operation, even if an error occurs.

4) Read the File in Chunks: (`while chunk := await file.read(512000):`)
- `file.read(512000)` reads 512,000 bytes (512 KB) of data from the uploaded file.
- `chunk :=` assigns the data to the variable chunk.
- The while loop continues until there’s no more data to read (when the file is fully read, chunk will be None, and the loop stops).

5) Write each chunk to the target file: (`await f.write(chunk)`)
- Each chunk (512 KB of data) is written to the destination file (f) on the server.
- Writing is done asynchronously (await), allowing the server to handle other tasks while waiting for the file to finish writing.

Conclusion:
- The uploaded file (file) is read in chunks of 512,000 bytes (approximately 512 KB).
- Each chunk is then written to the target file (f) asynchronously.
- The loop continues until the entire file is read and written in chunks.

--------------------------------------------------------------------------------
Binary Write Mode ("wb"):
--------------------------------------------------------------------------------
1) Binary Mode (b):
- The "b" in "wb" indicates that the file is written in binary mode.
- When you open a file in binary mode, it means the file will be handled as raw bytes (not human-readable).

2) Write Mode ("w"):
- The "w" in "wb" indicates that the file is opened for writing.
- When you open a file in write mode, it means the file will be overwritten if it already exists.

3) So, wb mode means:
- The file is opened for writing (w).
- Data will be written as raw bytes (b).

The uploaded file could be:
- A text file (like .txt, .csv).
- A binary file (like .jpg, .pdf, .zip)

To ensure all files are handled correctly (without corruption), binary mode (wb) is used:
- Text files: Writing in binary mode works because the raw bytes of the text are preserved.
- Binary files: Writing in text mode (readable format (text)) could corrupt binary files because text mode interprets data (e.g., line endings).
- Example: Writing a binary image in text mode may result in changes like converting \n (newline) to \r\n (Windows-style newline), corrupting the image.

--------------------------------------------------------------------------------
What Happens Step by Step (scenario):
--------------------------------------------------------------------------------
1) User Uploads File:
- A user uploads a file (e.g., a 10 MB PDF).
- The server starts receiving this file as a stream.

2) Server Opens File for Writing:
- The server creates a new file (e.g., file.txt) at the specified location (file_path).
- It opens this file in binary write mode (wb) to ensure all data is saved without corruption.

3) File is Processed in Chunks:
- The uploaded file is read in small parts (512 KB at a time).
- Each chunk is written to the destination file.

4) Process Completes:
- The loop continues until the entire file is saved.
- The file is automatically closed after the process (async with ensures this).

Why is This Efficient?
- Memory Usage: Only 512 KB of data is in memory at any given time, no matter how large the file is.
- Concurrency: Other tasks (e.g., handling other uploads) can proceed while this operation is ongoing.

--------------------------------------------------------------------------------
Why Save the File in Chunks?
--------------------------------------------------------------------------------
1) Memory Efficiency:
- If the file is very large (e.g., hundreds of MBs or several GBs), loading it entirely into memory at once could lead to high memory consumption or even crash the server.
- Chunked processing ensures only a small portion of the file is in memory at any given time.

2) Asynchronous Operations:
- Asynchronous file handling allows the server to remain responsive while writing the file.
- For instance, in a web server, other requests can be processed concurrently while this file is being saved.

3) Scalability:
- Handling file uploads in chunks makes the application more scalable, as it can serve multiple users simultaneously without exhausting system resources.

4) Practical Use Case:
- Chunking is particularly useful in cases where the file comes from a stream or when dealing with unreliable connections (e.g., network interruptions).

--------------------------------------------------------------------------------
Why Not Save the File Directly?
--------------------------------------------------------------------------------
If you attempted to save the file directly without chunking:
1) For Small Files: It might work fine, but it would block the server while saving.
2) For Large Files: It could lead to:
 - High memory usage.
 - Slower server response times for other users.
 - Potential server crashes if the system runs out of memory.
 
In summary, this chunked approach ensures efficient, safe, and scalable handling of file uploads,
especially in high-performance or resource-constrained environments.


--------------------------------------------------------------------------------
try...except:
--------------------------------------------------------------------------------
The try...except block is used to handle errors or exceptions that might occur during the execution of a code block. 
Here’s why it’s important:

1) Prevent Crashes:
- If an error occurs, the program would normally crash and stop execution.
- The try...except block ensures the program can handle the error gracefully and continue running.

2) Error Detection:
- If something goes wrong (e.g., file permissions, disk space issues), the code in the try block raises an exception.
- The except block catches the error and allows you to decide what to do next (e.g., log the error, return a user-friendly response).

Potential issues in uploading files, that may occur:
1) File permission errors (e.g., no write access to the directory).
2) Disk space issues (e.g., no space left on the server).
3) Network errors or corrupted upload streams.

except Block:
- This catches any exception that occurs during the file-saving process.
- Instead of crashing the application, the error is logged, and a user-friendly response is returned.


--------------------------------------------------------------------------------
What is Logging?
--------------------------------------------------------------------------------
Logging is the process of recording information about the program's execution, such as:
- Errors
- Warnings
- Debugging information
- General information about the application's status

In Python, the logging module provides a flexible way to log messages at different severity levels.

--------------------------------------------------------------------------------
Purpose of Logging
--------------------------------------------------------------------------------
1) Debugging:
- Helps developers identify issues in the application.
- Example: Tracking why a file upload failed.

2) Monitoring:
- Logs can be analyzed to monitor the system's health and performance.
- Example: How often do file upload errors occur?

3) Error Reporting:
- Logs capture details about exceptions that occur, which can help in diagnosing problems.

4) Auditing:
- Logs can be used to track user activity or system events for compliance and security.

--------------------------------------------------------------------------------
Severity Levels in Logging
--------------------------------------------------------------------------------
Logging messages are categorized by severity:
- DEBUG: Detailed information, useful for debugging.
- INFO: General information about the program’s execution.
- WARNING: An indication that something unexpected happened, but the program can still continue.
- ERROR: A serious problem that prevents part of the program from functioning.
- CRITICAL: A very severe error that might cause the program to stop.

--------------------------------------------------------------------------------
in my code:  `logger = logging.getLogger("uvicorn.error")`
--------------------------------------------------------------------------------
- A logger object is created for logging messages.
- "uvicorn.error" is a specific logger name used in applications running with the Uvicorn server.
- This ensures that the error logs are integrated with the Uvicorn logging system.

--------------------------------------------------------------------------------
in my code:  `logger.error(f"An error occurred while saving the file: {e}")`
--------------------------------------------------------------------------------
- Logs the error message at the ERROR severity level.
- f"An error occurred while saving the file: {e}" includes:
    -> A descriptive message.
    -> The exception details (e) to help diagnose the problem.

--------------------------------------------------------------------------------
Handling the Error Gracefully:
--------------------------------------------------------------------------------
If an exception occurs, the code does two things:
1) Logs the Error:
- The error is logged using logger.error() so that developers or system administrators can investigate the issue later.

2) Returns a User-Friendly Response:
```
return JSONResponse(
    content={"signal": ResponseSignal.FILE_UPLOAD_FAILED.value}, 
    status_code=status.HTTP_400_BAD_REQUEST
)
```
- Sends a JSON response to the client: Contains a signal (ResponseSignal.FILE_UPLOAD_FAILED.value) indicating the error.
- status_code=status.HTTP_400_BAD_REQUEST: Returns an HTTP status code 400 (Bad Request) to inform the client that the upload failed.

"""
