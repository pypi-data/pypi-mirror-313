from pathlib import Path

from aiodocker import Docker

DEFAULT_TAG = "gradion/executor"


class ExecutionContainer:
    """
    A context manager for managing the lifecycle of a Docker container used for code execution.

    It handles the creation, port mapping, volume binding, and cleanup of the container.

    Args:
        tag: Tag of the Docker image to use (defaults to gradion/executor)
        binds: Mapping of host paths to container paths for volume mounting.
            Host paths may be relative or absolute. Container paths must be relative
            and are created as subdirectories of `/app` in the container.
        env: Environment variables to set in the container

    Attributes:
        port: Host port mapped to the container's executor port. This port is dynamically
            allocated when the container is started.

    Example:
        >>> from gradion.executor import ExecutionClient
        >>> binds = {"/host/path": "example/path"}
        >>> env = {"API_KEY": "secret"}
        >>> async with ExecutionContainer(binds=binds, env=env) as container:
        ...     async with ExecutionClient(host="localhost", port=container.port) as client:
        ...         result = await client.execute("print('Hello, world!')")
        ...         print(result.text)
        Hello, world!
    """

    def __init__(
        self,
        tag: str = DEFAULT_TAG,
        binds: dict[Path | str, str] | None = None,
        env: dict[str, str] | None = None,
    ):
        self.tag = tag
        self.binds = binds or {}
        self.env = env or {}

        self._docker = None
        self._container = None
        self._port: int | None = None

    async def __aenter__(self):
        await self.run()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.kill()

    @property
    def port(self) -> int:
        """
        The host port mapped to the container's executor port.

        This port is dynamically allocated when the container is started.

        Raises:
            RuntimeError: If the container is not running
        """
        if self._port is None:
            raise RuntimeError("Container not running")
        return self._port

    async def kill(self):
        """
        Kill and remove the Docker container.
        """
        if self._container:
            await self._container.kill()

        if self._docker:
            await self._docker.close()

    async def run(self):
        """
        Create and start the Docker container.
        """
        self._docker = Docker()
        self._container = await self._run()

    async def _run(self, executor_port: int = 8888):
        config = {
            "Image": self.tag,
            "HostConfig": {
                "PortBindings": {
                    f"{executor_port}/tcp": [{}]  # random host port
                },
                "AutoRemove": True,
                "Binds": self._container_binds(),
            },
            "Env": self._container_env(),
            "ExposedPorts": {f"{executor_port}/tcp": {}},
        }

        container = await self._docker.containers.create(config=config)  # type: ignore
        await container.start()

        container_info = await container.show()
        self._port = container_info["NetworkSettings"]["Ports"][f"{executor_port}/tcp"][0]["HostPort"]

        return container

    def _container_binds(self) -> list[str]:
        return [f"{Path(k).resolve()}:/app/{v}" for k, v in self.binds.items()]

    def _container_env(self) -> list[str]:
        return [f"{k}={v}" for k, v in self.env.items()]
