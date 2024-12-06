from types import SimpleNamespace


class CertoraContext(SimpleNamespace):
    def delete_key(self, key: str) -> None:
        try:
            del self.__dict__[key]
        except Exception:
            pass
