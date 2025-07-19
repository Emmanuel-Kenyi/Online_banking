from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from .models import Election, Candidate, Vote
from .serializers import ElectionSerializer, CandidateSerializer, VoteSerializer
from django.utils import timezone
from django.utils.timezone import now
from users.models import CustomUser

# Create your views here.
@api_view(['GET'])
@permission_classes([AllowAny])
def list_all_elections(request):
    elections = Election.objects.all()
    serializer = ElectionSerializer(elections, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([AllowAny])
def list_ongoing_elections(request):
    now = timezone.now()
    elections = Election.objects.filter(start_date__lte=now, end_date__gte=now)
    serializer = ElectionSerializer(elections, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([AllowAny])
def list_expired_elections(request):
    now = timezone.now()
    elections = Election.objects.filter(end_date__lt=now)
    serializer = ElectionSerializer(elections, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def cast_vote(request, candidate_id):
    user = request.user
    try:
        candidate = Candidate.objects.get(id=candidate_id)
    except Candidate.DoesNotExist:
        return Response({'error': 'Candidate not found.'}, status=status.HTTP_404_NOT_FOUND)

    if user.has_voted:
        return Response({'error': 'You have already voted.'}, status=status.HTTP_400_BAD_REQUEST)

    # Check if user is trying to vote in the correct time window
    now = timezone.now()
    if not (candidate.election.start_date <= now <= candidate.election.end_date):
        return Response({'error': 'Election is not currently active.'}, status=status.HTTP_403_FORBIDDEN)

    Vote.objects.create(voter=user, candidate=candidate)
    user.has_voted = True
    user.save()
    return Response({'message': 'Vote cast successfully.'})

# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def active_election_count(request):
#     if not request.user.is_superuser:
#         return Response({'detail': 'Unauthorized'}, status=403)
#     count = Election.objects.filter(status='ongoing').count()
#     return Response({'count': count})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def active_election_count(request):
    try:
        if not request.user.is_superuser:
            return Response({'detail': 'Unauthorized'}, status=status.HTTP_403_FORBIDDEN)
        
        count = Election.objects.filter(start_date__lte=now(), end_date__gte=now()).count()
        return Response({'count': count})  # ✅ key matches frontend
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



