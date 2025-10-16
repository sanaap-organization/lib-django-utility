from rest_framework import serializers
from ulid import ulid


def create_serializer_class(name: str, meta_data: dict, fields, methods):
    # Dynamically create a Meta class with the given attributes
    if meta_data:
        Meta = type("Meta", (), meta_data)
        cls = type(name, (serializers.Serializer,), {**fields, "Meta": Meta})
    else:
        cls = type(name, (serializers.Serializer,), fields)
    for method_name, method in methods.items():
        setattr(cls, method_name, method)
    return cls


class InlineSerializer:

    def __init__(self, meta_data=None, fields=None, methods=None):
        self.meta_data = meta_data
        self.fields = fields if fields else {}
        self.methods = methods if methods else {}

    def klass(self):
        serializer_class = create_serializer_class(
            name=str(ulid()), meta_data=self.meta_data, fields=self.fields, methods=self.methods
        )
        return serializer_class

    def __call__(self, data=None, **kwargs):
        """
        Args:
            data: Optional data to initialize the serializer.
            **kwargs: Additional arguments to pass to the serializer.
        Returns:
             A ModelSerializer instance if data is provided, otherwise the initialed class.
        """
        serializer_class = self.klass()

        if data is not None:
            return serializer_class(data=data, **kwargs)

        return serializer_class(**kwargs)


def create_model_serializer_class(name: str, meta_data: dict, fields, methods):
    """
    Creates a ModelSerializer class with the given name, meta_data
    """
    # Dynamically create a Meta class with the given attributes
    Meta = type("Meta", (), meta_data)

    cls = type(name, (serializers.ModelSerializer,), {**fields, "Meta": Meta})
    for method_name, method in methods.items():
        setattr(cls, method_name, method)
    return cls


class InlineModelSerializer:

    def __init__(self, meta_data, fields=None, methods=None):
        self.meta_data = meta_data
        self.fields = fields if fields else {}
        self.methods = methods if methods else {}

    def klass(self):
        serializer_class = create_model_serializer_class(
            name=str(ulid()), meta_data=self.meta_data, fields=self.fields, methods=self.methods
        )
        return serializer_class

    def __call__(self, data=None, **kwargs):
        """
        Args:
            data: Optional data to initialize the serializer.
            **kwargs: Additional arguments to pass to the serializer.
        Returns:
             A ModelSerializer instance if data is provided, otherwise the initialed class.
        """
        serializer_class = self.klass()

        if data is not None:
            return serializer_class(data=data, **kwargs)

        return serializer_class(**kwargs)
