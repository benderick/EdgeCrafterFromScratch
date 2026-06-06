from engine.core.workspace import register

@register
class Meta:
    def __init__(self, author: str, exp_name: str, description: str = ""):
        self.author = author
        self.exp_name = exp_name
        self.description = description