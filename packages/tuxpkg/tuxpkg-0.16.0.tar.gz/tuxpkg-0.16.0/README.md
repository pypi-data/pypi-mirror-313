# tuxpkg
## release automation tool for Python projects


[![Pipeline Status](https://gitlab.com/Linaro/tuxpkg/badges/main/pipeline.svg)](https://gitlab.com/Linaro/tuxpkg/pipelines)
[![coverage report](https://gitlab.com/Linaro/tuxpkg/badges/main/coverage.svg)](https://gitlab.com/Linaro/tuxpkg/commits/main)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![PyPI - License](https://img.shields.io/pypi/l/tuxpkg)](https://gitlab.com/Linaro/tuxpkg/blob/main/LICENSE)

[Documentation](https://linaro.gitlab.io/tuxpkg) - [Repository](https://gitlab.com/Linaro/tuxpkg) - [Issues](https://gitlab.com/Linaro/tuxpkg/-/issues)

[TuxSuite](https://tuxsuite.com), a suite of tools and services to help with
Linux kernel development.

[[_TOC_]]



# Installing tuxpkg

There are several options for using tuxpkg:

- [From PyPI](install-pypi.md)
- [Debian packages](install-deb.md)
- [RPM packages](install-rpm.md)
- [Run uninstalled](run-uninstalled.md)



# gitlab CI pipeline
How to use:

!!!note
    [gpg manual](https://gnupg.org/documentation/manpage.html)

1. repository settings

  !!!note
      both the branch and repository tags must be protected!

  [Protected branch](https://docs.gitlab.com/ee/user/project/protected_branches.html)

  [Protected tags](https://docs.gitlab.com/ee/user/project/protected_tags.html)

2. CI/CD variables

The following variables must be set as protected in the CI/CD configuration:

- `TUXPKG_RELEASE_KEY`:
    - variable type: "file"
    - ascii-armored export of gnupg private key to sign the package repositories.  
  
    !!!note
        Because the private key will be uploaded into GitLab CI, you want to create a new GPG key
        for your project only. DO NOT upload your own private key! :-)
    
    ```shell
    gpg --export-secret-keys --armor KEYID
    ```

- `TUXPKG_RELEASE_KEYID`: 
    - variable type: "Variable"
    - variable options: "Protected"
    - the public gnupg key ID used to sign the package repositories. 
      The is the full GPG key id, e.g. `1EC68783C596C4AD1C2E45896D082F7024A0AEAF`.
  
    ```shell
    gpg -k
    ```

- `FLIT_PASSWORD`: 
    - variable type: "Variable"
    - variable options: "Protected, Masked"
    - Generate a project-specific token on [pypi.org](https://pypi.org/)
  
    !!!note
        [pypi api token help](https://pypi.org/help/#apitoken)

- `FLIT_USERNAME`:
    - variable type: "Variable"
    - variable options: "Protected"
    - set value to  `__token__`

The following variables don't need to be protected. They can be set in the
project settings as well, but it's probably better to set them explicitly in
`.gitlab-ci.yml`.

- `SKIP_BUILD_DEB`, `SKIP_BUILD_RPM`. Set these to `1` to skip building RPM and
  Debian packages, respectively.


3. Setup .gitlab-ci.yml file

```yaml
include:
  - https://gitlab.com/Linaro/tuxpkg/raw/main/gitlab-ci-pipeline.yml
variables:
  # ... override variables here (see below)
```

Variables that can be overriden locally:

- `TUXPKG`: how to call tuxpkg. Default: `tuxpkg`.
