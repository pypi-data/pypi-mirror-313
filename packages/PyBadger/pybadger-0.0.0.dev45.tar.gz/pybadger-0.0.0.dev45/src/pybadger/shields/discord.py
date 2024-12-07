from pybadger import shields as _shields


class DiscordBadger(_shields.Badger):
    """Shields.io badge generator for Discord."""

    def __init__(self, server_id: str):
        """Create a Discord badger.

        Parameters
        ----------
        server_id : str
            Server ID of the Discord server (e.g., `102860784329052160`),
            which can be located in the url of the channel.

        Notes
        -----
        A Discord server admin must enable the widget setting on the server for this badge to work.
        This can be done in the Discord app: Server Setting > Widget > Enable Server Widget

        References
        ----------
        [Shields.io API - Discord](https://shields.io/badges/discord)
        """
        super().__init__(base_path="discord")
        self._server_id = server_id
        return

    def online_users(self, ) -> _shields.Badge:
        """Create a badge for number of online users."""
        return self.create(
            path=self._server_id,
            params={"label": "Discord"},
            attrs_img={
                "title": "Number of online users in Discord server.",
                "alt": "Discord Users",
            },
            attrs_a={"href": f"https://discordapp.com/channel/{self._server_id}"},
        )
