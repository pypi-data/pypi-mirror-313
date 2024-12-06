class BaseModule:
    name = "anonymous"

    def __init__(self, params):
        self.params = params

    def process(self, ssh_client):
        """Appliquer l'action en utilisant ssh_client et les params."""
        raise NotImplementedError(
            "La méthode process doit être implémentée dans chaque module.")
