from rest_framework.views import APIView
from ramailo.models.post import Post
from ramailo.serializers.post_serializer import PostSerializer,PostCreateUpdateSerializer,CommentSerializer
from ramailo.services.post_service import PostService
from ramailo.builders.response_builder import ResponseBuilder

class PostListCreateAPIView(APIView):
    def get(self, request):
        posts = PostService.get_all_posts()
        serializer = PostSerializer(posts, many=True)
        return ResponseBuilder().success().result_object(serializer.data).ok_200().get_response()

    def post(self, request):
        serializer = PostCreateUpdateSerializer(data=request.data)
        if serializer.is_valid():
            post = PostService.create(serializer.validated_data)
            response_serializer = PostSerializer(post)
            return ResponseBuilder().success().result_object(response_serializer.data).ok_200().get_response()
        return ResponseBuilder().fail().message(serializer.errors).bad_request_400().get_response()

class PostDetailAPIView(APIView):
    def get(self, request, post_id):
        try:
            post = PostService.get_post_by_id(post_id)
        except Post.DoesNotExist:
            return ResponseBuilder().fail().message("Post not found").not_found_404().get_response()
        serializer = PostSerializer(post)
        return ResponseBuilder().success().result_object(serializer.data).ok_200().get_response()

    def put(self, request, post_id):
        try:
            post = PostService.get_post_by_id(post_id)
        except Post.DoesNotExist:
            return ResponseBuilder().fail().message("Post not found").not_found_404().get_response()
        serializer = PostCreateUpdateSerializer(post, data=request.data, partial=True)
        if serializer.is_valid():
            updated_post = PostService(post).update(serializer.validated_data)
            response_serializer = PostSerializer(updated_post)
            return ResponseBuilder().success().result_object(response_serializer.data).ok_200().get_response()
        return ResponseBuilder().fail().message(serializer.errors).bad_request_400().get_response()

    def delete(self, request, post_id):
        try:
            PostService.delete(post_id)
            return ResponseBuilder().success().message("Post deleted successfully").ok_200().get_response()
        except Post.DoesNotExist:
            return ResponseBuilder().fail().message("Post not found").not_found_404().get_response()

class PostCommentsAPIView(APIView):
    def get(self, request, post_id):
        try:
            comments = PostService.get_comments_for_post(post_id)
        except Post.DoesNotExist:
            return ResponseBuilder().fail().message("Post not found").not_found_404().get_response()
        serializer = CommentSerializer(comments, many=True)
        return ResponseBuilder().success().result_object(serializer.data).ok_200().get_response()
