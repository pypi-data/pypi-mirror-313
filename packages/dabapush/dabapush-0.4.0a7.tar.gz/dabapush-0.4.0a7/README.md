# dabapush

Database pusher and version control for social media data – early-alpha version

![PyPI - Downloads](https://img.shields.io/pypi/dm/dabapush)
![GitHub top language](https://img.shields.io/github/languages/top/Leibniz-HBI/dabapush)
![GitHub commit activity](https://img.shields.io/github/commit-activity/m/Leibniz-HBI/dabapush)
![GitHub License](https://img.shields.io/github/license/Leibniz-HBI/dabapush)
![GitHub Actions Tests](https://github.com/Leibniz-HBI/dabapush/actions/workflows/main.yml/badge.svg)
![GitHub Issues or Pull Requests](https://img.shields.io/github/issues-pr/Leibniz-HBI/dabapush)
![GitHub Issues or Pull Requests](https://img.shields.io/github/issues/Leibniz-HBI/dabapush)


---

## Using dabapush

`dabapush` is a tool to read longer running data collections and write them to another file format or persist them into a database. It is designed to run periodically, e.g. controlled by chron, thus, for convenience ot use project-based configurations which contain all required information on what to read where and what to do with it.
A **project** may have one or more **jobs**, each job consists of a reader and a writer configuration, e.g. read JSON-files from the Twitter API that we stored in folder `/home/user/fancy-project/twitter/` and write the flattened and compiled data set in to `/some/where/else` as CSV files.


```text

Usage: dabapush [OPTIONS] COMMAND [ARGS]...

  Dabapush

Options:
  -l, --logfile FILENAME  File to log in, defaults to stdout.
  -v, --verbose           Increases verbosity, maximally vvvv.
  --version               Show the version and exit.
  --help                  Show this message and exit.

Commands:
  create
  reader  reader command
  run     Run dabapush job in the current working directory.
  update  Update the project's status.
  writer  writer command
```
### First steps

In order to run a first `dabapush`-job we'll need to create a project configuration. This is done by calling:

```bash
dabapush create
```

By default this walks you through the configuration process in a step-by-step manner. Alternatively, you could call:

```bash
dabapush create --non-interactive
```

This will create an empty configuration, you'll have to fill out the required information by e.g. calling:

```bash
dabapush reader add NDJSON default
dabapush writer add CSV default
```

Whereas `reader add`/`writer add` is the verb, `NDJSON` or `CSV` is the plugin to add and `default` is the pipeline name.

Of course you can edit the configration after creation in your favorite editor, but **BEWARE NOT TO TEMPER WITH THE YAMl-TAGS!!!**.

To run the newly configured job, please call:

```bash
dabapush run default
```

## Command Reference

### Invocation Pattern

```bash
dabapush <command> <subcommand?> <options>
```

### Commands

`create` -- creates a dabapush project (invokes interactive prompt)

Options:

`--non-interactive`, create an empty configuration and exit

`--interactive`, *this is the default behavior*: prompts for user input on

- project name,
- project authors name,
- project author email address(es) for notifications
- manually configure targets or run discover?

----

`run all` -- collect all known items and execute targets/destinations

`run <target>` -- run a single writer and/or named target

----

`reader` -- interact with readers

`reader configure <name>` -- configure the reader for one or more subproject(s); Reader configuration is inherited from global to local level; throws if configuration is incomplete and defaults are missing

`reader list`: returns a table of all configured readers, with `<path> <target> <class> <id>`

`reader list_all`: returns a table of all registered reader plugins

`reader add <type> <name>`: add a reader to the project configuration

Options:

`--input-directory <path>`: directory to be read

`--pattern <pattern>`: pattern for matching file names against.

`remove <name>`: remove a reader from the project configuration.

----

`writer` -- interact with writers

`writer add <type> <name>`:

`writer remove <name>`: removes the writer for the given name

`writer list` -- returns table of all writers, with `<path> <subproject-name> <class> <id>`

`writer list_all`: returns a table of all registered writer plugins

`writer configure <name>` or `writer configure all`


## Extending dabapush and developers guide

Dabapush's reader and writer plug-ins are registered via entry point: `dabapush_readers` for readers and `dabapush_writers` for writers. Both expect `Configuration`-subclass.

### Developer Installation

1. Install [poetry](https://python-poetry.org/docs/#installation)
2. Clone repository
3. In the cloned repository's root directory run `poetry install`
4. Run `poetry shell` to start development virtualenv
5. Run `dabapush create` to create your first project.
6. Run `pytest` to run all tests
