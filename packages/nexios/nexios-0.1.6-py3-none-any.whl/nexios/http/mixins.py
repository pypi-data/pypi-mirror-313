
import warnings
class RequestValidatonMixin:
    validated = False
    _validation_schema = None
    validation_errors = {}
    validated_data = {}
    ok = None


    async def validate_request(self, data = None):
        if not data:
            data = await self.json, await self.data, await self.files
        if not self._validation_schema:
            warnings.warn("No schema found, use @validate_request(Shema) for nexio.decorators")
            return None
        schema = await self._validation_schema()(*data)

        if schema.is_valid():
            self.ok = True
            self.validated_data = schema.validated_data
            return True
        
        else:
            self.validation_errors = schema.validation_errors
            self.ok = False
            return False

        


    