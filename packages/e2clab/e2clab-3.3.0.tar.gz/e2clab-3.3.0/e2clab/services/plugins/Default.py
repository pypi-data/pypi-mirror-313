from e2clab.services.service import Service


class Default(Service):
    """
    A Default E2Clab Service.
    """

    def deploy(self):
        return self.register_service()
