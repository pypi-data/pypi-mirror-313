from pybadger import shields as _shields


class RepoDynamicsBadger(_shields.Badger):
    """Shields.io badge generator for RepoDynamics."""

    def __init__(self):
        super().__init__(base_path="static/v1")
        return

    def pypackit(self) -> _shields.Badge:
        logo_light = (
            "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAACXBIWXMAAAsPAAALDwGS"
            "+QOlAAADxklEQVRYhb1XbWxTZRR+3vvR3rt+OsJ2M5CWrKIxZJsm/gITk0XBjYQ4IJshAcJHjIq4HyyKgjJBPiLqwg"
            "8Tk6L80qATgwkLGpUE94OYSBgSIZnTFoK93VxhpV1v73s/TGu6rOu69nZlz6/zvue85zw55z73vZeYpgkraDr85IX7"
            "NLEGFHDrrtDQ8d+WW0owA4yV4LVH2juHyV9rQuYthPQwrqnX/U/3PHNswQhEmbFNCpS8vZgWW71gBFJECRQkIMyK+R"
            "DgZtvsOtV2Om5OBmomPZv795wLz/RLpB5gTMiIImEkF8+HQEEHXvr0xdXjzsjWO67QqiSX6J3uSyPdLEDAI2jc9Tj7"
            "2AGBCPOpnUVBB1Re6UrZkvDEa5HkkgXzlcw6XOr9OZixl/esOATDmopKEtBZKi2JBX7VVTIa4aLr5pW9DBSMQGPVAA"
            "Fu1FDXTw+6eAazqsCpeK+WOti6/zmfYiqlwkpiVhWUAzuxvyDrUfixbM7oXR+s7055wttEkcDBi1yN/lD7kc3np5RV"
            "MYHZsHbP853/mndes4mGkxe1gCDCwTvTgGMMuosBXATC3eaMsrbljlt6ETFgksV8ra8/6/t94npwOHVzVZgON8tmyD"
            "HO3kKCG82L073y1oNft/sqIsCD/7OYTzXUlyNKxFkqh+4eAwjeya2rNoIJbaKl3FhTTKx/v7+jlVXcgqUOzAXVoFK5"
            "sWTS2ff2xrN+tvbuxgICJjGn2iiL/2DDhx3d5SQ1YJRsfwbcmC96cNP5wxm7p+3cYHYE+z7f0UkpWpL2+EqGZRqDr3"
            "7Rt+VkV1mFc6AGbcyYdTYp4bM1fGMngKAxUKm8wcRolhyj2cHG607nEXo3+IqZXirjnn0c96kKQZa+t1J4Jlyse+TH"
            "45enZLbjRFuQ3Fv2BhB7SkiJV492/vBmHoHenZ+QfZ/t7PZwHkmkWEx14z0rBUNqGG171xXt1qm9A4MABov5syM4uj"
            "3YZ6VoNVE1FVSKigkY0CO5D5IbqZsfy+lo1nawjpIX2XRUTODCoYEzEluftUNKGIpR2c1Y9RGwhEssGAE7sQ1NXwus"
            "ADfr+WXBCHgZb568logN0e9ODJypKoEYH5u6ZDRoEg9+JLe+fGxwd5OwMuQXfPCLPjQIDfutFM+g5G14W7jd0XTyiR"
            "ZCWc8I+3f9ozQgT/cPfXTlwfwbUkb9tja9CHFuwjVsH2m+ZvvDn9m3gZeLnakqgS93nw07NFf+Q2YK8Jre/moSmHME"
            "Ts351lL94a+SuupQqY46bdHFSwf+/ympCgD8BxQORGJUan2aAAAAAElFTkSuQmCC"
        )
        badge = self.create(
            queries={
                "message": "PyPackIT",
                "logo": logo_light,
                "color": "rgb(0, 100, 0)",
            },
            params={
                "label": "Powered By"
            },
            attrs_img={
                "alt": "Powered by PyPackIT",
                "title": "Automated project management and DevOps by PyPackIT.",
            },
            attrs_a={"href": "https://pypackit.repodynamics.com"},
        )
        badge.set(params_dark={"color": "rgb(0, 100, 0)"})
        return badge
