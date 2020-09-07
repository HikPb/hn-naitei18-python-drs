from rest_framework import serializers
from .models import Form, User, Report, Notification, Division, Plan

class DivisionSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    class Meta:
        model = Division
        fields = (
            'id', 'name', 'manager',
        )
        datatables_always_serialize = ('id',)

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

class PlanSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Plan
        fields = (
            'id', 'title',
        )
        datatables_always_serialize = ('id',)

class ReportSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    sender = UserSerializer()
    receiver = UserSerializer()
    plan = PlanSerializer()

    class Meta:
        model = Report
        fields = (
            'id', 'created_at', 'plan', 'actual', 'issue', 'next', 'receiver', "sender",)
        datatables_always_serialize = ('id',)
