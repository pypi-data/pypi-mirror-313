# Developer Documentation
Please use this file to capture relevent information for developers to manage this project.

## Publishing to PYPI
### Pre-requisites
* A PYPI account with permissions to publish to the project
* A PYPI API token with permissions to publish to the project
  * Set your Poetry config to use the PYPI API token by running `poetry config pypi-token.pypi <API_TOKEN>` include the `pypi-` prefix in the token name
### Versioning
* In the repository root directory using `CMD` type `poetry version <version>` where `<version>` is the new version number in the format `MAJOR.MINOR.PATCH`
* You will be prompted for your PYPI username and password, enter your PYPI username and the API token
* The version number will be updated in the `pyproject.toml` file and a new git tag will be created with the version number
### Build
* Built wheel, `whl`:
  * Building the `whl` for publishing to PYPI, in the repository root directory using `CMD` type `poetry build --format wheel`
### Publishing
In the repository root directory using `CMD` with `.venv` active, `poetry shell`:
1. Update version, get the current version with `poetry version`, update to a new version with `poetry version <version>` where `<version>` is the new version number in the format `MAJOR.MINOR.PATCH`
2. Build with `poetry build --format wheel`
3. Publish with `poetry publish`


## Migration from Bitbucket steps
Migrating a repository from Bitbucket to GitHub while retaining branches and version history involves several steps.

1. **Clone the Bitbucket Repository**:
   ```bash
   git clone --mirror https://bitbucket.org/username/repo.git
   cd repo.git
   ```

2. **Create a New Repository on GitHub**:
   - Go to GitHub and create a new repository. Do not initialize it with a README, .gitignore, or license.

3. **Push to the New GitHub Repository**:
   ```bash
   git remote add github https://github.com/username/new-repo.git
   git push --mirror github
   ```

4. **Verify the Migration**:
   - Check the new GitHub repository to ensure all branches and commit history are present.

5. **Update Remote URLs (Optional)**:
   - If you want to continue working with the new GitHub repository, update the remote URL in your local repository:
   ```bash
   git remote set-url origin https://github.com/username/new-repo.git
   ```

6. **Branch for restructure work**
Create a standardised Python application structure
  - Main directory with just:
     -  `build.py`
     -  `poetry` files
     -  `license`
     -  `gitignore` and 
     -  `readme.md`
  -  Sub directories
     -  `.github`
        -  `workflows`
           -  `main.yml`
           -  `release.yml`
     - `transformation`
       - `__init__.py`
       - `pytrans.pyx`
       - `pytrans.cpp`
       - `etc`
     - `test`
     - `bindings`
     - `documentation` 

7. **Check that Github actions are working**
  - Test completing with success
  - Deployment to pypi when pushed to a release branch