#script to send push notifications using Gotify
#replace with your own Gotify server URL and app token 
# or use a smtp server to send emails


from gotify import Gotify
from dotenv import load_dotenv
import os
load_dotenv()

gotify_url = os.getenv("GOTIFY_URL")
gotify_app_token = os.getenv("GOTIFY_APP_TOKEN")

if not gotify_app_token:
    raise ValueError("GOTIFY_APP_TOKEN environment variable is not set.")
if not gotify_url:
    raise ValueError("GOTIFY_URL environment variable is not set.")


gotif = Gotify(base_url=gotify_url,app_token=gotify_app_token)

def push_notif(title="Notification", message=None, priority=5):
    """
    Push a notification to Gotify.
    
    :param message: The message content of the notification.
    :param title: The title of the notification (default is "Notification").
    """
    gotif.create_message(
        message,
        title=title,
        priority=priority  # Optional: Set message priority (0-10)
    )


if __name__ == "__main__":
    push_notif("title","test",5)