from rest_framework import serializers
from .models import Form, User, Notification

class UserSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    class Meta:
        model = User
        fields = (
            'id', 'name', 'email',
        )
        datatables_always_serialize = ('id',)
class FormSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    sender = UserSerializer()
    receiver = UserSerializer()
    class Meta:
        model = Form
        fields = (
            'id', 'title', 'compensation_from', 'compensation_to', 'content', 'form_type', 'created_at',
            'status', 'receiver', "sender", 'leave_from', 'leave_to', 'checkin_time', 'checkout_time')
        datatables_always_serialize = ('id',)

class NotificationSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    receiver = UserSerializer(read_only=True)
    class Meta:
        model = Notification
        fields = "__all__"

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
