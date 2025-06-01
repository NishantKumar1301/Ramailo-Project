from django.shortcuts import get_object_or_404
from ramailo.models.post import Post, Comment, PostImage

class PostService:
    def __init__(self, post=None):
        self.post = post

    @staticmethod
    def get_all_posts():
        """Return all posts."""
        return Post.objects.all()

    @staticmethod
    def get_post_by_id(post_id):
        """Return a post instance by UUID or raise 404."""
        return get_object_or_404(Post, idx=post_id)

    @staticmethod
    def create(validated_data):
        """Create a post and assign categories."""
        categories = validated_data.pop("category", [])
        post = Post.objects.create(**validated_data)
        if categories:
            post.category.set(categories)
        return post

    def update(self, validated_data):
        """Update post and categories if provided."""
        categories = validated_data.pop("category", None)
        for attr, value in validated_data.items():
            setattr(self.post, attr, value)
        self.post.save()
        if categories is not None:
            self.post.category.set(categories)
        return self.post

    @staticmethod
    def delete(post_id):
        """Delete post by UUID."""
        post = get_object_or_404(Post, idx=post_id)
        post.delete()
        return True

    def get_image_url(self):
        """Get post image URL or None."""
        try:
            return self.post.postimage.url
        except PostImage.DoesNotExist:
            return None

    @staticmethod
    def get_comments_for_post(post_id):
        """Get comments for a post."""
        post = get_object_or_404(Post, idx=post_id)
        return Comment.objects.filter(post=post)

    @staticmethod
    def get_categories_for_post(post_id):
        """Get categories for a post."""
        post = get_object_or_404(Post, idx=post_id)
        return post.category.all()
