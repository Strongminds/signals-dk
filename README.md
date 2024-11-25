# signals-dk
Subtree project for the danish version of Signals

## Migrations

Two new database migrations handling translation of `Category` and `Permission` have been added.

## Git

### Subtrees
This project is a collection of **git subtrees** on which you can push changes to be merged into the parent, eg:
`git subtree push --prefix=/frontend signals-dk main`

Use the `--squash` option for pushing a single aggregated commit.

### Add subtree
Use the following commands for adding new subtrees:
`git remote add` _remoterepos_ `git@github.com:`_organization_`/?`_remoterepos_`.git`
`git subtree add --prefix=`_foldername_ _remoterepos_ `main --squash`
