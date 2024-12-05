from e2clab.errors import E2clabError


class E2clabServiceImportError(E2clabError):
    def __init__(self, service_name: str) -> None:
        self.msg = f"Service not found: {service_name}, could not be imported."
        super().__init__(self.msg)
