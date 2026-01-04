from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.db.models import Q
from .models import TrainingPlan, TrainingCategory, TrainingPlanExercise, TrainingExerciseExecution, TrainingPlanScoring
from .serializers import TrainingPlanSerializer, TrainingPlanExerciseSerializer, TrainingCategorySerializer
# from scorings.models import ScoringCurrent, ScoringAllTime, LevelCurrent # Moved local to avoid circular import

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_training(request):
    plan_id = request.query_params.get('id')
    user_id = request.user.id
    
    # Filter by user or if public
    # Assuming user wants to see their own plans OR public plans
    # If explicit ID is given:
    if plan_id:
        try:
            plan = TrainingPlan.objects.get(plan_id=plan_id)
            # Check permissions: owner or public
            if plan.public or plan.user == request.user:
                serializer = TrainingPlanSerializer(plan)
                return Response(serializer.data)
            else:
                 return Response({'error': 'Not authorized to view this plan'}, status=status.HTTP_403_FORBIDDEN)
        except TrainingPlan.DoesNotExist:
             return Response({'error': 'Training plan not found'}, status=status.HTTP_404_NOT_FOUND)
    
    # If no ID, list user's plans
    plans = TrainingPlan.objects.filter(user=request.user)
    serializer = TrainingPlanSerializer(plans, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def search_training(request):
    query = request.query_params.get('q', '')
    if not query:
        return Response([])

    # Find plans that match name AND are (public OR owned by user)
    plans = TrainingPlan.objects.filter(
        Q(name__icontains=query) & 
        (Q(public=True) | Q(user=request.user))
    ).distinct()
    
    serializer = TrainingPlanSerializer(plans, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_training_categories(request):
    categories = TrainingCategory.objects.all()
    serializer = TrainingCategorySerializer(categories, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_training(request):
    serializer = TrainingPlanSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def edit_training(request):
    plan_id = request.data.get('plan_id')
    if not plan_id:
        return Response({'error': 'Plan ID is required for editing'}, status=status.HTTP_400_BAD_REQUEST)
        
    plan = get_object_or_404(TrainingPlan, plan_id=plan_id)
    
    if plan.user != request.user:
        return Response({'error': 'Not authorized to edit this plan'}, status=status.HTTP_403_FORBIDDEN)
        
    serializer = TrainingPlanSerializer(plan, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def start_training(request):
    plan_id = request.data.get('plan_id')
    if not plan_id:
        return Response({'error': 'Plan ID is required to start training'}, status=status.HTTP_400_BAD_REQUEST)
    
    plan = get_object_or_404(TrainingPlan, plan_id=plan_id)
    
    # Create the session (TrainingPlanExercise)
    session = TrainingPlanExercise.objects.create(plan=plan)
    
    # Return the session ID so frontend can track it
    return Response({
        'plan_exercise_id': session.plan_exercise_id,
        'message': 'Training started'
    }, status=status.HTTP_201_CREATED)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def save_training_execution(request):
    try:
        user = request.user
        data = request.data
        plan_id = data.get('plan_id')
        exercise_order = data.get('exercises_order', []) # JSON list of IDs
        sets_data = data.get('sets', []) # List of set objects

        # 1. Create TrainingPlanExercise (The Session)
        plan = TrainingPlan.objects.get(plan_id=plan_id)
        
        session = TrainingPlanExercise.objects.create(
            plan=plan,
            order=exercise_order
        )

        # 2. Iterate and create Executions
        total_xp = 0
        from exercises.models import Exercise

        for set_info in sets_data:
            # set_info structure assumed: { exercise_id, weight, reps, duration? }
            exercise_id = set_info.get('exercise_id')
            weight = set_info.get('weight', 0)
            reps = set_info.get('reps', 0)
            duration = set_info.get('duration', 0)
            
            try:
                exercise = Exercise.objects.get(exercise_id=exercise_id)
                
                TrainingExerciseExecution.objects.create(
                    plan_exercise=session,
                    exercise=exercise,
                    weight=float(weight) if weight else 0,
                    repetitions=int(reps) if reps else 0,
                    duration=int(duration) if duration else 0
                )
                total_xp += 10
            except Exercise.DoesNotExist:
                continue

        # 3. Update User XP
        from scorings.models import ScoringCurrent, ScoringAllTime, LevelCurrent
        
        # Level ONLY (Scoring is separate)
        level_tracker, created = LevelCurrent.objects.get_or_create(user=user)
        level_tracker.xp += total_xp
        level_tracker.save()

        return Response({
            'success': True, 
            'xp_earned': total_xp,
            'message': 'Training saved successfully'
        })
        
    except TrainingPlan.DoesNotExist:
        return Response({'error': 'Plan not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        print(f"Error saving training: {e}")
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
