from urllib import parse

from pydantic import BaseModel


class CHReplicatedEngine(BaseModel):
    zookeeper_path: str
    shard_name: str
    replica_name: str


class CHBIDatabase(BaseModel):
    name: str
    engine: CHReplicatedEngine
    comment: str


class CHBIManagementAuthentication(BaseModel):
    user: str
    password: str


class CHBIServer(BaseModel):
    address: str
    port: int

    def get_server_url(self, authentication: CHBIManagementAuthentication):
        user = parse.quote(authentication.user, safe="")
        password = parse.quote(authentication.password, safe="")
        return f"http://{user}:{password}@{self.address}:{self.port}"
