from rest_framework import serializers
from django.utils import timezone
from .models import ToDo, PriorityLevel
from account.models import Account


class ToDoSerializer(serializers.ModelSerializer):
    """
    serializes the ToDo model
    """
    user = serializers.SerializerMethodField("get_user")

    class Meta:
        model = ToDo
        fields = [
            "id", "user", "title", "description", "priority", "due_date", "time", "completed", "created_at", "updated_at"
        ]
        read_only_fields = ["id", "created_at", "updated_at"]

    def get_user(self, instance):
        return self.context["request"].user.id

    def validate_user(self, value):
        """
        validates the user field
        """

        if not Account.objects.filter(id=value).exists():
            raise serializers.ValidationError("User does not exist!")

        return value
    
    def validate_due_date(self, value):
        """
        validates the due_date field
        
        expected date format: YYYY-MM-DD
            e.g. 2024-02-31
        """

        if value < value.today():
            raise serializers.ValidationError("Due date cannot be in the past!")

        return value
    
    def validate_time(self, value):
        """
        validates the time field
        
        expected time format: HH:MM
            e.g. 23:59
        """

        return value
    
    def validate_completed(self, value):
        return False            # since a ToDo object is created as not completed by default
    
    def validate_priority(self, value):
        if value not in [priority[0] for priority in PriorityLevel.choices]:
            raise serializers.ValidationError("Invalid priority level!")
        
        return value
    
    def create(self, validated_data):
        return ToDo.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        instance.title = validated_data.get("title", instance.title)
        instance.description = validated_data.get("description", instance.description)
        instance.priority = validated_data.get("priority", instance.priority)
        instance.due_date = validated_data.get("due_date", instance.due_date)
        instance.time = validated_data.get("time", instance.time)
        instance.updated_at = validated_data.get("updated_at", timezone.now())
        instance.save()
        return instance
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["user"] = f"{instance.user.firstname} {instance.user.lastname}"
        return representation