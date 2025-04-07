def format_message(msg):
    text = msg.text.split()
    reason = ' '.join(text[1:-1]) 
    value = text[-1]
    return reason, value