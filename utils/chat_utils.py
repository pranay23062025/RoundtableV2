def format_message(role, content):
    return {
        "role": role,
        "content": content
    }

def format_chat_display(msg):
    if msg["role"] == "User":
        return f"**You:** {msg['content']}"
    else:
        return f"**{msg['role']}**: {msg['content']}"