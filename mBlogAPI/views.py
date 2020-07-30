from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import PostSerializer, UserSerializer, Post, User

@api_view(['GET'])
def postsList(request):
    posts = Post.objects.all()
    serializer = PostSerializer(posts, many=True)
    return Response(serializer.data)

@api_view(['GET', 'PUT'])
def postDetails(request, pk=1):
    try:
        post = Post.objects.get(id=pk)
    except Post.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = PostSerializer(post)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = PostSerializer(instance=post, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT'])
def postDetailsAction(request, pk=1, action='true'):
    """
    The get request could return everyone that upvoted it.
    And the put request could be used to increment/decrement.
    """
    try:
        post = Post.objects.get(id=pk)
    except Post.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        pass

    elif request.method == 'PUT':
        if action == 'true':
            print(f'Upvoting {request.user.username}');
            post.upvotes = post.upvotes + 1
            post.upvotedby.add(request.user)
            post.save()

        elif action == 'false':
            print('Downvoting')
            post.upvotes = post.upvotes - 1
            post.upvotedby.remove(request.user)
            post.save()
        
        return Response(status=status.HTTP_200_OK)
    
            
@api_view(['GET'])
def postsLiked(request, pk):
    try:
        user = User.objects.get(id=pk)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    serializer = UserSerializer(user)
    return Response(serializer.data)

    