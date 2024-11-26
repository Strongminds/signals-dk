# signals-dk
Subtree project for the danish version of Signals

## Migrations

Two new database migrations handling translation of `Category` and `Permission` have been added.

## Git

### Subtrees
This project is a collection of **git subtrees** on which you can push/pull changes to and from the parent, eg:

`git subtree push --prefix=frontend signals-frontend main` (for pushing the 
frontend)

`git subtree push --prefix=backend signals-backend main` (for pushing the backend)

`git subtree push --prefix=aws-infrastructure signals-aws-infrastructure main` (for pushing AWS infrastructure setup)

Likewise, you can `pull` in changes from the subtree repos.

**Keep Workflow Dependencies in Sync**: If the parent workflow depends on specific versions of subtree workflows, ensure the subtree changes are merged and available in their remote repositories before pushing the parent changes.

**Test Integration**: After pushing, verify the integration between parent and subtree workflows by triggering the appropriate events (e.g., by creating a release or manually running the workflows).

Use the script `./deployAll.sh` for pushing all subtree changes to their respective repos.

Avoid pushing using `--squash`, since this can potentially break committing to the subtree repos (in case they have been updated)

### Add subtree
Use the following commands for adding new subtrees:
`git remote add` _remoterepos_ `git@github.com:`_organization_`/?`_remoterepos_`.git`
`git subtree add --prefix=`_foldername_ _remoterepos_ `main --squash`
