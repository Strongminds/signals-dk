# Signals-dk
Subtree project for the danish version of Signals

## Migrations

Two new database migrations handling translation of `Category` and `Permission` have been added.

## Repository

This repository serves as the parent repository for the **signals-dk** project, integrating multiple sub-projects (`frontend`, `backend`, etc.) using Git subtree. This setup allows for seamless collaboration, while maintaining the independence of the individual sub-project repositories.

### Structure

- `frontend`: Contains the frontend codebase, pulled from its dedicated repository.
- `backend`: Contains the backend codebase, pulled from its dedicated repository.

### Subtree Management Commands

#### Pull Updates from Subtree Repositories

To bring the latest changes from the upstream `frontend` or `backend` repositories into the `signals-dk` repository:

```
git subtree pull --prefix=frontend https://github.com/your-org/frontend.git main
git subtree pull --prefix=backend https://github.com/your-org/backend.git main
```

#### Push Changes Back to Subtree Repositories
If changes are made to the frontend or backend directories in this repository, push them back to the respective upstream repositories:

```
git subtree push --prefix=frontend https://github.com/your-org/frontend.git main
git subtree push --prefix=backend https://github.com/your-org/backend.git main
```

#### Add New Subtrees (If Needed)
To add a new subtree repository:

```
git subtree add --prefix=new-repo https://github.com/your-org/new-repo.git main
```

#### In a Dedicated Subtree Repository
You can also clone and work directly in the subtree repositories (e.g., frontend or backend) for independent development
