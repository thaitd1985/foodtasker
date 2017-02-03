

class SearchResultSetSerializerMixin(object):
    def to_representation(self, instance):
        return super().to_representation(getattr(instance, 'object', instance))
