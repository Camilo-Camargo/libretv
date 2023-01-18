import time

import uvicorn

from git import Repo, RemoteProgress
from git import InvalidGitRepositoryError, NoSuchPathError

from database import (category, language, country, country_language,
                      subdivision, subdivision_country, channel,
                      channel_language, channel_category, blocklist,
                      stream)


from constants import (IPTV_DATABASE_URL,
                       IPTV_DATABASE_PATH,
                       IPTV_STREAM_URL,
                       IPTV_STREAM_PATH,
                       IPTV_EPG_URL,
                       IPTV_EPG_PATH
                       )


class CloneProgress(RemoteProgress):
    def update(self, op_code, cur_count, max_count=None, message=""):
        print(f"\r{int(cur_count)}/{int(max_count)}: {message}", end="")


def load_repo(url, path):
    """
    Clone or Update a repository based on url
    return: Repo Object
    """

    # Check if the repository exists if not fetch it
    print(f"[Warning]: Fetching iptv-org repository at {url}")

    try:
        repo = Repo(path)
    except (InvalidGitRepositoryError, NoSuchPathError):
        repo = Repo.clone_from(
            url=url,
            to_path=path,
            progress=CloneProgress(),
            branch="master"
        )

    # Check updates
    repo.remotes.origin.pull(progress=CloneProgress())

    # Get the date and the last commit
    head = repo.head
    last_commit = head.commit
    print(f"Branch: {head.reference}")
    print(f"Last Commit: {last_commit}")
    print(f"{last_commit.message}")
    last_commit_date = time.gmtime(last_commit.committed_date)
    last_commit_date = time.strftime('%Y-%m-%d %H:%M:%S', last_commit_date)
    print(last_commit_date)

    return repo


if (__name__ == "__main__"):
    # load database
    repos = [
        load_repo(IPTV_DATABASE_URL, IPTV_DATABASE_PATH),
        load_repo(IPTV_STREAM_URL, IPTV_STREAM_PATH),
        load_repo(IPTV_EPG_URL, IPTV_EPG_PATH)
    ]

    # loading data to mysql database
    category.load()
    print("Category loaded")
    language.load()
    print("Language loaded")
    country.load()
    print("Country loaded")
    country_language.load()
    print("Country_Language loaded")
    subdivision.load()
    print("Subdivision loaded")
    subdivision_country.load()
    print("Subdivision Country loaded")
    channel.load()
    print("Channel loaded")
    channel_language.load()
    print("Channel Language loaded")
    channel_category.load()
    print("Channel Category Loaded")
    blocklist.load()
    print("BlockList Loaded")
    stream.load()
    print("Stream Loaded")

    #  Running the GraphQL server
    print("[Warning]: running the server with uvicorn")
    uvicorn.run("api:app")
