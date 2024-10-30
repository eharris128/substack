from substack_api.user import get_user_id

username = "iamevanharris"  # Replace with the actual username
user_id = get_user_id(username)
print(f"User ID for {username}: {user_id}")