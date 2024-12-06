class AgentStatusRequest:
    def __init__(self, code: str):
        self.code = code

    def __str__(self):
        return f"AgentStatusRequest(code={self.code})"