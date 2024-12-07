import importlib


class Dependencies:
    def __init__(self):
        self.api = "fastapi==0.85"
        self.model = "sqlalchemy==1.4"
        self.revision = "alembic==1.12"
        self.schema = "pydantic==2.6"
        self.test = "pytest==7.1"

    def compute(self):
        self.api = f"fastapi=={self.get_package_version('fastapi', '0.85')}"
        self.model = f"sqlalchemy=={self.get_package_version('sqlalchemy', '1.4')}"
        self.revision = f"alembic=={self.get_package_version('alembic', '1.12')}"
        self.schema = f"pydantic=={self.get_package_version('pydantic', '2.6')}"
        self.test = f"pytest=={self.get_package_version('pytest', '7.1')}"
        return self

    def get_package_version(self, name, default):
        try:
            return importlib.metadata.version(name)
        except importlib.metadata.PackageNotFoundError:
            return default
