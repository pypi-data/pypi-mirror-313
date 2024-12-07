from .ips import *
from .netfinder import fetch, get_soup


def usage_pd(
    url="https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.to_clipboard.html",
    dir_save=None,
):
    # extract each usage from its url
    def get_usage(url):
        # extract each usage from its url
        print(f"trying: {url}")
        sp = get_soup(url, driver="se")
        return fetch(sp, where="dt")[0]


    if dir_save is None:
        if "mac" in get_os():
            dir_save = "/Users/macjianfeng/Dropbox/github/python/py2ls/py2ls/data/"
        else:
            dir_save = "Z:\\Jianfeng\\temp\\"
    sp = get_soup(url, driver="se")
    links_all4lev1 = fetch(sp, where="a", get="href", class_="reference internal")
    links_level_1 = [
        strcmp(link, links_all4lev1)[0].replace(
            "../", "https://pandas.pydata.org/docs/reference/"
        )
        for link in links_all4lev1
        if not link.startswith("pandas")
    ]
    dict_usage = {}
    for link_level_1 in links_level_1:
        sp = get_soup(link_level_1, driver="se")
        links_all = fetch(sp, where="a", get="href", class_="reference internal")

        filtered_links = unique(
            [
                i
                for i in links_all
                if any([i.startswith(cond) for cond in ["pandas", "api"]])
            ]
        )
        links = [
            (
                "https://pandas.pydata.org/docs/reference/api/" + i
                if not i.startswith("api")
                else "https://pandas.pydata.org/docs/reference/" + i
            )
            for i in filtered_links
        ]
        usages = [get_usage(i) for i in links]
        for usage, link in zip(usages, links):
            if usage.startswith("DataFrame"):
                usage = usage.replace("DataFrame", "df")
            if usage.startswith("pandas"):
                usage = usage.replace("pandas", "pd")
            if usage.endswith("[source]#"):
                usage = usage.replace("[source]#", "")
            if usage.endswith("#"):
                usage = usage.replace("#", "")
            str2rm = ["class", "property"]
            for str2rm_ in str2rm:
                if usage.startswith(str2rm_):
                    usage = usage.replace(str2rm_, "")
            funcname = ssplit(usage, by="(")[0]
            dict_usage.update({funcname: usage + f"\n{link}"})
    # save to local
    dir_save += "/" if not dir_save.endswith("/") else ""
    fsave(
        dir_save + "usages_pd.json",
        dict_usage,
    )
def usage_sns(
    url="https://seaborn.pydata.org/generated/seaborn.swarmplot.html",
    dir_save=None,
):
    """
    Fetches usage examples of various Seaborn plotting functions from the Seaborn documentation website.
    It filters the relevant plot-related links, extracts usage examples, and saves them in a JSON file.

    Parameters:
    - url (str): URL of the Seaborn page to start extracting plot usages (default is swarmplot page).
    - dir_save (str): Directory where the JSON file containing usages will be saved (default is a local path).

    Saves:
    - A JSON file named 'usages_sns.json' containing plotting function names and their usage descriptions.

    Returns:
    - None
    """

    # extract each usage from its url
    def get_usage(url):
        print(f"trying: {url}")
        sp = get_soup(url, driver="se")
        return fetch(sp, where="dt")[0]

    if dir_save is None:
        if "mac" in get_os():
            dir_save = "/Users/macjianfeng/Dropbox/github/python/py2ls/py2ls/data/"
        else:
            dir_save = "Z:\\Jianfeng\\temp\\"
    sp = get_soup(url, driver="se")
    links_all = fetch(sp, where="a", get="href", class_="reference internal")
    filtered_links = unique(
        [
            i
            for i in links_all
            if not any(
                [
                    i.startswith(cond)
                    for cond in [
                        "seaborn.JointGrid",
                        "seaborn.PairGrid",
                        "seaborn.objects",
                    ]
                ]
                + ["plot" not in i]
            )
        ]
    )
    links = ["https://seaborn.pydata.org/generated/" + i for i in filtered_links]

    usages = [get_usage(i) for i in links]
    dict_usage = {}
    for usage, link in zip(usages, links):
        dict_usage.update(
            {ssplit(usage, by="(")[0].replace("seaborn.", ""): usage[:-1] + f"\n{link}"}
        )
    # save to local
    dir_save += "/" if not dir_save.endswith("/") else ""
    fsave(
        dir_save + "usages_sns.json",
        dict_usage,
    )


def main():
    # update pandas usage to local
    usage_pd()
    # usage_sns()


if __name__ == "__main__":
    main()
