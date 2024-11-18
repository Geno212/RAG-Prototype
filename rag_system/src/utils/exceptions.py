class DocumentProcessingError(Exception):
    """Exception raised for errors during document processing."""
    def __init__(self, message="An error occurred while processing the document."):
        self.message = message
        super().__init__(self.message)


class DocumentUploadError(Exception):
    """Exception raised for errors during document upload."""
    def __init__(self, message="Failed to upload the document."):
        self.message = message
        super().__init__(self.message)


class CollectionNotFoundError(Exception):
    """Exception raised when the specified collection is not found."""
    def __init__(self, collection_name, message=None):
        if not message:
            message = f"The collection '{collection_name}' was not found."
        self.message = message
        super().__init__(self.message)


class QueryProcessingError(Exception):
    """Exception raised for errors during query processing."""
    def __init__(self, message="An error occurred while processing the query."):
        self.message = message
        super().__init__(self.message)
