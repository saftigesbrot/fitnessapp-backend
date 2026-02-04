from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Max
from django.utils import timezone
import datetime
from .models import Scoring, LevelCurrent
from .serializers import ScoringSerializer, LevelCurrentSerializer

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_scoring(request):
    scoring_type = request.query_params.get('type')
    scoring_id = request.query_params.get('id')
    time_frame = request.query_params.get('time_frame') # 'daily', 'weekly', 'monthly'
    user = request.user

    if scoring_id:
        try:
            scoring = Scoring.objects.get(scoring_id=scoring_id)
            serializer = ScoringSerializer(scoring)
            return Response(serializer.data)
        except Scoring.DoesNotExist:
            return Response({'error': 'Scoring not found'}, status=status.HTTP_404_NOT_FOUND)

    if scoring_type == 'current':
        try:
            # Latest scoring by creation time
            scoring = Scoring.objects.filter(user=user).latest('created_at')
            serializer = ScoringSerializer(scoring)
            return Response(serializer.data)
        except Scoring.DoesNotExist:
             return Response({'value': 0, 'user': user.id})

    elif scoring_type == 'top':
        # Max value for user
        scoring = Scoring.objects.filter(user=user).order_by('-value').first()
        if scoring:
            serializer = ScoringSerializer(scoring)
            return Response(serializer.data)
        else:
             return Response({'value': 0, 'user': user.id})
    
    elif scoring_type == 'leaderboard':
        queryset = Scoring.objects.all()
        now = timezone.now()

        if time_frame == 'daily':
            queryset = queryset.filter(created_at__date=now.date())
        elif time_frame == 'weekly':
            # Calc start of current week (Monday) using iso calendar or just days subtract
            # Weekday: Mon=0, Sun=6
            start_of_week = now - datetime.timedelta(days=now.weekday())
            queryset = queryset.filter(created_at__date__gte=start_of_week.date())
        elif time_frame == 'monthly':
            # Current month
            queryset = queryset.filter(created_at__year=now.year, created_at__month=now.month)

        # Aggregate max score per user
        leaderboard_data = queryset.values('user__username', 'user__id').annotate(
            value=Max('value')
        ).order_by('-value')[:50]
        
        return Response(list(leaderboard_data))
    
    elif scoring_type == 'levels':
        # Return users sorted by level descending, then XP descending
        levels = LevelCurrent.objects.all().order_by('-level', '-xp')[:50]
        serializer = LevelCurrentSerializer(levels, many=True)
        return Response(serializer.data)

    else:
        # History
        scorings = Scoring.objects.filter(user=user).order_by('-created_at')
        serializer = ScoringSerializer(scorings, many=True)
        return Response(serializer.data)

@api_view(['GET'])
@permission_classes([AllowAny])
def get_level(request):
    if not request.user.is_authenticated:
        return Response({'level': 1, 'xp': 0})

    try:
        level = LevelCurrent.objects.get(user=request.user)
        serializer = LevelCurrentSerializer(level)
        return Response(serializer.data)
    except LevelCurrent.DoesNotExist:
        # Return default if not exists
        return Response({'level': 1, 'xp': 0})
