#!/usr/bin/env python3

import requests


def process_json(json_decoded):
    for starred in json_decoded:
        print(starred["starred_at"] + "," + starred["user"]["login"])


repo = "terminusdb/terminus-server"
url = f'https://api.github.com/repos/terminusdb/terminus-server/stargazers?per_page=100'
req = requests.get(url, headers={'Accept': 'application/vnd.github.v3.star+json'})
print("Starred_At,Starred_By")
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
    process_json(json_decoded)

