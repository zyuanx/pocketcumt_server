from rest_framework import serializers


class SearchBookSerializer(serializers.Serializer):
    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass

    book_title = serializers.CharField()
    page = serializers.IntegerField(default=1)

    class Meta:
        fields = ['book_title', 'page']


class BookDetailSerializer(serializers.Serializer):
    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass

    book_id = serializers.CharField()

    class Meta:
        fields = ['book_id']
