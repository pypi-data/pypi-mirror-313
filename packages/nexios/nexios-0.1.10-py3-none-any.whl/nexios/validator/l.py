import asyncio
import inspect
from typing import (
    Any, 
    Callable, 
    Dict, 
    List, 
    Optional, 
    Union, 
    Awaitable,
    Coroutine
)

class ValidationError(Exception):
    """Custom exception for validation errors."""
    def __init__(self, errors: Dict[str, List[str]]):
        self.errors = errors
        super().__init__(f"Validation failed: {errors}")

class ValidationRule:
    """Base class for validation rules with async support."""
    async def validate(self, value: Any, context: Dict[str, Any] = None) -> bool:
        """
        Async validation method to be implemented by subclasses.
        
        Args:
            value: The value to validate
            context: Optional context dictionary for additional validation info
        
        Returns:
            Boolean indicating validation success
        """
        raise NotImplementedError("Subclasses must implement validate method")
    
    def get_error_message(self) -> str:
        """Return a default error message."""
        return "Validation failed"

class CustomAsyncRule(ValidationRule):
    """
    Allows creation of complex async custom validation rules.
    Supports both simple predicates and more complex async validation.
    """
    def __init__(
        self, 
        validation_func: Union[Callable[[Any], Awaitable[bool]], Callable[[Any], bool]],
        error_message: str = "Custom validation failed"
    ):
        """
        Initialize a custom async validation rule.
        
        Args:
            validation_func: A function that can be sync or async and returns a boolean
            error_message: Custom error message for validation failure
        """
        self.validation_func = validation_func
        self._error_message = error_message
    
    async def validate(self, value: Any, context: Dict[str, Any] = None) -> bool:
        """
        Validate using the provided custom function.
        
        Handles both sync and async validation functions.
        """
        # Determine if the function is async or sync
        if asyncio.iscoroutinefunction(self.validation_func) or isinstance(
            self.validation_func, 
            Coroutine
        ):
            return await self.validation_func(value)
        else:
            # If sync function, run in default event loop
            return self.validation_func(value)
    
    def get_error_message(self) -> str:
        """Return the custom error message."""
        return self._error_message

class TortoiseUniqueRule(ValidationRule):
    """
    Async validation rule to check uniqueness in Tortoise ORM models.
    """
    def __init__(
        self, 
        model_class: Any, 
        field: str, 
        error_message: str = "Value must be unique"
    ):
        """
        Initialize uniqueness validation for a Tortoise ORM model.
        
        Args:
            model_class: Tortoise ORM model class
            field: Field to check for uniqueness
            error_message: Custom error message
        """
        self.model_class = model_class
        self.field = field
        self._error_message = error_message
    
    async def validate(self, value: Any, context: Dict[str, Any] = None) -> bool:
        """
        Check if the value is unique in the specified model and field.
        
        Args:
            value: Value to check for uniqueness
            context: Optional context (can include current model instance for updates)
        
        Returns:
            Boolean indicating uniqueness
        """
        if value is None:
            return True
        
        # Check if this is an update scenario
        current_instance = context.get('instance') if context else None
        
        # Construct query
        query = self.model_class.filter(**{self.field: value})
        
        # If updating, exclude current instance
        if current_instance:
            query = query.exclude(pk=current_instance.pk)
        
        # Check if any matching records exist
        exists = await query.exists()
        return not exists
    
    def get_error_message(self) -> str:
        """Return the uniqueness error message."""
        return self._error_message

class Validator:
    """Enhanced async validator with context support."""
    def __init__(self, schema: Dict[str, List[ValidationRule]]):
        self.schema = schema
    
    async def validate(
        self, 
        data: Dict[str, Any], 
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Validate data against the schema with optional context.
        
        Args:
            data: Dictionary of data to validate
            context: Optional context dictionary for complex validations
        
        Returns:
            Validated data dictionary
        
        Raises:
            ValidationError if validation fails
        """
        errors = {}
        validated_data = {}
        
        # Ensure context is a dictionary
        context = context or {}
        
        for field, rules in self.schema.items():
            value = data.get(field)
            
            field_errors = []
            for rule in rules:
                # Pass context to each validation rule
                is_valid = await rule.validate(value, context)
                
                if not is_valid:
                    field_errors.append(rule.get_error_message())
            
            if field_errors:
                errors[field] = field_errors
            else:
                validated_data[field] = value
        
        if errors:
            raise ValidationError(errors)
        
        return validated_data

def validate_schema(schema: Dict[str, List[ValidationRule]]):
    """
    Decorator for async route validation with Tortoise ORM support.
    
    Supports:
    - Async route validation
    - Context-aware validation
    - Detailed error handling
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Check if the function is async
            if not asyncio.iscoroutinefunction(func):
                raise TypeError("Validation decorator requires an async function")
            
            # Assume first argument after self/cls is the request
            request_arg = args[1] if len(args) > 1 else kwargs.get('request')
            
            if request_arg is None:
                raise ValueError("No request object found for validation")
            
            # Get JSON data from request
            try:
                data = request_arg.get_json()
            except Exception:
                raise ValidationError({"request": ["Invalid JSON payload"]})
            
            # Optional: Pass current model instance for update scenarios
            context = kwargs.get('context', {})
            
            # Validate data
            try:
                validated_data = await Validator(schema).validate(data, context)
                
                # Replace request data with validated data
                kwargs['validated_data'] = validated_data
            except ValidationError as ve:
                # Customizable error handling
                return {"errors": ve.errors}, 400
            
            # Call the original function
            return await func(*args, **kwargs)
        return wrapper
    return decorator

# Example Usage with Tortoise ORM
from tortoise.models import Model
from tortoise import fields

class User(Model):
    id = fields.IntField(pk=True)
    username = fields.CharField(max_length=50, unique=True)
    email = fields.CharField(max_length=100, unique=True)
    age = fields.IntField()

class UserController:
    @validate_schema({
        'username': [
            # Built-in rules
            Required(), 
            Length(min_length=3, max_length=50),
            
            # Tortoise ORM unique validation
            TortoiseUniqueRule(
                model_class=User, 
                field='username', 
                error_message="Username is already taken"
            )
        ],
        'email': [
            Required(), 
            Email(),
            TortoiseUniqueRule(
                model_class=User, 
                field='email', 
                error_message="Email is already registered"
            )
        ],
        'age': [
            # Custom async validation example
            CustomAsyncRule(
                lambda age: 18 <= age <= 120, 
                error_message="Age must be between 18 and 120"
            )
        ]
    })
    async def create_user(self, request, validated_data):
        # Create user with validated data
        user = await User.create(**validated_data)
        return {"message": "User created", "user_id": user.id}

    @validate_schema({
        'username': [
            # Allow update with current instance context
            CustomAsyncRule(
                lambda username, context: username != context['instance'].username, 
                error_message="New username must be different"
            )
        ]
    })
    async def update_user(self, request, validated_data):
        # Update user with additional context validation
        user_id = request.view_args.get('user_id')
        current_user = await User.get(id=user_id)
        
        # Pass current instance in context
        context = {'instance': current_user}
        
        # Update user
        for key, value in validated_data.items():
            setattr(current_user, key, value)
        await current_user.save()
        
        return {"message": "User updated", "user_id": current_user.id}
    

