# uh-libs

  * https://dev.azure.com/unitehereiu/Unite%20Here%20Development/_git/uh-libs

**uh-libs** is a collection of reusable Python library code, and CLI scripts of general use to UHIU devs.

## Getting started

Devs can get started by simply cloning the repo and running `rake venv:install_all\[dev\]` in the root directory of the project.

If you don't already have it installed, you will have to install `ruby` & the ruby build system `rake`, see links in references @ end of this document.

***TODO*** `venv:install_all` probably won't work in windows; do we need to support invokation from windows?

CLI interfaces provided are also available via a Docker container published to the UHIU registry by running:

***TODO*** example command to pull image & run command in it

## Environment Variables

Some of the provided scripts require environment variables be configured, on linux or mac this can be done a few ways

1. Create a shell init file, `export` it from there, and source it into your environment (or do this directly in your `~/.bashrc` and re-source it):
```sh
mkdir -p ~/.bash.d && touch ~/.bash.d/myvars && chmod 0600 ~/.bash.d/myvars
echo 'export SEPUEDE_API_KEY="hello"' >> ~/.bash.d/myvars
source ~/.bash.d/myvars
```
The first line creates the `~/.bash.d/myvars` file if it doesn't already exist, and sets permissions on the file such that only you can read & write to it.

The second line puts a var export into the file from the command line as an illustration, you can edit it in an editor instead.

Whenever you change your shell init files, they have to be re-sourced (changes are not automatically picked up), you can use `echo $SEPUEDE_API_KEY` to verify it is set.

2. If you don't want the var to persist in your shell always, or want to temporarily override it, just prefix the command you want to run with the setting (with no `export`):
```
SEPUEDE_API_KEY=hello odata-cli --list-entities
```

Be aware that this is not secure; you really shouldn't have secrets hanging around in your shell environment, or written unencrypted to disk.  Worse, when these vars are passed to docker, it will happen on the command line, so anyone with access to your machine can read them via `ps`, and worse still, `rake` echoes every command it is about to run to STDERR (normally a fantastic debugging feature), so anyone who can see your screen may see it

Still, it's a step in the right direction, until we have a better understanding of our secrets management requirements

***TODO*** how does one set env vars in windows?

### List of known environment variables

The library code itself does not read environment variables or interact with any sort of configuration at all, but some of the scripts provided do attempt to read the following; it is recommended if your project uses the same resources, you reuse the existing variable names when possible, to simplify your own configuration management:
```sh
export DOCKER_REGISTRY=uhiuregistry.azurecr.io
export PYTHONDONTWRITEBYTECODE=1
export SEPUEDE_API_KEY="<update me>"
export SEPUEDE_API_URL=""
export SEPUEDE_ODATA_URL=""
export STRIKEDB_HOST=""
export STRIKEDB_NAME=""  # or whatever db catalog you are using
export STRIKEDB_PASS="<update me>"
export STRIKEDB_USER=""
export STRIKEAPI_USER=""
export STRIKEAPI_PASS="<update me>"
export STRIKEAPI_TEST_URL=""
# if you are on linux & installed mssql-tools & msodbcsql17, you may also want to update your PATH:
export PATH="$PATH":/opt/mssql-tools/bin
```

## Using Rake

The developer workflow is augmented by a handful of Rake tasks, which help ensure docker images are built and managed consistently across the team, and provides some helper tasks for maintaining the library.

To see a list of tasks, use `rake -T`, some tasks may have longer descriptions which you can see with e.g. `rake -D docker:clean`
```
$ rake -T 
rake azure:acr:list_repositories                 # list repositories @ uhiuregistry
rake azure:acr:list_repository_tags[repository]  # list repository tags @ uhiuregistry
rake azure:acr:login                             # login to Azure Docker Registry
rake azure:login[use_device_code]                # login to az CLI
rake docker:acr:list_tags                        # list tags @ uhlibs in uhiuregistry registry
rake docker:acr:push[tag]                        # push image to docker registry
rake docker:build[tag]                           # build uhlibs image
rake docker:clean[rm_volume]                     # shutdown & remove uhlibs container & remove uhlibs image
rake docker:clean_all                            # reclaim space from old docker objects  WARNING: Destroys things
rake docker:run[cmd,tag]                         # run command in docker container, then exit container
rake docker:shell[tag]                           # run interactive bash shell in docker container
rake docker:sysinfo[incl_swarm]                  # display info about docker objects on system
rake docker:test[tag]                            # run unit tests in container
rake git:archive[branch,dest]                    # create tar.gz distribution of working dir
rake git:up[remote,branch]                       # does git pull --rebase in a manner consistent with never having merge commits
rake pkg:bumpmaj[tag_message]                    # bump major version part of MAJ.MIN.REV version string & tag repo
rake pkg:bumpmin[tag_message]                    # bump minor version part of MAJ.MIN.REV version string & tag repo
rake pkg:bumprev[tag_message]                    # bump revision part of MAJ.MIN.REV version string & tag repo
rake pkg:showver                                 # print package version
rake venv:clean                                  # clean up working dir
rake venv:install[dev_mode]                      # Create venv & pip install package & dependencies
rake venv:pip_freeze                             # used to maintain the pip-freeze.txt file
rake venv:test[exit_on_fail,pdb]                 # run tests & linter
rake venv:uninstall                              # clean as well as destroy virtualenv
```

## Managing dependencies

**uh-libs** is expected to be useful to a wide variety of project types (web services, data processors, report generators), working with a variety of technologies (server backends, file formats).

To avoid the situation where all clients have to install all dependencies, dependencies are grouped into optional sections.

When one runs `rake venv:install`, only the base package and core dependencies are installed.

One of the commands run during the course of the `rake venv:install\[1\]` task is currently:
```
pip install .[dev] .[flask] .[mongo] .[odata] .[odbc] .[pdf] .[postgres] .[redis]
```
`.[dev]` pulls in unit testing and linting stuff, the others are self-explanatory.

This allows `strike-reports` for example to specify in its dependencies `uh-libs uh-libs[flask] uh-libs[odbc]`, and not have to install the `[odata]` stuff.

# Managing with Poetry

## install poetry locally
It is important to not install poetry within the uh-libs package, it is not a dependency for uh-libs!!

Follow the guide at: https://python-poetry.org/docs/#installing-with-the-official-installer


## installing new packages

`poetry add <package name>`

To add the dependency as part of a group, i.e. "dev": 
`poetry add <package name> --group <group name>`

## deploying to PyPi
 * https://python-poetry.org/docs/cli/#publish

- Itterate the version in pyproject.toml
- Verify that tests pass
- Build the distributable with `poetry build`
- Publish distributable with `poetry publish`
Note: the apikey must be setup prior to publishing to pypi. `poetry config pypi-token.pypi <your-api-token>`

## Of interest

  * https://www.ruby-lang.org/en/downloads/
  * https://github.com/ruby/rake
  * https://python-poetry.org/docs/
