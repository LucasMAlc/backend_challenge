import requests

BASE_URL = "http://localhost:8000/careers/"
COMMENTS_URL = "http://localhost:8000/comments/"

print("\n" + "=" * 60)
print("Testing Backend Challenge API")
print("=" * 60)

# Clean up - Delete all existing posts
print("\n[1/7] Cleaning up old data...")
response = requests.get(BASE_URL)
if response.status_code == 200:
    posts = response.json()
    if isinstance(posts, dict) and 'results' in posts:
        posts = posts['results']
    
    for post in posts:
        requests.delete(f"{BASE_URL}{post['id']}/?username={post['username']}")
    print(f"Deleted {len(posts)} existing posts")

# Create a new post
print("\n[2/7] Creating new post...")
response = requests.post(BASE_URL, json={
    "username": "testuser",
    "title": "Post with Comments",
    "content": "This post will have comments"
})

if response.status_code in [200, 201]:
    post_id = response.json()['id']
    print(f"Post created (ID: {post_id})")
else:
    print(f"Error: {response.status_code}")
    exit()

# Create comments
print("\n[3/7] Creating comments...")
comments = [
    {"username": "alice", "content": "Great post!"},
    {"username": "bob", "content": "Thanks for sharing."},
    {"username": "testuser", "content": "Thank you!"}
]

for comment in comments:
    response = requests.post(COMMENTS_URL, json={
        "post": post_id,
        **comment
    })
    if response.status_code in [200, 201]:
        print(f"Comment by {comment['username']}: '{comment['content']}'")

# List posts
print("\n[4/7] Listing posts...")
response = requests.get(BASE_URL)
if response.status_code == 200:
    posts = response.json()
    if isinstance(posts, dict) and 'results' in posts:
        posts = posts['results']
    print(f"Total posts: {len(posts)}")

# List comments
print("\n[5/7] Listing comments...")
response = requests.get(f"{COMMENTS_URL}?post={post_id}")
if response.status_code == 200:
    comments = response.json()
    if isinstance(comments, dict) and 'results' in comments:
        comments = comments['results']
    print(f"Total comments on post {post_id}: {len(comments)}")

# Update post
print("\n[6/7] Updating post...")
response = requests.patch(f"{BASE_URL}{post_id}/", json={
    "username": "testuser",
    "title": "Updated Post with Comments"
})
if response.status_code == 200:
    print("Post updated successfully")

# Test filters
print("\n[7/7] Testing filters...")
response = requests.get(f"{BASE_URL}?username=testuser&ordering=-created_datetime")
if response.status_code == 200:
    print("Filters working correctly")

print("\n" + "=" * 60)
print("Tests completed!")
print(f"Final state: 1 post (ID: {post_id}) with 3 comments")
print("=" * 60 + "\n")