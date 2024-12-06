from .exceptions import ValidationError
from typing import Dict
import re,json,uuid
from datetime import date,time,datetime
from nexios.http.parsers import UploadedFile
class BaseField:
    validated = False
    
    async def validate(self, value):
        pass

    

class StringField(BaseField):

    def __init__(self,max_length :int = None,
                      min_length :int = None) -> None:
        
        self.max_length = max_length
        self.min_length = min_length
        


    async def validate(self, value :str) -> str:
        self.value = value
        self.check_type(value)
        self.validate_max(value)
        self.validate_min(value)

        return str(value)

            
    def validate_max(self,value):
        if not value or not self.max_length:
            return 
        if len(value) > self.max_length:
            raise ValidationError(f"Value length must not be above {self.max_length}") 
        
    def validate_min(self,value):
        if not value or not self.min_length:
            return 
        if len(value) < self.min_length:
            raise ValidationError(f"Value length must not be below {self.min_length}") 
        
    def check_type(self, value):
        if not value :
            return 
        if not isinstance(value,str):
            raise ValidationError("Invalid type expected type 'string' ")
        
    

    def __str__(self) -> str:
        return "String Field Validator"


    
class IntegerField(BaseField):

    def __init__(self,
        max = None,
        min = None,
        max_digits = None) -> None:
        self.max = max
        self.min = min
        self.max_digits = max_digits
        super().__init__()

    async def validate(self, value):
        self.check_type(value)
        self.validate_max(value)
        self.validate_min(value)

        return int(value)
    def check_type(self, value):

        if not value:
            return
        if not isinstance(self.cast_value(value), int):
            raise ValidationError("Invalid type expected type 'Integer' ")

    def cast_value(self, value):
        
        try:
            return int(value)

        except:
            return value
    
    def validate_max(self,value):
        if not value or not self.max:
            return

        if self.cast_value(value) > self.max:
            raise ValidationError(f"Value must not exceed {self.max}") 

    def validate_min(self,value):
        if not value or not self.min:
            return

        if self.cast_value(value) < self.min:
            raise ValidationError(f"Value must not be below {self.min}") 
        

    def valiate_max_digits(self, value):
        if not value or not self.max_digits:
            return
        
        if len(str(value)) > self.max_digits:
            raise ValidationError(f"Length of value digit must not exceed {self.max_digits}")


    def __str__(self):
        return "<IntegerField Validator>"


class BooleanField(BaseField):
    async def validate(self, value):
        if not value:
            return
        casted_value = self.cast_value(value)
        if not isinstance(value, bool):
            raise ValidationError("Invalid type expected type 'Boolean'")
        return casted_value

    def cast_value(self, value):
        true_value = [
            "true",
            1,"1",
            "t",
            "yes"

        ]
        false_value = [
            "false",
            "no",
            0,"0",
            "n"
        ]
        if value in true_value:
            return True
        elif value in false_value:
            return False
        else:
            raise ValidationError("Invalid type expected type 'Boolean'")

    def __str__(self):
        return "Boolean Field Validator"
    

    


class URLField(BaseField):
    async def validate(self, value):
        if not value:
            return
        pattern = re.compile(
            r'^(http|https)://[a-zA-Z0-9-._~:/?#[\]@!$&\'()*+,;=.]+$'
        )
        if not pattern.match(value):
            raise ValidationError("Invalid URL format")
        return value

    

    def __str__(self):
        return "URL Field Validator"

class JSONField(BaseField):
    async def validate(self, value):
        if not value:
            return
        if not isinstance(value, (str, dict)):
            raise ValidationError("Invalid type expected 'string' or 'dictionary'")
        if isinstance(value, str):
            try:
                json.loads(value)
            except json.JSONDecodeError:
                raise ValidationError("Invalid JSON format")
        return value

    def __str__(self):
        return "JSON Field Validator"
    

class FileField(BaseField): 
    def __init__(self, allowed_extensions=None,max_size = None, min_size = None):
        self.allowed_extensions = allowed_extensions or []
        self.max_size = max_size
        self.min_size = min_size

    async def validate(self, value):
        if not value:
            return
        if not isinstance(value, UploadedFile): 
            
            raise ValidationError("Invalid file format")
        await self.validate_size(value)
        if self.allowed_extensions:
            extension = value.split('.')[-1].lower()
            if extension not in self.allowed_extensions:
                raise ValidationError(
                    f"File type not allowed. Allowed extensions: {', '.join(self.allowed_extensions)}"
                )
        return value
    
    async def validate_size(self, value :UploadedFile):
        if not value:
            return value
        
        if self.min_size and value.size < self.min_size:
            raise ValidationError("File size too small")
        
        if self.max_size and value.size > self.max_size:
            raise ValidationError("File size too large")


    def __str__(self):
        return "File Field Validator"

class ImageField(FileField):
    def __init__(self):
        super().__init__(allowed_extensions=["jpg", "jpeg", "png", "gif"])

    def __str__(self):
        return "Image Field Validator"
    
