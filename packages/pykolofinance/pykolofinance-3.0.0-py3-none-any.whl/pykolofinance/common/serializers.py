from rest_framework import serializers


class EnumCharField(serializers.CharField):
    def __init__(self, enum_class, *args, **kwargs):
        self.enum_class = enum_class
        super().__init__(*args, **kwargs)

    def to_representation(self, value):
        if value is not None:
            return str(value)
        return None

    def to_internal_value(self, data):
        if data is not None:
            try:
                return getattr(self.enum_class, data)
            except AttributeError:
                raise serializers.ValidationError(f"Invalid enum value: {data}")
        return None


class GenericRequestResponse(serializers.Serializer):
    success = serializers.BooleanField(default=True)
    message = serializers.CharField(default="Success")


class EmptySerializer(serializers.Serializer):
    pass

class DigitOnlyFieldSerializer(serializers.CharField):
    def to_internal_value(self, data):
        if not str(data).isdigit():
            raise serializers.ValidationError("This field should contain digits only.")
        return data