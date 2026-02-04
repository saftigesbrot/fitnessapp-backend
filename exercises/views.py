from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from .models import Exercise, ExerciseCategory
from .serializers import ExerciseSerializer, CategoryListSerializer

@api_view(['GET'])
@permission_classes([AllowAny])
def get_exercise(request):
    exercise_id = request.query_params.get('id')
    if not exercise_id:
        return Response({'error': 'Exercise ID is required'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        exercise = Exercise.objects.get(exercise_id=exercise_id)
        
        # Check visibility
        if not exercise.public:
            if not request.user.is_authenticated or exercise.user != request.user:
                return Response({'error': 'Not authorized to view this exercise'}, status=status.HTTP_403_FORBIDDEN)

        serializer = ExerciseSerializer(exercise)
        return Response(serializer.data)
    except Exercise.DoesNotExist:
        return Response({'error': 'Exercise not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_exercise(request):
    serializer = ExerciseSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    print("Serializer Errors:", serializer.errors) # Added logging
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([AllowAny])
def search_exercises(request):
    name_query = request.query_params.get('name')
    category_query = request.query_params.get('category')
    
    # Base queryset: Public exercises OR (if authenticated) own exercises
    if request.user.is_authenticated:
        queryset = Exercise.objects.filter(
            Q(public=True) | Q(user=request.user)
        ).distinct().order_by('-exercise_id')
    else:
        queryset = Exercise.objects.filter(public=True).order_by('-exercise_id')
    
    if name_query:
        queryset = queryset.filter(name__icontains=name_query)
        
    if category_query:
        # Assuming category_query matches the category name
        queryset = queryset.filter(category__name__icontains=category_query)
        
    serializer = ExerciseSerializer(queryset, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([AllowAny])
def get_category_list(request):
    categories = ExerciseCategory.objects.all()
    serializer = CategoryListSerializer(categories, many=True)
    return Response(serializer.data)
