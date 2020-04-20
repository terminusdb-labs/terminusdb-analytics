#!/usr/bin/env python3

from woqlclient.woqlClient import WOQLClient
from woqlclient import WOQLQuery as WOQL
from config import server_url, key, db_id


def create_schema(client: WOQLClient):
    schema = WOQL().when(True).woql_and(
        WOQL().doctype("GitHubRepo")
        .label("GitHub repo")
        .description("A GitHub repository")
        .property("github_repo_name", "string"),
        WOQL().doctype("GitHubRepoStar")
        .label("GitHub Repo Star")
        .description("GitHub Repo Star")
        .property("github_repo_star_username", "string")
        .property("github_repo_star_date", "dateTime")
        .property("github_repo_star_repo", "GitHubRepo"),
        WOQL().doctype("DockerRepo")
        .label("Docker Repo")
        .description("A Docker Hub Repo")
        .property("docker_repo_name", "string"),
        WOQL().doctype("DockerPullStat")
        .label("Docker Hub Pull statistic")
        .description("Contains amount of total pulls on a date")
        .property("docker_pull_stat_repo", "DockerRepo")
        .property("docker_hub_date", "dateTime")
        .property("docker_hub_pull_amount", "integer")

    )
    schema.execute(client)


if __name__ == "__main__":
    client = WOQLClient()
    client.connect(server_url, key)
    client.createDatabase(db_id, "Metrics DB")
    client = WOQLClient(server=server_url, key=key, db=db_id)
    create_schema(client)
