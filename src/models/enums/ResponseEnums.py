from enum import Enum

class ResponseSignal(Enum):
    
    FILE_TYPE_NOT_SUPPORTED = "File type not supported"

    FILE_SIZE_EXCEEDED = "File size exceeded"
    
    FILE_VALIDATED_SUCCESS = "File validate successfully"
    
    FILE_UPLOAD_SUCCESS = "File uploaded successfully"
    
    FILE_UPLOAD_FAILED = "File upload failed"
    
    FILE_PROCESS_FAILED = "Processing failed"
    
    FILE_PROCESS_SUCCESS = "Processing success"
