from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import ScoringCurrent, ScoringTop, ScoringAllTime, LevelCurrent
from .serializers import ScoringCurrentSerializer, ScoringTopSerializer, ScoringAllTimeSerializer, LevelCurrentSerializer

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_scoring(request):
    scoring_type = request.query_params.get('type')
    scoring_id = request.query_params.get('id')
    user = request.user

    if scoring_id:
        # Generic retrieval from AllTime - assumption based on vague requirement "specific by Id"
        try:
            scoring = ScoringAllTime.objects.get(scoring_id=scoring_id)
            # Check permission? Assuming public or own
            serializer = ScoringAllTimeSerializer(scoring)
            return Response(serializer.data)
        except ScoringAllTime.DoesNotExist:
            return Response({'error': 'Scoring not found'}, status=status.HTTP_404_NOT_FOUND)

    if scoring_type == 'current':
        try:
            scoring = ScoringCurrent.objects.get(user=user)
            serializer = ScoringCurrentSerializer(scoring)
            return Response(serializer.data)
        except ScoringCurrent.DoesNotExist:
             return Response({'error': 'No current scoring found'}, status=status.HTTP_404_NOT_FOUND)

    elif scoring_type == 'top':
        try:
            scoring = ScoringTop.objects.get(user=user)
            serializer = ScoringTopSerializer(scoring)
            return Response(serializer.data)
        except ScoringTop.DoesNotExist:
             return Response({'error': 'No top scoring found'}, status=status.HTTP_404_NOT_FOUND)
    
    else:
        # Default or error? listing all time for user
        scorings = ScoringAllTime.objects.filter(user=user).order_by('-created_at')
        serializer = ScoringAllTimeSerializer(scorings, many=True)
        return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_level(request):
    try:
        level = LevelCurrent.objects.get(user=request.user)
        serializer = LevelCurrentSerializer(level)
        return Response(serializer.data)
    except LevelCurrent.DoesNotExist:
        # Return default if not exists
        return Response({'level': 1, 'xp': 0})
