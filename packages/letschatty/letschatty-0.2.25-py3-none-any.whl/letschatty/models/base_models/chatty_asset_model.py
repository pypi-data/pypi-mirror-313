from . import TimestampValidationMixin, UpdateableMixin
from pydantic import BaseModel, Field, ConfigDict
from typing import Any, ClassVar
from bson import ObjectId
from ...models.utils.types import StrObjectId
from ...models.utils.types.serializer_type import SerializerType

class ChattyAssetModel(TimestampValidationMixin, UpdateableMixin, BaseModel):
    id: StrObjectId = Field(alias="_id", default_factory=lambda: str(ObjectId()), frozen=True)
    exclude_fields: ClassVar[dict[SerializerType, set[str]]] = {}

    model_config = ConfigDict(
        populate_by_name=True)

    def model_dump(
        self, 
        *args, 
        serializer: SerializerType = SerializerType.API, 
        **kwargs
    ) -> dict[str, Any]:
        # Get fields to exclude for this serializer type
        exclude = self.exclude_fields.get(serializer, set())
        
        # Add exclude to kwargs if not present, or update existing exclude
        if 'exclude' in kwargs:
            if isinstance(kwargs['exclude'], set):
                kwargs['exclude'].update(exclude)
            else:
                kwargs['exclude'] = exclude
        else:
            kwargs['exclude'] = exclude
        kwargs["by_alias"] = True
        data = super().model_dump(*args, **kwargs)
        ordered_data = {}
        if 'id' in data:
            ordered_data['id'] = data.pop('id')
        if 'name' in data:
            ordered_data['name'] = data.pop('name')
        ordered_data.update(data)       
        if serializer == SerializerType.DATABASE:
            ordered_data['_id'] = ObjectId(ordered_data['_id'])
        return ordered_data

    def model_dump_json(
        self, 
        *args,
        serializer: SerializerType = SerializerType.API,  # Default to API for JSON
        **kwargs
    ) -> str:
        # Just add serializer to kwargs and let parent handle the JSON conversion
        return super().model_dump_json(*args, exclude=self.exclude_fields.get(serializer, set()), **kwargs)