class ListField(BaseField): 
    def __init__(self, 
                 child_field=None,
                 max_length = None,
                 min_length = None):
        self.child_field = child_field
        self.max_length = max_length
        self.min_length = min_length
    async def validate(self, value):
        if not value:
            return
        if not isinstance(value, list):
            raise ValidationError("Invalid type expected type 'list'")
        if self.child_field:
            for item in value:
                await self.child_field.validate(item)
        return value

    def validate_length(self,value):
        if not value:
            return
        if self.max_length and len(value) > self.max_length:
            raise ValidationError(f"Field length must not exceed {self.max_length}")
        
        if self.min_length and len(value) < self.min_length:
            raise ValidationError(f"Field length must not be below {self.min_length}")

        return value

    def __str__(self):
        return "List Field Validator"
    

class EmailField(BaseField):
    async def validate(self, value):
        if not value:
            return
        
        pattern = re.compile(r'^[\w\.-]+@[\w\.-]+\.\w+$')
        if not pattern.match(value):
            raise ValidationError("Invalid email address format")
        return value

    

    def __str__(self):
        return "Email Field Validator"
    

class UUIDField(BaseField):
    async def validate(self, value):
        if not value: 
            return None
        if not isinstance(value, (str, int)):  # Ensure the value is a string or int
            raise ValidationError("Invalid type, expected a string or integer for UUID")
        
        if isinstance(value, int):
            return str(uuid.UUID(int=value))
        
        try:
            return str(uuid.UUID(value))
        except ValueError:
            raise ValidationError("Invalid UUID format")

        return uuid.UUID(value)
    def __str__(self):
        return "UUID Field Validator"


class FloatField(IntegerField):
    async def validate(self, value):
        if not value:
            return
        self.check_type(value)
        return float(value)

    def check_type(self, value):
        if not isinstance(value, (float, int)):
            raise ValidationError("Invalid type expected type 'Float' ")

    def __str__(self):
        return "Float Field Validator"



class DateField(BaseField):
    async def validate(self, value):
        
        if not value:
            return
        if isinstance(value,date):
            return value
        
        casted_value = self.cast_object(value)
        if not isinstance(casted_value, date):
            raise ValidationError("Invalid type expected type 'Date'")
        return casted_value

    def __str__(self):
        return "Date Field Validator" 
    
    def cast_object(self, value):
        formats = [
            "%Y-%m-%d",   # 2024-11-26
            "%d/%m/%Y",   # 26/11/2024
            "%m-%d-%Y",   # 11-26-2024
            "%B %d, %Y",  # November 26, 2024
            ]
        for fmt in formats:
            try:
                return datetime.strptime(value, fmt).date()
                
            except ValueError:
                continue
        raise ValidationError(f"Invalid date format ! try using {formats}")
        

class TimeField(BaseField):
    async def validate(self, value):
        if not value:
            return
        if isinstance(value, time):
            return value
        casted_value = self.cast_object(value)
        
        if not isinstance(casted_value, time):
            raise ValidationError("Invalid type expected type 'Time'")
        return casted_value
    def cast_object(self, value):
        formats = [
        "%H:%M",       # 14:30
        "%I:%M %p",    # 02:30 PM
        "%H:%M:%S",    # 14:30:00
        ]
        for fmt in formats:
            try:
                return   datetime.strptime(value, fmt).time()
                
            except ValueError:
                continue
        raise ValidationError(f"Invalid time format ! try using {formats}")
    def __str__(self):
        return "Time Field Validator"
    

class DateTimeField(BaseField):
    async def validate(self, value):
        if not value:
            return
        if isinstance(value,datetime):
            return value
        casted_value = self.cast_object(value)
        
        if not isinstance(casted_value, datetime):
            raise ValidationError("Invalid type expected type 'DateTime'")
        return casted_value

    def cast_object(self, value):
        formats = [
            "%Y-%m-%d %H:%M:%S",  # 2024-11-26 14:30:00
            "%Y-%m-%d %I:%M %p",  # 2024-11-26 02:30 PM
            "%d/%m/%Y %H:%M:%S",  # 26/11/2024 14:30:00
            "%d-%m-%Y %I:%M:%S %p",  # 26-11-2024 02:30:00 PM
            "%B %d, %Y %I:%M %p",  # November 26, 2024 02:30 PM
        ]
        for fmt in formats:
            try:
                # Try to parse the value with each format
                return datetime.strptime(value, fmt)
            except ValueError:
                continue
        # If no format matches, raise a ValidationError
        raise ValidationError(f"Invalid datetime format! Supported formats: {', '.join(formats)}")
    def __str__(self):
        return "DateTime Field Validator"
    
class ChoiceField(BaseField):
    def __init__(self, choices):
        if not isinstance(choices, (list, tuple)) or not choices:
            raise ValueError("Choices must be a non-empty list or tuple")
        self.choices = choices

    async def validate(self, value):
        if not value:
            return
        if value not in self.choices:
            raise ValidationError(f"Invalid value. Allowed choices are: {self.choices}")
        return value

    def __str__(self):
        return "Choice Field Validator"