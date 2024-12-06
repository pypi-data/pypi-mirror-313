from .authenticate import authenticate

def delete_post(blog_id, client_secret_file, title):
    """
    Deletes a specific post by its title. If multiple posts have the same title,
    it prompts the user to select which one to delete.
    :param blog_id: ID of the Blogger blog.
    :param client_secret_file: Path to client secret JSON file.
    :param title: Title of the posts to delete.
    """
    def get_posts_by_title(blogger_service, blog_id, title):
        """
        Retrieves all posts with the given title.
        :param blogger_service: Authenticated Blogger service object.
        :param blog_id: ID of the Blogger blog.
        :param title: Title of the posts to find.
        :return: List of posts (each as a dictionary containing details).
        """
        try:
            request = blogger_service.posts().list(blogId=blog_id).execute()
            posts = request.get('items', [])
            return [post for post in posts if post['title'] == title]
        except Exception as e:
            print(f"Error fetching posts: {e}")
            return []

    try:
        blogger_service = authenticate(client_secret_file)
        matching_posts = get_posts_by_title(blogger_service, blog_id, title)

        if not matching_posts:
            print(f"No posts found with the title '{title}'.")
            return

        if len(matching_posts) == 1:
            # Automatically delete the single matching post
            post_id = matching_posts[0]['id']
            blogger_service.posts().delete(blogId=blog_id, postId=post_id).execute()
            print(f"Deleted post with title '{title}' and ID: {post_id}")
        else:
            # Prompt the user to choose which post to delete
            print(f"Found {len(matching_posts)} posts with the title '{title}':")
            for i, post in enumerate(matching_posts, start=1):
                print(f"[{i}] ID: {post['id']} | URL: {post.get('url', 'No URL')} | Published: {post.get('published', 'Unknown')}")

            choice = int(input("Enter the number of the post you want to delete (or 0 to cancel): "))
            if choice == 0:
                print("Deletion cancelled.")
                return

            selected_post = matching_posts[choice - 1]
            post_id = selected_post['id']

            # Delete the selected post
            blogger_service.posts().delete(blogId=blog_id, postId=post_id).execute()
            print(f"Deleted post with title '{title}' and ID: {post_id}")
    except Exception as e:
        print(f"An error occurred: {e}")
