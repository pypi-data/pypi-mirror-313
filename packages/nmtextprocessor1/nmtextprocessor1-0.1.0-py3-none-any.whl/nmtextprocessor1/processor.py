STOP_WORDS = {"is", "are", "has", "have", "had"}

def remove_stop_words(text):
    words = text.split()
    filtered_words = [word for word in words if word not in STOP_WORDS]
    return " ".join(filtered_words)