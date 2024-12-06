- [ara usage](#ara-usage)
- [ara profiling](#ara-profiling)
- [Build \& Publish Base Docker Image for ARA CLI](#build--publish-base-docker-image-for-ara-cli)
- [ara-cli publish](#ara-cli-publish)
  - [best practices commit and merge and recreate workspace](#best-practices-commit-and-merge-and-recreate-workspace)
  - [update dependencies](#update-dependencies)
  - [test and run during development](#test-and-run-during-development)
  - [set version and build and install locally for testing outside of container](#set-version-and-build-and-install-locally-for-testing-outside-of-container)
  - [upload to test pypi with test pypi API key](#upload-to-test-pypi-with-test-pypi-api-key)
  - [upload to live pypi with talsen team production API key (from main branch)](#upload-to-live-pypi-with-talsen-team-production-api-key-from-main-branch)

# ara usage 
See [user readme](docs/README.md)
 
# ara profiling
go to workspace root and run:
> python -m cProfile -o output.prof ara_cli/__main__.py <valid ara command>

then output will be generated in 'output.prof'
then analyze output with
> python pstat_prof.py

# Build & Publish Base Docker Image for ARA CLI

```bash
bash ./docker/base/build.sh
```

# ara-cli publish
## best practices commit and merge and recreate workspace
1. commit and publish everything in the branch
2. go to git and merge
3. destroy old workspace from merged branch from within the working directory
   > workspace destroy
4. go back in to top level working directory and check which repos are available for branching
   > workspace repos
5. create new workspacce with workspace command: workspace new <repo> <new-workspace-name>
   > workspace new ara-cmd hans-ara-cmd
6. switch to new workspace 

## update dependencies
To update dependencies, add package names in `setup.py`. The packages will ONLY be installed automatically when the RELEASE version of ara-cli is installed (and NOT a test pypi version).

## test and run during development
1. run `bash deploy.sh`
2. run `bash login.sh`
3. --> in container --> for behave BDD tests `bash test-feature.sh` 
3. a) --> in container --> for only 1 test: behave ara/features/<name>.feature
3. b) --> in container --> for unit tests and (if successful) feature tests: `bash test-all.sh` 
4. --> in container --> for unit tests in folder ara_cli `pytest --cov=. --cov-report term-missing tests/ `
5. --> in container --> example for running a single unit test in ara_cli folder `pytest tests/test_template_manager.py::test_files_created_from_template`
6. if change is successfull always commit before proceeding with next change
7. if change was successfully reviewd merge in gitlab: https://git.talsen.team/talsen-products/ara-cli/-/merge_requests/new

## set version and build and install locally for testing outside of container
1. set the new verion in the ara_cli/version.py file
2. adapt the version number in the 'local_install.sh' file
3. use `bash local_install.sh` to control local setup procedure
4. Test the functionality


## upload to test pypi with test pypi API key
1. run `bash deploy.sh`
2. run `login.sh`
3. in `setup.py` and `local_install.sh` increment `version` otherwise upload will fail! 
3. a) merge to staging and continue from a new workspace
4. from inside container run `python setup.py sdist bdist_wheel`
5. run the following command: 

```bash
twine upload --repository testpypi dist/* --verbose -u __token__ -p pypi-AgENdGVzdC5weXBpLm9yZwIkZGI5YzUyZTUtNDhjMy00NmI3LTgxNmMtY2QwMTRjYjZmZjlmAAIqWzMsImM3ZTM0MDRmLWU1MzUtNDliMi05ZDhiLWQ0NGUyNzlmYTU0MiJdAAAGID-dX7aQZZimTyUQeKPzbP0TlqMEpLQlzRW7VJr1JKab
```

this will upload to a test pypi account.


6. run `python3 -m pip install --index-url https://test.pypi.org/simple/ ara_cli==<VERSION>`
7. run `ara -h`
8. if everything has worked (upload, installation and usage) you can now continue to upload the package to pypi (live)


## upload to live pypi with talsen team production API key (from main branch)
1. run `bash deploy.sh`
2. run `login.sh`
3. `dist` folder should still be there from the testupload (otherwise do `python setup.py sdist bdist_wheel` inside the container again), do NOT upload to live without previously testing in test pypi!
4. Get the API-Key from [nextcloud](https://cloud.talsen.team/apps/keeweb/?open=%2Finfrastructure%2Fpublic-services%2Fapi-keys.kdbx)
5. Get the Password from Hans or DevOps
6. run the following command: 
```bash
twine upload dist/* --verbose -u __token__ -p <API-Key>
```