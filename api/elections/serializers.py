from rest_framework import serializers
from .models import Election, Candidate, Vote
from users.serializers import UserSerializer

class CandidateSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Candidate
        fields = ['id', 'user', 'election']

class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = ['voter', 'candidate']

class ElectionSerializer(serializers.ModelSerializer):
    candidates = CandidateSerializer(many=True, read_only=True)

    class Meta:
        model = Election
        fields = ['id', 'title', 'description', 'start_date', 'end_date', 'candidates']
