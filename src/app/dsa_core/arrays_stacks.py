# DSA ALGORITHM: Stack (LIFO) and Queue (FIFO) & Array Push/Pop wrapper
# USED FOR: Chatbot message buffers, voice prompt queues, and user crop list edits.

class Stack:
    """LIFO Stack used for navigation history and chatbot state undo."""
    def __init__(self):
        self.items = []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        if not self.is_empty():
            return self.items.pop()
        return None

    def peek(self):
        return self.items[-1] if not self.is_empty() else None

    def is_empty(self):
        return len(self.items) == 0


class Queue:
    """FIFO Queue used for processing incoming voice/text requests in order."""
    def __init__(self):
        self.items = []

    def enqueue(self, item):
        self.items.append(item)

    def dequeue(self):
        if not self.is_empty():
            return self.items.pop(0)
        return None

    def is_empty(self):
        return len(self.items) == 0


def push_crop(crop_list, new_crop):
    """DSA: Array Push Operation."""
    crop_list.append(new_crop)
    return crop_list


def pop_crop(crop_list, index=-1):
    """DSA: Array Pop Operation."""
    if crop_list and abs(index) <= len(crop_list):
        return crop_list.pop(index)
    return None
