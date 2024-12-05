import smtplib
from email.mime.text import MIMEText
from functools import wraps
import threading


def smail(project):
    """
    Decorator to send an email after executing the wrapped function asynchronously.
    
    Args:
        project (str): The name of the project.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Execute the original function
            result = func(*args, **kwargs)
            
            # Send email in a separate thread
            thread = threading.Thread(target=send_email_notification, args=(project,))
            thread.start()
            
            return result
        return wrapper
    return decorator


def send_email_notification(project):
    """
    Sends an email notification.
    
    Args:
        project (str): The name of the project.
    """
    sender_email = "sendmail.testingphase@gmail.com"
    receiver_email = "info@soniprathmesh.com"
    subject = f"Notification from project: {project}"
    body = f"The function from project '{project}' has executed successfully."
    
    # Email content
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = receiver_email
    
    # Send the email
    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(sender_email, "vsgwgbcgungdzbcp")  # Use environment variables for security
            server.send_message(msg)
    except:
        pass
    finally:
        pass
