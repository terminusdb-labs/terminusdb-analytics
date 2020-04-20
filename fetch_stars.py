#!/usr/bin/env python3

import requests
import argparse

from woqlclient.woqlClient import WOQLClient
from woqlclient import WOQLQuery as WOQL
from config import server_url, key, db_id


def process_json(json_decoded):
    return [{'date': starred['starred_at'],
             'username': starred['user']['login']}
            for starred in json_decoded]

def insert_stars(client, repo, stars):
    repo_woql = {"@value": repo, "@type": "xsd:string"}
    repo_without_slash = repo.replace("/", "_")
    repo_without_slash_woql = {"@value": repo_without_slash, "@type": "xsd:string"}
    for star in stars:
        username_woql = {"@value": star['username'], "@type": "xsd:string"}
        insert_query = WOQL().when(WOQL().woql_and(
            WOQL().idgen("doc:GitHubRepo", [repo_without_slash_woql], 'v:GitHubRepoId'),
            WOQL().idgen("doc:GitHubRepoStar",
                        [repo_without_slash_woql, username_woql],
                        "v:GitHubStarId")
            ),
            WOQL().woql_and(
                WOQL().insert('v:GitHubRepoId', 'scm:GitHubRepo'),
                WOQL().add_triple('v:GitHubRepoId', 'scm:github_repo_name', repo_woql),
                WOQL().insert('v:GitHubStarId', 'scm:GitHubRepoStar'),
                WOQL().add_triple('v:GitHubStarId', 'scm:github_repo_star_date', {'@type': 'xsd:dateTime', '@value': star['date']}),
                WOQL().add_triple('v:GitHubStarId', 'scm:github_repo_star_username', username_woql),
                WOQL().add_triple('v:GitHubStarId', 'scm:github_repo_star_repo', 'v:GitHubRepoId')
            )
        )
        insert_query.execute(client)

def fetch_stars(repo):
    url = f'https://api.github.com/repos/terminusdb/terminus-server/stargazers?per_page=100'
    req = requests.get(url, headers={'Accept': 'application/vnd.github.v3.star+json'})
    json_decoded = req.json()
    stars = process_json(json_decoded)
    limit_not_reached = True
    page = 1

    while limit_not_reached:
        page = page + 1
        new_url = url + '&page=' + str(page)
        req = requests.get(new_url, headers={'Accept': 'application/vnd.github.v3.star+json'})
        json_decoded = req.json()
        if len(json_decoded) < 100:
            limit_not_reached = False
        stars = stars + process_json(json_decoded)
    return stars


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Fetch GitHub stars from a repo and put them in TerminusDB')
    parser.add_argument('repo_name', help="Repo name in the format owner/repo")
    args = parser.parse_args()
    client = WOQLClient(server=server_url, key=key, db=db_id)
    repo = args.repo_name
    stars = fetch_stars(repo)
    insert_stars(client, repo, stars)

