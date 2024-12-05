from typing import Self


class PluginExecutionException(Exception):
    """
    Exception that is raised when a plugin execution fails.
    Can be thrown by the plugin itself.
    """

    def __init__(self: Self, plugin_name: str = "", message: str = "") -> None:
        default_message: str = "The requested Plugin could not be executed successfully."
        if message:
            self.message = message
        elif plugin_name:
            self.message = f"The execution of the requested '{plugin_name}'-Plugin failed."
        else:
            self.message = default_message
        super().__init__(self.message)
