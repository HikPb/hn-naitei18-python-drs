from rest_framework import serializers
from .models import Form

class FormSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    class Meta:
        model = Form
        fields = (
            'id', 'title', 'compensation_from',
            'compensation_to', 'content', 'form_type', 'status')
        datatables_always_serialize = ('id',)


# class ReportSerializer(serializers.ModelSerializer):
#     artist = ArtistSerializer()
#     genres = serializers.SerializerMethodField()
#     def get_genres(self, album):
#         return ', '.join([str(genre) for genre in album.genres.all()])
#     class Meta:
#         model = Album
#         fields = (
#         'rank', 'name', 'year', 'artist_name', 'genres',
#         )
