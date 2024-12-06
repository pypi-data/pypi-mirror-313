
# tuxpkg Subcommands


## create-repository [repo]

Creates Debian and RPM repository from files in dist/.

```shell
tuxpkg create-repository
```

## release

Makes a release

```shell
tuxpkg release
```

## init 

Initializes a project directory

```shell
tuxpkg init
```

## get-makefile [mk]

Prints the path to the tuxpkg shared makefile. It can be included in a Makefile using a construct like like `$(include $(shell tuxpkg get-makefile))`

```shell
tuxpkg get-makefile
```

## get-debian-rules

Prints the path to the tuxpkg shared debian/rules. It can be included in a your debian/rules using a construct like like `$(include $(shell tuxpkg get-debian-rules))`. You just need to set PYBUILD_NAME first.

```shell
tuxpkg get-debian-rules
```

## show current version [-V]

```shell
tuxpkg --version
```

