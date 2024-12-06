## Installing the RPM packages 


!!! note
    tuxpkg requires Python 3.6 or newer.


To install tuxpkg on your system globally:

1. Create /etc/yum.repos.d/tuxpkg.repo with the following contents:

```shell
[tuxpkg]
name=tuxpkg
type=rpm-md
baseurl=https://linaro.gitlab.io/tuxpkg/packages/
gpgcheck=1
gpgkey=https://linaro.gitlab.io/tuxpkg/packages/repodata/repomd.xml.key
enabled=1
```

2. Install tuxpkg as you would any other package:

```shell
# dnf install tuxpkg
```

Upgrades will be available in the same repository, so you can get them using the same procedure you already use to get other updates for your system.
