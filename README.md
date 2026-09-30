<div align="center">
    <h1 align="center">cs.translators.elia</h1>
</div>
<div align="center">

[![PyPI](https://img.shields.io/pypi/v/cs.translators.elia)](https://pypi.org/project/cs.translators.elia/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/cs.translators.elia)](https://pypi.org/project/cs.translators.elia/)
[![PyPI - Wheel](https://img.shields.io/pypi/wheel/cs.translators.elia)](https://pypi.org/project/cs.translators.elia/)
[![PyPI - License](https://img.shields.io/pypi/l/cs.translators.elia)](https://pypi.org/project/cs.translators.elia/)
[![PyPI - Status](https://img.shields.io/pypi/status/cs.translators.elia)](https://pypi.org/project/cs.translators.elia/)


[![PyPI - Plone Versions](https://img.shields.io/pypi/frameworkversions/plone/cs.translators.elia)](https://pypi.org/project/cs.translators.elia/)

[![CI](https://github.com/codesyntax/cs.translators.elia/actions/workflows/main.yml/badge.svg)](https://github.com/codesyntax/cs.translators.elia/actions/workflows/main.yml)
![Code Style](https://img.shields.io/badge/Code%20Style-Black-000000)

[![GitHub contributors](https://img.shields.io/github/contributors/codesyntax/cs.translators.elia)](https://github.com/codesyntax/cs.translators.elia)
[![GitHub Repo stars](https://img.shields.io/github/stars/codesyntax/cs.translators.elia?style=social)](https://github.com/codesyntax/cs.translators.elia)

</div>

This package extends [plone.app.multilingual](https://github.com/plone/plone.app.multilingual) with pluggable external translation utilities for automatic content translation in Plone.

It integrates the [ELIA Translator](https://elia.eus/traductor) a product by [Elhuyar](https://www.elhuyar.eus/eu)

This add-on requires [plone.app.multilingual PR #468](https://github.com/plone/plone.app.multilingual/pull/468).
No released version of `plone.app.multilingual` provides the `IExternalTranslationService` interface yet.


## Installation

Install cs.translators.elia with `pip`:

```shell
pip install cs.translators.elia
```

And to create the Plone site:

```shell
make create-site
```

## Contribute

- [Issue tracker](https://github.com/codesyntax/cs.translators.elia/issues)
- [Source code](https://github.com/codesyntax/cs.translators.elia/)

### Prerequisites ✅

-   An [operating system](https://6.docs.plone.org/install/create-project-cookieplone.html#prerequisites-for-installation) that runs all the requirements mentioned.
-   [uv](https://6.docs.plone.org/install/create-project-cookieplone.html#uv)
-   [Make](https://6.docs.plone.org/install/create-project-cookieplone.html#make)
-   [Git](https://6.docs.plone.org/install/create-project-cookieplone.html#git)
-   [Docker](https://docs.docker.com/get-started/get-docker/) (optional)

### Installation 🔧

1.  Clone this repository, then change your working directory.

    ```shell
    git clone git@github.com:codesyntax/cs.translators.elia.git
    cd cs.translators.elia
    ```

2.  Install this code base.

    ```shell
    make install
    ```


### Add features using `plonecli` or `bobtemplates.plone`

This package provides markers as strings (`<!-- extra stuff goes here -->`) that are compatible with [`plonecli`](https://github.com/plone/plonecli) and [`bobtemplates.plone`](https://github.com/plone/bobtemplates.plone).
These markers act as hooks to add all kinds of subtemplates, including behaviors, control panels, upgrade steps, or other subtemplates from `plonecli`.

To run `plonecli` with configuration to target this package, run the following command.

```shell
make add <template_name>
```

For example, you can add a content type to your package with the following command.

```shell
make add content_type
```

You can add a behavior with the following command.

```shell
make add behavior
```

```{seealso}
You can check the list of available subtemplates in the [`bobtemplates.plone` `README.md` file](https://github.com/plone/bobtemplates.plone/?tab=readme-ov-file#provided-subtemplates).
See also the documentation of [Mockup and Patternslib](https://6.docs.plone.org/classic-ui/mockup.html) for how to build the UI toolkit for Classic UI.
```

## License

The project is licensed under GPLv2.

## Credits and acknowledgements 🙏

Generated using [Cookieplone (2.0.0)](https://github.com/plone/cookieplone) and [cookieplone-templates (fa8eca4)](https://github.com/plone/cookieplone-templates/commit/fa8eca4f3ea456538542b6b07f9bceaa05127fd2) on 2026-09-30 16:04:32.322924. A special thanks to all contributors and supporters!
