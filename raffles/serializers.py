from rest_framework import serializers
from .models import Raffle

class RaffleCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Raffle
        fields = ['raffle_title', 'raffle_description', 'raffle_fecha', 'raffle_price', 'raffle_image']
