"""Binder badge for launching a Jupyter notebook.

References
----------
[Binder](https://mybinder.org/)
"""

import pylinks as _pylinks

from pybadger import shields as _shields


class BinderBadger(_shields.Badger):
    """Shields.io badge generator for Binder."""

    def __init__(self, message: str = "Binder"):
        """Create a Binder badger.

        Parameters
        ----------
        message : str, default: "Binder"
            Default message to display on the badge.
        """
        super().__init__(base_path="static/v1")
        self._msg = message
        self._label = "Try Online"
        self._title = "Launch Jupyter notebook in Binder."
        self._logo = (
            "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAFkAAABZCAMAAABi1XidAAAB8lBMVEX///9XmsrmZYH1"
            "olJXmsr1olJXmsrmZYH1olJXmsr1olJXmsrmZYH1olL1olJXmsr1olJXmsrmZYH1olL1olJXmsrmZYH1olJXmsr1ol"
            "L1olJXmsrmZYH1olL1olJXmsrmZYH1olL1olL0nFf1olJXmsrmZYH1olJXmsq8dZb1olJXmsrmZYH1olJXmspXmspX"
            "msr1olL1olJXmsrmZYH1olJXmsr1olL1olJXmsrmZYH1olL1olLeaIVXmsrmZYH1olL1olL1olJXmsrmZYH1olLna3"
            "1Xmsr1olJXmsr1olJXmsrmZYH1olLqoVr1olJXmsr1olJXmsrmZYH1olL1olKkfaPobXvviGabgadXmsqThKuofKHm"
            "Z4Dobnr1olJXmsr1olJXmspXmsr1olJXmsrfZ4TuhWn1olL1olJXmsqBi7X1olJXmspZmslbmMhbmsdemsVfl8Zgms"
            "Nim8Jpk8F0m7R4m7F5nLB6jbh7jbiDirOEibOGnKaMhq+PnaCVg6qWg6qegKaff6WhnpKofKGtnomxeZy3noG6dZi+"
            "n3vCcpPDcpPGn3bLb4/Mb47UbIrVa4rYoGjdaIbeaIXhoWHmZYHobXvpcHjqdHXreHLroVrsfG/uhGnuh2bwj2Hxk1"
            "7yl1vzmljzm1j0nlX1olL3AJXWAAAAbXRSTlMAEBAQHx8gICAuLjAwMDw9PUBAQEpQUFBXV1hgYGBkcHBwcXl8gICA"
            "goiIkJCQlJicnJ2goKCmqK+wsLC4usDAwMjP0NDQ1NbW3Nzg4ODi5+3v8PDw8/T09PX29vb39/f5+fr7+/z8/Pz9/v"
            "7+zczCxgAABC5JREFUeAHN1ul3k0UUBvCb1CTVpmpaitAGSLSpSuKCLWpbTKNJFGlcSMAFF63iUmRccNG6gLbuxkXU"
            "66JAUef/9LSpmXnyLr3T5AO/rzl5zj137p136BISy44fKJXuGN/d19PUfYeO67Znqtf2KH33Id1psXoFdW30sPZ1sM"
            "vs2D060AHqws4FHeJojLZqnw53cmfvg+XR8mC0OEjuxrXEkX5ydeVJLVIlV0e10PXk5k7dYeHu7Cj1j+49uKg7uLU6"
            "1tGLw1lq27ugQYlclHC4bgv7VQ+TAyj5Zc/UjsPvs1sd5cWryWObtvWT2EPa4rtnWW3JkpjggEpbOsPr7F7EyNewtp"
            "BIslA7p43HCsnwooXTEc3UmPmCNn5lrqTJxy6nRmcavGZVt/3Da2pD5NHvsOHJCrdc1G2r3DITpU7yic7w/7Rxnjc0"
            "kt5GC4djiv2Sz3Fb2iEZg41/ddsFDoyuYrIkmFehz0HR2thPgQqMyQYb2OtB0WxsZ3BeG3+wpRb1vzl2UYBog8FfGh"
            "ttFKjtAclnZYrRo9ryG9uG/FZQU4AEg8ZE9LjGMzTmqKXPLnlWVnIlQQTvxJf8ip7VgjZjyVPrjw1te5otM7RmP7xm"
            "+sK2Gv9I8Gi++BRbEkR9EBw8zRUcKxwp73xkaLiqQb+kGduJTNHG72zcW9LoJgqQxpP3/Tj//c3yB0tqzaml05/+or"
            "HLksVO+95kX7/7qgJvnjlrfr2Ggsyx0eoy9uPzN5SPd86aXggOsEKW2Prz7du3VID3/tzs/sSRs2w7ovVHKtjrX2pd"
            "7ZMlTxAYfBAL9jiDwfLkq55Tm7ifhMlTGPyCAs7RFRhn47JnlcB9RM5T97ASuZXIcVNuUDIndpDbdsfrqsOppeXl5Y"
            "+XVKdjFCTh+zGaVuj0d9zy05PPK3QzBamxdwtTCrzyg/2Rvf2EstUjordGwa/kx9mSJLr8mLLtCW8HHGJc2R5hS219"
            "IiF6PnTusOqcMl57gm0Z8kanKMAQg0qSyuZfn7zItsbGyO9QlnxY0eCuD1XL2ys/MsrQhltE7Ug0uFOzufJFE2PxBo"
            "/YAx8XPPdDwWN0MrDRYIZF0mSMKCNHgaIVFoBbNoLJ7tEQDKxGF0kcLQimojCZopv0OkNOyWCCg9XMVAi7ARJzQdM2"
            "QUh0gmBozjc3Skg6dSBRqDGYSUOu66Zg+I2fNZs/M3/f/Grl/XnyF1Gw3VKCez0PN5IUfFLqvgUN4C0qNqYs5YhPL+"
            "aVZYDE4IpUk57oSFnJm4FyCqqOE0jhY2SMyLFoo56zyo6becOS5UVDdj7Vih0zp+tcMhwRpBeLyqtIjlJKAIZSbI8S"
            "GSF3k0pA3mR5tHuwPFoa7N7reoq2bqCsAk1HqCu5uvI1n6JuRXI+S1Mco54YmYTwcn6Aeic+kssXi8XpXC4V3t7/AD"
            "uTNKaQJdScAAAAAElFTkSuQmCC"
        )
        return

    def github(
        self,
        user: str,
        repo: str,
        ref: str,
        notebook_path: str | None = None,
    ) -> _shields.Badge:
        """Create a Binder badge for a GitHub repository.

        Parameters
        ----------
        user : str
            GitHub username.
        repo : str
            GitHub repository name.
        ref : str
            Branch, tag, or commit hash to use.
        notebook_path : str, optional
            Path to the notebook file to open.
        """
        return self._create_binder_badge(
            link=_pylinks.site.binder.github(user=user, repo=repo, ref=ref, notebook_path=notebook_path)
        )

    def gist(
        self,
        user: str,
        gist_id: str,
        ref: str,
        notebook_path: str | None = None,
    ) -> _shields.Badge:
        """Create a Binder badge for a GitHub Gist.

        Parameters
        ----------
        user : str
            GitHub username.
        gist_id : str
            GitHub Gist ID.
        ref : str
            Commit hash to use.
        notebook_path : str, optional
            Path to the notebook file to open.
        """
        return self._create_binder_badge(
            link=_pylinks.site.binder.gist(user=user, gist_id=gist_id, ref=ref, notebook_path=notebook_path),
        )

    def git(
        self,
        url: str,
        ref: str,
        notebook_path: str | None = None,
    ) -> _shields.Badge:
        """Create a Binder badge for a Git repository.

        Parameters
        ----------
        url : str
            URL of the Git repository.
        ref : str
            Branch, tag, or commit hash to use.
        notebook_path : str, optional
            Path to the notebook file to open.
        """
        return self._create_binder_badge(
            link=_pylinks.site.binder.git(url=url, ref=ref, notebook_path=notebook_path),
        )

    def gitlab(
        self,
        user: str,
        repo: str,
        ref: str,
        notebook_path: str | None = None,
    ) -> _shields.Badge:
        """Create a Binder badge for a GitLab repository.

        Parameters
        ----------
        user : str
            GitLab username.
        repo : str
            GitLab repository name.
        ref : str
            Branch, tag, or commit hash to use.
        notebook_path : str, optional
            Path to the notebook file to open.
        """
        return self._create_binder_badge(
            link=_pylinks.site.binder.gitlab(user=user, repo=repo, ref=ref, notebook_path=notebook_path),
        )

    def zenodo(
        self,
        doi: str,
        notebook_path: str | None = None,
    ) -> _shields.Badge:
        """Create a Binder badge for a Zenodo repository.

        Parameters
        ----------
        doi : str
            Zenodo DOI.
        notebook_path : str, optional
            Path to the notebook file to open.
        """
        return self._create_binder_badge(
            link=_pylinks.site.binder.zenodo(doi=doi, notebook_path=notebook_path),
        )

    def figshare(
        self,
        doi: str,
        notebook_path: str | None = None,
    ) -> _shields.Badge:
        """Create a Binder badge for a Figshare repository.

        Parameters
        ----------
        doi : str
            Figshare DOI.
        notebook_path : str, optional
            Path to the notebook file to open.
        """
        return self._create_binder_badge(
            link=_pylinks.site.binder.figshare(doi=doi, notebook_path=notebook_path),
        )

    def hydroshare(
        self,
        resource_id: str,
        notebook_path: str | None = None,
    ) -> _shields.Badge:
        """Create a Binder badge for a HydroShare resource.

        Parameters
        ----------
        resource_id : str
            HydroShare resource ID.
        notebook_path : str, optional
            Path to the notebook file to open.
        """
        return self._create_binder_badge(
            link=_pylinks.site.binder.hydroshare(resource_id=resource_id, notebook_path=notebook_path),
        )

    def dataverse(
        self,
        doi: str,
        notebook_path: str | None = None,
    ) -> _shields.Badge:
        """Create a Binder badge for a Dataverse repository.

        Parameters
        ----------
        doi : str
            Dataverse DOI.
        notebook_path : str, optional
            Path to the notebook file to open.
        """
        return self._create_binder_badge(
            link=_pylinks.site.binder.dataverse(doi=doi, notebook_path=notebook_path),
        )

    def _create_binder_badge(self, link: str | _pylinks.url.URL) -> _shields.Badge:
        return self.create(
            queries={"message": self._msg},
            params={"label": self._label, "logo": self._logo},
            attrs_img={"alt": self._msg, "title": self._title},
            attrs_a={"href": str(link)},
        )
