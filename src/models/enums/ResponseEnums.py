from enum import Enum

class ResponseSignal(Enum):
    
    FILE_TYPE_NOT_SUPPORTED = "File type not supported"

    FILE_SIZE_EXCEEDED = "File size exceeded"
    
    FILE_VALIDATED_SUCCESS = "File validate successfully"
    
    FILE_UPLOAD_SUCCESS = "File uploaded successfully"
    
    FILE_UPLOAD_FAILED = "File upload failed"
    
    FILE_PROCESS_FAILED = "Processing failed"
    
    FILE_PROCESS_SUCCESS = "Processing success"
    
    FILE_ID_ERROR = "No file found with this id"
    
    NO_FILES_ERROR = "No files found"

    PROCESSING_FAILED = "Processing failed"
    
    PROCESSING_SUCCESS = "Processing success"
    