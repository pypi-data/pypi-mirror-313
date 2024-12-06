from .authenticate import authenticate

def post_instantly(blog_id, client_secret_file, title, content):
    """
    Posts a blog instantly.
    :param blog_id: ID of the Blogger blog.
    :param client_secret_file: Path to client secret JSON file.
    :param title: Title of the blog post.
    :param content: Content of the blog post.
    """
    try:
        blogger_service = authenticate(client_secret_file)

        body = {
            "title": title,
            "content": content
        }

        response = blogger_service.posts().insert(blogId=blog_id, body=body).execute()
        print(f"Post published successfully: {response['url']}")
    except Exception as e:
        print(f"An error occurred while posting: {e}")
