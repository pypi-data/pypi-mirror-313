class AttrsNotInAnnotations(Exception):
    def __init__(self, attrs: list):
        self.attrs = attrs

    def __str__(self):
        return f"attrs not found: {self.attrs}"


class DataNotFound(Exception):
    def __init__(self, model_name: str, data_id: int):
        self.model_name = model_name
        self.data_id = data_id

    def __str__(self):
        return f"{self.model_name}_object({self.data_id}) Not Found"
