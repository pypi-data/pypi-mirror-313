from datetime import datetime, timedelta, timezone
from .authenticate import authenticate

def schedule_post(blog_id, client_secret_file, title, content, publish_time, utc_offset="+00:00"):
    """
    Schedules a blog post to be published at a specific time using UTC offset.
    :param blog_id: ID of the Blogger blog.
    :param client_secret_file: Path to client secret JSON file.
    :param title: Title of the blog post.
    :param content: Content of the blog post.
    :param publish_time: Scheduled publish time (DD/MM/YYYY-HH:MM:SS format).
    :param utc_offset: UTC offset as a string (e.g., "+05:30", "-07:00").
    """
    try:
        # Convert publish_time from custom format to datetime object
        dt = datetime.strptime(publish_time, "%d/%m/%Y-%H:%M:%S")

        # Parse UTC offset
        sign = 1 if utc_offset.startswith("+") else -1
        hours, minutes = map(int, utc_offset[1:].split(":"))
        offset = timezone(timedelta(hours=sign * hours, minutes=sign * minutes))

        # Apply UTC offset to the datetime object
        localized_dt = dt.replace(tzinfo=offset)

        # Convert to UTC
        publish_time_utc = localized_dt.astimezone(timezone.utc).isoformat()

        blogger_service = authenticate(client_secret_file)

        body = {
            "title": title,
            "content": content,
            "published": publish_time_utc,
            "status": "DRAFT"  # Post will remain in draft until the scheduled time
        }

        response = blogger_service.posts().insert(blogId=blog_id, body=body).execute()
        print(f"Post scheduled successfully: {response['url']}")
    except ValueError:
        print("Invalid date or UTC offset format. Please use DD/MM/YYYY-HH:MM:SS for date and ±HH:MM for offset.")
    except Exception as e:
        print(f"An error occurred while scheduling: {e}")
