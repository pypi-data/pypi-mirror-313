
## Installing the Debian packages


!!! note
    tuxpkg requires Python 3.6 or newer.


1. Download the repository signing key to /etc/apt/trusted.gpg.d/:

```shell
# wget -O /etc/apt/trusted.gpg.d/tuxpkg.gpg https://linaro.gitlab.io/tuxpkg/packages/signing-key.gpg

```
2. Create /etc/apt/sources.list.d/tuxpkg.list with the following contents:
```shell
deb https://linaro.gitlab.io/tuxpkg/packages/ ./
```

3. Install tuxpkg as you would any other package:

```shell
# apt update
# apt install tuxpkg
```

Upgrading tuxpkg will work just like it would for any other package (apt update, apt upgrade).
