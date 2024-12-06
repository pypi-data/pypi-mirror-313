from __future__ import annotations

from abc import ABC
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from atoti import (  # noqa: ICN003 # pylint: disable=nested-import,undeclared-dependency
        Session,
        SessionConfig,
    )


class Plugin(ABC):  # noqa: B024
    """Class extended by Atoti plugins."""

    def session_config_hook(
        self,
        session_config: SessionConfig,
        /,
    ) -> SessionConfig:
        """Hook called with a config before it is used to start a session."""
        return session_config

    def session_hook(
        self,
        session: Session,  # noqa: ARG002
        /,
    ) -> None:
        """Hook called after a session is started."""
        return

    @property
    def _java_package_name(self) -> str | None:
        """The fully qualified name of the plugin's Java package.

        When not ``None``, the `init()` method of its class named like this Python class will be called before starting the application.

        Warning:
            This property will be removed.
            See https://activeviam.atlassian.net/browse/PIVOT-8868.
        """
        return None
