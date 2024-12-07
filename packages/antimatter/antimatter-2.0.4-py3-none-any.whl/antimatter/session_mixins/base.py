from antimatter.authz import Authorization


class BaseMixin:
    def __init__(self, authz: Authorization, **kwargs):
        try:
            super().__init__(authz=authz, **kwargs)
        except TypeError:
            super().__init__()  # If this is last mixin, super() will be object()
        self.authz = authz
