class SuspiciousOperation(Exception):
    """
    Exception raised for suspicious or potentially malicious operations.
    This could be used to flag any operation that appears to be abnormal
    or poses a security concern.
    """
    pass

class CreateError(Exception):
    """
    Exception raised when an error occurs during the creation process.
    This can be used when there is a failure in creating a record or 
    resource, such as in database operations or object initialization.
    """
    pass

class UpdateError(Exception):
    """
    Exception raised when an error occurs during the update process.
    This can be used when an update to an existing record or resource 
    fails due to issues like validation, constraints, or other errors.
    """
    pass

class DatabaseError(Exception):
    """
    Exception raised for errors related to database operations.
    This can be used when there is a failure in connecting to or interacting 
    with the database, such as during queries, transactions, or migrations.
    """
    pass

class ImproperlyConfigured(Exception):
    
    pass

class InvalidSessionKey(Exception):

    pass 

