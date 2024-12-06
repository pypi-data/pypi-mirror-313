# Deployment

---

<div class="hide-next-element"></div>

### Table of Contents

<div class="hide-next-element"></div>

* [Initial Deployment](#initial-deployment)
* [Subsequent Deployment](#subsequent-deployment)

<div class="hide-next-element"></div>

---

<a name="initial-deployment"></a>
### Initial Deployment

* *(Required for initial publication on PyPI as needed)* Register a [new account on PyPI](https://pypi.org/account/register/) (do the same for Test PyPI as needed).

* *(Required for initial publication on PyPI)* Configure [API token authentication for PyPI](https://pypi.org/help/#apitoken) by creating an API token (do the same for Test PyPI as needed) and copy the value of the API token.

* *(Required for initial publication on PyPI)* Create a `.env` file by running `cp .env.template .env` in the command line from the project root directory and paste the PyPI API token from the previous step as the value for `UV_PUBLISH_TOKEN` (this environment variable is used in the Makefile by `uv publish` to [publish the package using uv](https://docs.astral.sh/uv/guides/publish/#publishing-your-package)).

* *(Optional after initial package publication on PyPI)* Configure a *new* [package-specific PyPI API token](https://pypi.org/help/#apitoken) and update the above `UV_PUBLISH_TOKEN` environment variable in the `.env` to use it.

* *(Optional if using Twine)* Install `twine` (if not already installed) with `uv add twine`.

* *(Optional if using custom domain for GitHub Pages)* Follow the [steps for managing a custom domain for GitHub Pages](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/managing-a-custom-domain-for-your-github-pages-site).

  * If you want to use a subdomain, you should follow the [steps for configuring a subdomain for GitHub Pages](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/managing-a-custom-domain-for-your-github-pages-site#configuring-a-subdomain), which require the creation of a `CNAME` DNS record for your custom domain.
  
  * ***Note***: If you are using CloudFlare and you create a `CNAME` record for your GitHub Pages subdomain, you must turn off "Proxy status" so that it is "DNS only" or else HTTPS will not work!

---

<a name="subsequent-deployment"></a>
### Subsequent Deployment

* *(Optional)* Check `pyproject.toml` for latest dependency versions.

* *(Optional)* Update virtual machine with the latest dependencies (`make update` in Makefile):
```shell
uv sync --all-extras --dev
```

* Lint code with `ruff` (`make lint` in Makefile):
```shell
ruff check .
```

* Check code security with `bandit` (`make secure` in Makefile):
```shell
bandit -c pyproject.toml -r .
```

* *(Optional)* Run *all* `pytest` tests (see following commands for running subsets of tests) (`make test_code` in Makefile):
```shell
uv run pytest tests
```

* *(Optional)* Run *all* `pytest` tests *verbosely*:
```shell
 uv run pytest -v -s tests
```

* *(Optional)* Run all tests from `pytest` file:
```shell
uv run pytest -v -s tests/test_pyobjson.py
```

* *(Optional)* Run *specific* test from `pytest` file:
```shell
uv run pytest -v -s tests/test_pyobjson.py -k test_main
```

* *(Optional)* Test Python support using [act](https://github.com/nektos/act) for GitHub Actions:
```shell
act -j build
```

***Note***: If `act` is unable to locate Docker, make sure that the required `/var/run/docker.sock` symlink exists. If it does not, you can fix it by running:
```shell
sudo ln -s "$HOME/.docker/run/docker.sock" /var/run/docker.sock`
```

***Note***: If you are running macOS on a devices with an M-series chip (Apple Silicon), you will need to specify `linux/amd64` architecture when running `act`:
```shell
act --container-architecture linux/amd64 -j build
```

* *(Optional)* Build the PyPI package independent of deployment:
```shell
make build
```

* *(Optional)* Test packages for PyPI deployment:
```shell
make verify_build
```

* *(Optional)* Check MkDocs documentation by serving it at [http://localhost:8000/](http://localhost:8000/) locally:
```shell
make test_docs
```

* *(Optional)* Build the PyPI package and MkDocs documentation independent of deployment:
```shell
make docs
```

***Note***: Running `make test_docs` from the previous step recreates the documentation without building the PyPI package.

* Create a git commit:
```shell
git add .
git commit -m 'commit message'
```

* Update the git tag with the new version (`git tag -a [tag_name/version] -m [message]`):
```shell
git tag -a v1.0.0 -m 'release message'
git push origin --tags
```

* *(Optional)* Test deployment by building the PyPI packages, recreating the documentation, and deploying to Test PyPI:
```shell
make uv_test_deploy
```

* Deploy the package by building it, recreating the documentation, and deploying the package to PyPI:
```shell
make uv_deploy
```

* Create a second git commit with updated version number and documentation:
```shell
git add .
git commit -m 'updated version number and documentation'
```

* Update package git repository:
```shell
git push
```
