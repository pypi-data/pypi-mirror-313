from e2clab.errors import E2clabError


class E2clabProviderImportError(E2clabError):
    def __init__(self, service_name: str) -> None:
        self.msg = f"Provider not found: {service_name}, could not be imported."
        super().__init__(self.msg)
