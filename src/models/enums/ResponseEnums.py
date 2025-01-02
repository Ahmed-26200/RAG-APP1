# An enumeration is a set of symbolic names bound to unique, constant values. 
# which is used to define the possible responses for the file upload operation.
# In this case, the enumeration is used to define the allowed file types and maximum file size for file uploads, ...

from enum import Enum

class ResponseSignal(Enum):
    
    FILE_VALIDATED_SUCCESS = "File validate successfully"
    FILE_TYPE_NOT_SUPPORTED = "File type not supported"
    FILE_SIZE_EXCEEDED = "File size exceeded"
    FILE_UPLOAD_SUCCESS = "File uploaded successfully"
    FILE_UPLOAD_FAILED = "File upload failed"
    FILE_PROCESS_FAILED = "Processing failed"
    FILE_PROCESS_SUCCESS = "Processing success"
