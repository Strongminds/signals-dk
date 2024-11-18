# STRONGMINDS observations

## General

- Ongoing (heavy) development going on simultaneously (eg frontend being revamped to a 'v2')
- MacOS preference for developers (Windows/WSL Ubuntu works as well) - problems were line endings, access rights and more

## Specific items

| Area | Title | Description |
|------------------|-----------------|-----------------|
| General    | Vulnerabilities    | Vulnerabilities in both frontend/backend packages    |
| Frontend   | Copy & paste components    | Eg RadioInput in both 'incident' and 'incident-management'    |
| Frontend   | Mix of JS & TS    | Eg Wizard step definitions in /signals/incident/definitions/    |
| Frontend   | Dutch language in code    | Eg Wizard step definitions    |

## PR changes that may affect signals (Amsterdam)

https://github.com/Strongminds/signals-dk/pull/1

- Added i18next and supporting libraries
- Rearranged incident definition code to be localizable
- backend/docker-compose.yml: Removed version
- backend/docker-compose/environments/.celery_beat: Added DATABASE enviroment variables

