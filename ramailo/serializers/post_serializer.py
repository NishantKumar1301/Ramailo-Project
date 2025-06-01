from rest_framework import serializers
from ramailo.models.post import Category, Post, Comment, PostImage
from ramailo.models.user import User

# Category Serializer
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["idx", "name"]

    name = serializers.ChoiceField( choices=Category.CHOICES)

# Post Image Serializer
class PostImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostImage
        fields = ["idx", "post", "url"]

    post = serializers.UUIDField()
    url = serializers.URLField()


# Post Serializer (Read)
class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = [
            "idx",
            "title",
            "content",
            "is_published",
            "author",
            "created_at",
            "category",
        ]

    idx = serializers.UUIDField(read_only=True)
    title = serializers.CharField(max_length=200)
    content = serializers.CharField()
    is_published = serializers.BooleanField()
    author = serializers.UUIDField()
    created_at = serializers.DateTimeField(read_only=True)
    category = serializers.PrimaryKeyRelatedField(many=True, read_only=True)


# Post Create/Update Serializer
# class PostCreateUpdateSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Post
#         fields = [
#             "title",
#             "content",
#             "is_published",
#             "author",
#             "category",
#         ]

    # title = serializers.CharField(max_length=200)
    # content = serializers.CharField()
    # is_published = serializers.BooleanField()
    # author = serializers.UUIDField()
#     category = serializers.PrimaryKeyRelatedField(many=True, queryset=Category.objects.all())

class PostCreateUpdateSerializer(serializers.ModelSerializer):
    title = serializers.CharField(max_length=200)
    content = serializers.CharField()
    is_published = serializers.BooleanField()
    author = serializers.UUIDField()
    category = serializers.ListField(
        child=serializers.UUIDField(),
        write_only=True,
        required=False,
        allow_empty=True,
    )

    class Meta:
        model = Post
        fields = [
            "title",
            "content",
            "is_published",
            "author",
            "category",
        ]

    def validate_author(self, value):
        # Validate that author UUID corresponds to an existing User
        try:
            user = User.objects.get(idx=value)
        except User.DoesNotExist:
            raise serializers.ValidationError("Invalid author UUID.")
        return user  

    def validate_category(self, value):
        # Validate that all category UUIDs exist
        categories = Category.objects.filter(idx__in=value)
        if len(categories) != len(value):
            raise serializers.ValidationError("One or more category UUIDs are invalid.")
        return categories  

    def create(self, validated_data):
        # Pop validated author (User instance) and categories (QuerySet)
        author = validated_data.pop("author")
        categories = validated_data.pop("category", [])

        # Create Post with User instance as author
        post = Post.objects.create(author=author, **validated_data)
        post.category.set(categories)
        return post

    def update(self, instance, validated_data):
        author = validated_data.pop("author", None)
        categories = validated_data.pop("category", None)

        if author:
            instance.author = author

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if categories is not None:
            instance.category.set(categories)

        instance.save()
        return instance

# Comment Serializer
class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ["idx", "post", "user", "content"]

    idx = serializers.UUIDField(read_only=True)
    post = serializers.UUIDField()
    user = serializers.UUIDField()
    content = serializers.CharField()

