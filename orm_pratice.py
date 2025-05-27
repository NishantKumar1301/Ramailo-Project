# Import models
from ramailo.models.post import Post, Category, Comment, PostImage

# 1. Get all posts and print their titles
posts = Post.objects.all()
for p in posts:
    print(p.title)

# 2. Get published posts
published_posts = Post.objects.filter(is_published=True)
print(published_posts)

# 3. Get unpublished posts
unpublished_posts = Post.objects.filter(is_published=False)
print(unpublished_posts)

# 4. Search posts with "Tech" in title (no results)
tech_posts = Post.objects.filter(title__icontains="Tech")
print(tech_posts)

# 5. Search posts with "AI" in title (found one)
ai_posts = Post.objects.filter(title__icontains="AI")
print(ai_posts)

# 6. Get posts by author name containing "Nishant"
particular_user_posts = Post.objects.filter(author__name__icontains="Nishant")
for post in particular_user_posts:
    print(post.title)

# 7. Get posts belonging to category named "sports"
sports_posts = Post.objects.filter(category__name='sports')
print(sports_posts)

# 8. Get all comments and print their content
comments = Comment.objects.all()
for comment in comments:
    print(comment.content)

# 9. Get comments on posts with title containing "AI Tools"
tech_comments = Comment.objects.filter(post__title__icontains="AI Tools")
print(tech_comments)

# 10. Get comments by user name containing "Nishant"
particular_user_comments = Comment.objects.filter(user__name__icontains="Nishant")
for comment in particular_user_comments:
    print(comment.content)

# 11. Get all categories and print their names
categories = Category.objects.all()
for category in categories:
    print(category.name)

# 12. Get a category object for 'sports'
sport_category = Category.objects.get(name='sports')

# 13. Get all posts related to 'sports' category
sports_posts_via_category = sport_category.post_set.all()
print(sports_posts_via_category)

# 14. Get all post images and print their URLs
post_images = PostImage.objects.all()
for img in post_images:
    print(img.url)

# 15. Get a PostImage for the post titled "Virat Kohli The Real King"
post_image_virat = PostImage.objects.get(post__title="Virat Kohli The Real King")
print(post_image_virat)
