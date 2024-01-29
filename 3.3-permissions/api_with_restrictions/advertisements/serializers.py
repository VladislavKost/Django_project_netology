from django.contrib.auth.models import User
from rest_framework import serializers

from advertisements.models import Advertisement
from rest_framework.exceptions import ValidationError


class UserSerializer(serializers.ModelSerializer):
    """Serializer для пользователя."""

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "first_name",
            "last_name",
        )


class AdvertisementSerializer(serializers.ModelSerializer):
    """Serializer для объявления."""

    creator = UserSerializer(
        read_only=True,
    )

    class Meta:
        model = Advertisement
        fields = (
            "id",
            "title",
            "description",
            "creator",
            "status",
            "created_at",
        )

    def create(self, validated_data):
        """Метод для создания"""

        # Простановка значения поля создатель по-умолчанию.
        # Текущий пользователь является создателем объявления
        # изменить или переопределить его через API нельзя.
        # обратите внимание на `context` – он выставляется автоматически
        # через методы ViewSet.
        # само поле при этом объявляется как `read_only=True`
        validated_data["creator"] = self.context["request"].user
        return super().create(validated_data)

    def validate(self, data):
        """Метод для валидации. Вызывается при создании и обновлении."""
        request_method = self.context["request"].method
        if request_method == "POST":
            user_records_draft = Advertisement.objects.filter(
                creator_id=self.context["request"].user.id, status="DRAFT"
            )
            if len(user_records_draft) == 10:
                raise ValidationError(
                    "Разрешается иметь не более 10 черновиков объяслений. Удалите ненужные черновики и повторите попытку"
                )
        elif request_method == "PATCH":
            user_records_opened = Advertisement.objects.filter(
                creator_id=self.context["request"].user.id, status="OPEN"
            )
            if len(user_records_opened) == 10:
                raise ValidationError(
                    "Разрешается иметь не более 10 открытых объяслений"
                )
        return data
