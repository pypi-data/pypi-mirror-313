import typing
from .exceptions import ValidationError
from .fields import BaseField
class FieldDescriptor:

    def __init__(
            self,
            field :BaseField,
            validators :typing.Dict[str,typing.Callable] = [],
            required :bool = True,
            default :typing.Any = None
                 ) -> None:
        
        self.field = field
        self.required = required
        self.default = default
        self.vaidators = validators
        
        



    async def validate(self,value):
        self._validation_errors = []
        
        if not self.required and not value:
            return value
        
        

        await self.validate_required(value)
        try:
            return await self.field.validate(value)
        
        except ValidationError as e:
            self._validation_errors.append(str(e))
        finally:
            if len(self._validation_errors) > 0:
                raise ValidationError()
            
        

    async def validate_required(self, value):
        if self.required == True and not value and not self.default:
            self._validation_errors.append("Required Field")
            raise ValidationError("Required Field")
        

    
