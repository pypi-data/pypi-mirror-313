from abc import ABC,abstractmethod
import typing
from .descriptor import FieldDescriptor
from .exceptions import ValidationError
class SchemaMeta(type):
    def __new__(cls, name, bases, dct):
        cls._fields = {}
        
        for key,value in dct.items():
            if isinstance(value, FieldDescriptor):

                cls._fields[key] = value
                setattr(cls,key,value)
        return super().__new__(cls, name, bases, dct)
    
    




class Schema(metaclass = SchemaMeta):
    
    _validation_errors = {}
    _data = {}
    _called = False
    _validated_data = {}

    async def validate(self):
        pass 
    
    def is_valid(self):
        assert self._called == True, "__call__ must be callaed before accessing other validator methoods"
        if len(self.validation_errors.items()) == 0:
            return True
        return False
   
    
    async def __call__(self, *_data_dicts :typing.Dict) -> typing.Any:
        data  = {k: v for d in _data_dicts for k, v in d.items()}
        self._validation_errors.clear()
            
        self.declared_fields :typing.Dict[str,typing.Type[FieldDescriptor]] = self.__class__._fields
        self.cheking = True
        
        for field_name, descriptor in self.declared_fields.items():
            try:
                value = await descriptor.validate(data.get(field_name))
                try:
                    defined_validator = getattr(self,f"validate_{field_name}")
                    if callable(defined_validator):
                        value = await defined_validator(value)
                except AttributeError:
                    pass
                self._validated_data[field_name] = value
            except ValidationError as e:
                setattr(self,"error",True)
                self._validation_errors[field_name] = descriptor._validation_errors
            
            setattr(self,field_name,data.get(field_name))
        
        await self.validate()
        self._called = True
        return self
    
    
    
    @property
    def validation_errors(self):
        
        return self._validation_errors
    
    @property
    def validated_data(self):
        return self._validated_data

            
    
            
        
    




