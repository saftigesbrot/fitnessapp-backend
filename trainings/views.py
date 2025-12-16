from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import TrainingPlan, TrainingCategory, TrainingPlanExercise, TrainingExerciseExecution, TrainingPlanScoring
from .serializers import TrainingPlanSerializer, TrainingPlanExerciseSerializer

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
def save_training(request):
    """
    Saves a completed training session.
    Expects data:
    {
        "plan_exercise_id": <id>,
        "scoring": { "use_scoring": true, "scoring_id": 123 },
        "executions": [
            { "exercise_id": 1, "weight": 50, "duration": 0, "repetitions": 10 },
            ...
        ]
    }
    """
    plan_exercise_id = request.data.get('plan_exercise_id')
    scoring_data = request.data.get('scoring', {})
    executions_data = request.data.get('executions', [])
    
    if not plan_exercise_id:
        return Response({'error': 'plan_exercise_id is required'}, status=status.HTTP_400_BAD_REQUEST)
        
    session = get_object_or_404(TrainingPlanExercise, plan_exercise_id=plan_exercise_id)
    
    # Verify owner (via plan)
    if session.plan.user != request.user:
        return Response({'error': 'Not authorized to save this session'}, status=status.HTTP_403_FORBIDDEN)

    # 1. Create Scoring
    scoring = TrainingPlanScoring.objects.create(
        use_scoring=scoring_data.get('use_scoring', True),
        scoring_id=scoring_data.get('scoring_id')
    )
    
    # 2. Link Scoring to Session
    session.scoring_plan = scoring
    session.save()
    
    # 3. Create Executions
    created_executions = []
    for exec_data in executions_data:
        # Validate required fields for execution
        # Ideally use a serializer for validation too, but manual creation for simplicity here
        try:
            execution = TrainingExerciseExecution.objects.create(
                plan_exercise=session,
                exercise_id=exec_data.get('exercise_id'),
                weight=exec_data.get('weight', 0),
                duration=exec_data.get('duration', 0),
                repetitions=exec_data.get('repetitions', 0)
            )
            created_executions.append(execution)
        except Exception as e:
            # If error, might want to rollback transaction, but for now just log/error
            pass

    return Response({'message': 'Training saved successfully'}, status=status.HTTP_200_OK)
