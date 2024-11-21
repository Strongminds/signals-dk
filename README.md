# signals-dk
Subtree project for the danish version of Signals

## Porting database values

### Create temp table
The chosen strategy is to manually export data from the `signals_category` data to CSV format. Then use Google Sheets for translating the `name` and `handling_message` columns into the target language (eg `da`) by using the formula:
```
=GOOGLETRANSLATE(A2; "nl"; "da")
```
Export the result back into CSV, create a temporary table based on the needed data (columns: `id` `name` `handling_message`) and update the original table like:
```
UPDATE signals_category 
SET
    name = temp_signals_category_da."name" ,
    handling_message = temp_signals_category_da.handling_message 
FROM temp_signals_category_da
WHERE signals_category.id = temp_signals_category_da.signals_category_id;
```


## Git

### Subtrees
This project is a collection of **git subtrees** on which you can push changes to be merged into the parent, eg:
`git subtree push --prefix=/frontend signals-dk main`

Use the `--squash` option for pushing a single aggregated commit.

### Add subtree
Use the following commands for adding new subtrees:
`git remote add` _remoterepos_ `git@github.com:`_organization_`/?`_remoterepos_`.git`
`git subtree add --prefix=`_foldername_ _remoterepos_ `main --squash`
