
[![GibsonAI](https://github.com/user-attachments/assets/26bc1002-f878-4995-a6c5-eb8d5eb69c28)](https://gibsonai.com/)

# Gibson CLI

[![PyPI - Version](https://img.shields.io/pypi/v/gibson-cli)](https://pypi.org/project/gibson-cli/)
![Python 3.9+](https://img.shields.io/badge/Python-3.9%2B-blue)
[![Docs](https://img.shields.io/badge/Docs-https://docs.gibsonai.com-green)](https://docs.gibsonai.com)

## Prerequisites

Gibson currently works on projects that use Python 3.9 or greater, MySQL, SQLAlchemy, Pydantic, Alembic, FastAPI and pytest. It is capable of building a complete application, from database to API end points, using these frameworks. Future enhancements of Gibson will include support for more languages and frameworks.

Portions of the Gibson backend code are written by Gibson.  So far, versus a human developer, it has coded 66% of the software and did so in seconds. To get started, read the instructions here.

## Installation / Upgrading

Install the latest version of the CLI using `pip`

```sh
pip3 install gibson-cli --upgrade
```

Note: the first time you install any package from PyPI via `pip` that includes an executable, it is placed in a directory that is likely not in your `PATH`. There are a number of ways to do this, but one method is to run the following command:

```sh
echo 'export PATH="$PATH:${$(which python3)%python3}"' >> ~/.zshrc # or ~/.bashrc
```

You will only need to do this once.

## Key Terms

- Dev Mode
  - Turn dev mode on to have Gibson write code for you as you execute commands.

- Entity | Entities
  - Synonymous with a table name or data structure.

- Memory
  - There are two types of memory: stored (long term) and last (the last action taken).

- Merge
  - Merge the entities in the last memory into the stored memory.

## Memory Concepts

There are two types of memory maintained by the Gibson CLI:

- `stored` (long term)
- `last` (short term)

When you import a datastore or API project into Gibson it stores the schema and all of its entities in stored memory. Stored memory is long term. It contains a copy of your database schema and represents the currently stable version of it.

Each time you ask Gibson to do something that results in a new or modified entity it will store it in last memory. Any time you ask the CLI to perform a coding task it will prefer last memory first, then stored memory.

Let's consider a more concrete example. You imported your datastore into the CLI and one of the tables is called "user". You execute:

`gibson modify user I want to add nickname`

So Gibson creates a new version of the user table containing a nickname column. This new table is stored in last memory.  If you execute:

`gibson code models`

The CLI will write the code for what is sitting in last memory.

This means you can make changes, try things out and decide if you want to make the changes permanent before merging the changes from last to stored.  You can easily forget the last changes you made by executing:

`gibson forget last`

When you're ready to commit, just execute:

`gibson merge`

Everything in last will be moved to stored and last will be forgotten. Finally, if you want Gibson to recreate your database schema with all the recent changes, just execute:

`gibson build datastore`

Just note, build will first drop all of the tables in the datastore then recreate the database from scratch.

## Logging in

Run `gibson auth login` to login to Gibson with your Google account.

## Acquiring an API Key

While in beta, you have to acquire an API manually:

- Go to <https://app.gibsonai.com/>.
- Chat with Gibson and create a new project.
- When your project is complete Gibson will email you the API key.
- gibson conf api::key [API key]

## Usage

The main command is located in `bin/gibson`. Executing this command with no parameters will provide a help style menu to guide you.

## Configuration

All of Gibson's configuration files and caches are stored in `$HOME/.gibson`. Use `gibson conf` for updating the configuration and `gibson forget` for clearing caches.

### For Windows Users

- Make sure that you have an environment variable called HOME set. Gibson will store its configuration files and caches in this directory. We recommend you keep this directory outside of any repository to which you might be committing.
- To execute the `gibson` command, follow these instructions:
  - Assuming the gibson executable is in `c:\Users\\[me]\projects\gibson\bin`
  - Run `python c:\Users\\[me]\projects\gibson\bin\gibson`

## Editor Integration

### vim

- Make sure the `gibson` command is in your path by editing the `PATH` environment variable
- Edit `~/.vimrc`
- Add the following:
  - `:command! -nargs=* Gibson r ! gibson <args>`
- Open a file and execute commands:
  - `:Gibson module abc`
  - `:Gibson code models`
  - `:Gibson code schemas`

## Currently Supported Software

- Python 3.9 or greater
- MySQL
- SQLAlchemy
- Pydantic
- Alembic
- FastAPI
- pytest

More languages and frameworks are in active development. If you do not see a version that you need let us know and we will get on it.

## Coming Very Soon

- pytest based unit tests for all of the code Gibson writes.
  - We know this is critical for Gibson to prove that its code is production-grade and bug free. As a development team, we need this too. It is coming in short order.
- Enhanced AI commands at your finger tips with code output and scratch storage.
  - [DONE] See "Asking Gibson Questions With Context"
- Context aware coding from your Github repository.
  - gibson scan
- AI based feedback directly to Gibson's creator:
  - `gibson tell mike [hopefully nice things]`
    - e.g. `gibson tell mike we need support for postgres`
    - or, `gibson tell mike to hire me, I want to work on gibson`
- Significant data modeling improvements.
- The ability to integrate and download Function code using `gibson`.
  - Along with a number of new Functions.
- Full FastAPI coding including module and entity specific dispatchers.

## Detailed How-To

### First Step

- Just run `gibson`. He will say hello and walk you through set up.

### Configuring Your API Key

`gibson conf api::key [API key]`

### Configuring Your Datastore

`gibson conf datastore::type mysql`
`gibson conf datastore::uri mysql+pymysql://[user]:[password]@[host]/[database name]`

Note: Gibson currently only supports MySQL. Let us know if you need something else.

### Turning On Dev Mode

`gibson dev on`

- We suggest you turn dev mode on and leave it on. With it enabled, Gibson will act like your coworker and write code as you execute commands.

- You will need to provide 3 paths: `base` (where you want project base code to go), `model` (where you want SQLAlchemy models to go) and `schema` (where you want Pydantic schemas to go).

### Importing Your Datastore

`gibson import mysql` or `gibson import pg_dump /path/to/pg_dump.sql` or `gibson import openapi /path/to/openapi.json`

- This will make Gibson's stored memory aware of all of your datastore objects.
- In addition to making Gibson aware, this will write all of the base, model and schema code for you.

### Configuring a Custom BaseModel

You may be using a custom SQLAlchemy BaseModel and you do not want Gibson to use the one it has written.

```sh
gibson conf code::custom::model::class [class name]
gibson conf code::custom::path [import path]
```

For example, you might provide class name = `MyBaseModel` and import path = `project.model.MyBaseModel`

### Writing the Base Code

`gibson code base`

### Writing the Code for a Single Model

`gibson code model [entity name]`

### Writing the Code for a Single Schema

`gibson code schema [entity name]`

### Writing the Code for All Models

`gibson code models`

### Writing the Code for All Schemas

`gibson code schemas`

### Adding a New Module to the Software Using AI

- gibson module [module name]
  - e.g. gibson module user
- Gibson will display the SQL tables it has generated as a result of your request. It will store these entities in its last memory.
- `gibson code models`
- This will write the code for the entities it just created.
- `gibson merge`
- This will merge the new entities into your project.
- Note, at the moment Gibson does not build the tables into your datastore.

### Making Changes to the Software Using AI

- `gibson modify [entity name] [natural language request]`
  - e.g. `gibson modify my_table I want to add a new column called name and remove all of the columns related to email`
- Gibson will display the modified SQL table and store it in its last memory.
- `gibson code models`
- This will write the code for the modified entity.
- `gibson merge`
- This will merge the modified entity into your project.
- Note, at the moment Gibson does not build the modified table into your datastore.

### Forgetting Things Stored in Memory

- `gibson forget stored`
- `gibson forget last`
- `gibson forget all`

### Building All of the Entities in Stored Memory into the Datastore

`gibson build`

### Showing an Entity that is Stored in Memory

`gibson show [entity name]`

### Building a Project End-to-End Using AI

- Go to <https://app.gibsonai.com/>.
- Chat with Gibson and create a new project.
- When your project is complete Gibson will email you the API key.
- `gibson conf api::key [API key]`
- `gibson import api`
- Magic, no?

### Integrating a Model into Your Code

Gibson creates base-level SQLAlchemy models. To integrate them just do this:

```py
from my_project.gibsonai.model.Module import ModuleBase

class MyModule(ModuleBase):
    pass
```

- When you need to add custom business logic to the model, just modify your version of the model:

```py
from my_project.gibsonai.model.Module import ModuleBase

class MyModule(ModuleBase):
    def my_custom_business_logic(self):
        return 1 + 1
```

We strongly suggest you do not reference the base-level SQLAlchemy models directly. By sub-classing you won't have to refactor your code if you decide to add custom code.

### Integrating a Schema into Your Code

At the moment, just refer to the base-level schema directly.

### Migrating Your Software from PHP to Python

- Configure your datastore
- Turn on Dev Mode
- `gibson import mysql` (alternatively import from pg_dump or openapi)
- 70% of your code is written, customize the remaining

### Asking Gibson Questions With Context

- `gibson q [natural language request]`
- Your natural language request can include:
  - `file://[full path]` to import a file from the filesystem
  - `py://[import]` to import a file from `PYTHONPATH`
  - `sql://[entity name]` to import the SQL
- For example:
  - `gibson q format file:///Users/me/file.py for PEP8`
  - `gibson q code review py://user.modules.User`
  - `gibson q add nickname to sql://user`
- When using `sql://`, any entities that are created as part of Gibson's response will be transferred into Gibson's last memory allowing you to execute a query, create a new entity and have Gibson immediately create a model or schema from it.
  - e.g. `gibson q add nickname to sql://user`
  - `gibson code model user`

## Contributing

- Clone this repository somewhere in your file system
- `pip3 install [path to this repository]`
