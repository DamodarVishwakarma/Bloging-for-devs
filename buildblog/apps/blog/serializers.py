from rest_framework import serializers
from blog.models import Blog


class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = ("__all__")


        

    

   
    #   fields=['title','contents','image','video','url','status','sub_title','point','author','primary_technology','related_technology']
        