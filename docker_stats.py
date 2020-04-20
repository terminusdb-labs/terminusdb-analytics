#!/usr/bin/env python3

from woqlclient.woqlClient import WOQLClient
from woqlclient import WOQLQuery as WOQL
from config import server_url, key, db_id

import argparse
import datetime
import requests


def fetch_docker_pulls(docker_repo: str):
    url = f'https://hub.docker.com/v2/repositories/{docker_repo}/'
    json_decoded = requests.get(url).json()
    return json_decoded["pull_count"]

def insert_docker_pulls(docker_repo: str, pull_amount: int, client: WOQLClient):
    today = f"{datetime.datetime.now():%Y-%m-%dT%H:%M:%S}"
    repo_without_slash = docker_repo.replace("/", "_")
    repo_without_slash_woql = {"@value": repo_without_slash, "@type": "xsd:string"}
    date_woql = {"@value": today, "@type": "xsd:dateTime"}
    repo_woql = {"@value": docker_repo, "@type": "xsd:string"}
    insert_query = WOQL().when(WOQL().woql_and(
        WOQL().idgen("doc:DockerRepo", [repo_without_slash_woql], 'v:DockerRepoId'),
        WOQL().idgen("doc:DockerPullStat",
                     [repo_without_slash_woql, {'@type': 'xsd:string', '@value': today}],
                     "v:PullStatId")
        ),
        WOQL().woql_and(
            WOQL().insert('v:DockerRepoId', 'scm:DockerRepo'),
            WOQL().add_triple('v:DockerRepoId', 'scm:docker_repo_name', repo_woql),
            WOQL().insert('v:PullStatId', 'scm:DockerPullStat'),
            WOQL().add_triple('v:PullStatId', 'scm:docker_hub_date', date_woql),
            WOQL().add_triple('v:PullStatId', 'scm:docker_pull_stat_repo', 'v:DockerRepoId'),
            WOQL().add_triple('v:PullStatId', 'scm:docker_hub_pull_amount', pull_amount)
        )
    )
    insert_query.execute(client)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Fetch Docker Pulls from a repo and put them in TerminusDB')
    parser.add_argument('repo_name', help="Repo name in the format owner/repo")
    args = parser.parse_args()
    docker_repo = args.repo_name
    client = WOQLClient(server=server_url, key=key, db=db_id)
    docker_pulls = fetch_docker_pulls(docker_repo)
    insert_docker_pulls(docker_repo, docker_pulls, client)
