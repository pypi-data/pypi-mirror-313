# icplot

This project is a utility library used at ICHEC for generating plots and graphics for use in technical documents.

# Installation #

The package is available on PyPI. For a minimal installation you can do:

``` shell
pip install icplot
```

For full functionality, particularly for conversion of image formats `imagemagick` and `cairo` are required. On Mac you can install them with:

``` shell
brew install imagemagick cairo
```

# Features #

The project has support for:

* Coverting image formats between pdf, svg and png
* Building pdf output from tex files, including tikz.

There is a command line interface included, mainly for testing, which may be heplful in getting to know available features.

To covert between image formats you can do:

``` shell
icplot convert --source my_image.svg --target my_image.png
```

To render a Tex tikz image as pdf and png you can do:

``` shell
icplot convert --source my_tikz.tex
```

# Copyright #

Copyright 2024 Irish Centre for High End Computing

The software in this repository can be used under the conditions of the GPLv3+ license, which is available for reading in the accompanying LICENSE file.

