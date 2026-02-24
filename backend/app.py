from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
CORS(app)

posts = [
        {
        'id': 1,
        'title': 'First Post',
        'content': 'This is the content of the first post.',
        'author': 'Author1',
        'timestamp': "2025-11-02 10:00:00"
    }, {
        'id': 2,
        'title': 'Second Post',
        'content': 'This is the content of the second post.',
        'author': 'Author2',
        'timestamp': "2025-11-03 12:30:00"
    }
]

@app.route('/', methods=['GET'])
def home():
    return "Welcome to Jibril's Blog!", 200

# Get all posts
@app.route('/posts', methods=['GET'])
def get_posts():
    return jsonify(posts), 200

# Get a single post by id
@app.route('/posts/<int:post_id>', methods=['GET'])
def get_post(post_id):
    post = next((post for post in posts if post['id'] == post_id), None)
    if post:
        return jsonify(post), 200
    return jsonify({'message': 'Post not found'}), 404

# Create a new post
@app.route('/posts', methods=['POST'])
def create_post():
    data = request.get_json()
    new_post = {
        'id': len(posts) + 1,
        'title': data['title'],
        'content': data['content'],
        'author': data['author'],
        'timestamp': datetime.now()
    }
    posts.append(new_post)
    return jsonify(new_post), 201

# Update an existing post
@app.route('/posts/<int:post_id>', methods=['PUT'])
def update_post(post_id):
    data = request.get_json()
    post = next((post for post in posts if post['id'] == post_id), None)
    if post:
        post['title'] = data.get('title', post['title'])
        post['content'] = data.get('content', post['content'])
        post['author'] = data.get('author', post['author'])
        post['timestamp'] = datetime.now().isoformat()
        return jsonify(post), 200
    return jsonify({'message': 'Post not found'}), 404

# Partially update an existing post
@app.route('/posts/<int:post_id>', methods=['PATCH'])
def patch_post(post_id):
    data = request.get_json()
    post = next((post for post in posts if post['id'] == post_id), None)
    if post:
        if 'title' in data:
            post['title'] = data['title']
        if 'content' in data:
            post['content'] = data['content']
        if 'author' in data:
            post['author'] = data['author']
        post['timestamp'] = datetime.now().isoformat()
        return jsonify(post), 200
    return jsonify({'message': 'Post not found'}), 404

# Delete a post
@app.route('/posts/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    global posts
    posts = [post for post in posts if post['id'] != post_id]
    return jsonify({'message': 'Post deleted'}), 200

# Handle 404 errors
@app.errorhandler(404)
def not_found(error):
    return jsonify({'message': 'Resource not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)