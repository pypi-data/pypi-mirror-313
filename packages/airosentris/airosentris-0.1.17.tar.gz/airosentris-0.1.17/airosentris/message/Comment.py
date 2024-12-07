class   Comment:
    def __init__(self, id, timestamp, content):
        self.id = id
        self.timestamp = timestamp
        self.content = content

    def __repr__(self):
        return f"Comment(id={self.id}, timestamp={self.timestamp}, content={self.content})"