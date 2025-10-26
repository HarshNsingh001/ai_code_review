from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import CodeReview
from .serializers import CodeReviewSerializer, CodeSubmissionSerializer
from .analyzers import CodeAnalyzer
from .ai_checker import AICodeChecker

@api_view(['POST'])
def review_code(request):

    serializer = CodeSubmissionSerializer(data=request.data)
    
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    code = serializer.validated_data['code']
    language = serializer.validated_data['language']
    use_ai = serializer.validated_data['use_ai']
    
    # Perform static analysis
    analyzer = CodeAnalyzer(code, language)
    analysis_summary = analyzer.get_analysis_summary()
    
    # AI-powered review (if requested)
    ai_feedback = ""
    if use_ai:
        try:
            ai_checker = AICodeChecker()
            ai_feedback = ai_checker.review_code(code, language, analysis_summary)
        except Exception as e:
            ai_feedback = f"AI review not available: {str(e)}"
    
    # Save review to database
    review = CodeReview.objects.create(
        code=code,
        language=language,
        complexity_score=analysis_summary['complexity'].get('average_complexity', 0),
        ai_feedback=ai_feedback,
        issues_found=analysis_summary['issues']
    )
    
    # Prepare response
    response_data = {
        'id': review.id,
        'language': language,
        'analysis': {
            'complexity': analysis_summary['complexity'],
            'maintainability_index': analysis_summary['maintainability_index'],
            'lines_of_code': analysis_summary['lines_of_code'],
            'total_issues': analysis_summary['total_issues']
        },
        'issues': analysis_summary['issues'],
        'ai_feedback': ai_feedback,
        'created_at': review.created_at
    }
    
    return Response(response_data, status=status.HTTP_201_CREATED)

@api_view(['GET'])
def get_review_history(request):

    reviews = CodeReview.objects.all()[:20]  # Last 20 reviews
    serializer = CodeReviewSerializer(reviews, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_review_detail(request, review_id):

    try:
        review = CodeReview.objects.get(id=review_id)
        serializer = CodeReviewSerializer(review)
        return Response(serializer.data)
    except CodeReview.DoesNotExist:
        return Response(
            {'error': 'Review not found'}, 
            status=status.HTTP_404_NOT_FOUND
        )

@api_view(['GET'])
def health_check(request):

    return Response({
        'status': 'healthy',
        'message': 'AI Code Review Assistant is running'
    })