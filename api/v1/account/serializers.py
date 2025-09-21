from rest_framework import serializers
import bleach
from .models import Profile

class ProfileSerializer(serializers.ModelSerializer):
    # 添加一個額外的非模型字段，用於標記是否刪除頭像
    remove_portrait = serializers.BooleanField(required=False, write_only=True)
    
    class Meta:
        model = Profile
        fields = ['real_name', 'nickname', 'portrait', 'address', 'phone', 'remove_portrait']
        read_only_fields = ()
        
    def validate_real_name(self, value):
        return bleach.clean(value, tags=[], strip=True)

    def validate_nickname(self, value):
        return bleach.clean(value, tags=[], strip=True)

    def validate_address(self, value):
        return bleach.clean(value, tags=[], strip=True)

    def update(self, instance, validated_data):
        remove_portrait = validated_data.pop('remove_portrait', False)
        if remove_portrait and instance.portrait:
            instance.portrait.delete(save=False)
            instance.portrait = None
        
        return super().update(instance, validated_data)
"""
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'email',
            'is_active',
            'is_staff',
            'date_joined',
        )
        read_only_fields = (
            'email',
            'date_joined',
        )
"""

class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError('舊密碼錯誤')
        return value

    def save(self, **kwargs):
        user = self.context['request'].user
        user.set_password(self.validated_data['new_password'])
        user.save()