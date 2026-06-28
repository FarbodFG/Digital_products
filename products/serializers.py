from .models import Product, Category, File
from rest_framework import serializers


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'title', 'describtion', 'avatar')


class FileSerializer(serializers.ModelSerializer):
    file_type = serializers.SerializerMethodField()

    class Meta:
        model = File
        fields = ('id', 'title', 'file', 'file_type')
        
    def get_file_type(self, obj):
        return obj.get_file_type_display()


class ProductSerializer(serializers.HyperlinkedModelSerializer):
    categories = CategorySerializer(many=True)
    # files = FileSerializer(many=True)
    # files = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ('id', 'title', 'describtion', 'avatar',
                  'created_time', 'categories', 'url')

    # def get_files(self, obj):
    #     files = obj.files.all()
    #     return FileSerializer(files, many=True, context=self.context).data
