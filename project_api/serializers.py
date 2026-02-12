from rest_framework import serializers
from projects.models import Project
from django.contrib.auth import get_user_model

User = get_user_model()

class ProjectSerializer(serializers.ModelSerializer):
    owner_username = serializers.CharField(source='owner.username', read_only=True)
    owner_id = serializers.IntegerField(write_only=True)  # write_only для создания
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = Project
        fields = (
            'id',
            'name',
            'description',
            'status',
            'status_display',
            'deadline',
            'created_at',
            'updated_at',
            'owner_id',  # теперь это write_only поле
            'owner_username',
        )
        read_only_fields = ('created_at', 'updated_at', 'owner_username')
    
    def create(self, validated_data):
        owner_id = validated_data.pop('owner_id')
        owner = User.objects.get(id=owner_id)
        project = Project.objects.create(owner=owner, **validated_data)
        return project
    
    def update(self, instance, validated_data):
        if 'owner_id' in validated_data:
            owner_id = validated_data.pop('owner_id')
            owner = User.objects.get(id=owner_id)
            instance.owner = owner
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        instance.save()
        return instance