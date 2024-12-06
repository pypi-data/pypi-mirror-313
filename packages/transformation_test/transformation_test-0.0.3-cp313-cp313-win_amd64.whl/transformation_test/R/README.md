# Wrappers around Transformations

## Installing from an R repository

If you got given an R repository e.g. with pre-compiled 

```R
ourRepo <- 'C:/transr/software/R_pkgs'
stopifnot(file.exists(ourRepo))
cran_public_repo_url <- 'https://cran.csiro.au'
ourRepoUrl <- paste('file://', ourRepo , sep=ifelse(Sys.info()['sysname']=='Windows', '/', ''))
# 'https://cran.csiro.au' is added as a second repository in case other dependencies need to be installed too.
ourPkgs <- 'transr'
# install.packages may take a minute or two.
install.packages(ourPkgs, repos=c(ourRepoUrl, cran_public_repo_url))
```

## Installing the package

```r
setwd('c:/path/to/dir')
library(devtools)
install.packages('transr_1.0.zip')
# or
install.packages('transr_1.0.tar.gz')
```

```r
load(transr)
?transr
browseVignettes('transr')
```

## Building/installing the package from source

```r
setwd('c:/src/csiro/stash/transformation/bindings/R')
library(devtools)
devtools::document('transr')
devtools::build('transr')
devtools::build('transr', binary=TRUE)
```

## Developping

Note that over if you change the cpp files you you may need to do from time to time (?)

```r
setwd('c:/src/csiro/stash/transformation/bindings/R')
library(Rcpp)
Rcpp::compileAttributes('transr')
```

A visual studio 2017 solution/project files are included. This is for use of the IDE and not immplying the need for microsoft compilers.


## Building for binary distribution

There may be some nicer ways to do so using `devtools`, but for now:

```bat
set SOFTW_DIR=c:\build\transr
set R_REPO_DIR=%SOFTW_DIR%\R_pkgs
if not exist %R_REPO_DIR% mkdir %R_REPO_DIR%
set R_SRC_DIR=%R_REPO_DIR%\src\contrib
if not exist %R_SRC_DIR% mkdir %R_SRC_DIR%
set R_SRC_DIR_UNIX=%R_SRC_DIR:\=/%

cd %R_SRC_DIR%
del /Q *.tar.gz
:: had trouble with rtools cp. Odd.

set COPYOPTIONS=/Y /R /D

:: xcopy C:\src\csiro\stash\transformation\bindings\R\transr_*.tar.gz  %COPYOPTIONS%
xcopy C:\tmp\transr_*.tar.gz  %COPYOPTIONS%

set R_PROG_DIR=c:\Program Files\R

REM below may not matter for this package. No harm though.
set PATH=C:\cmd_bin;%PATH%
```

```bat
:: 
set CMD_W_WINBIN_REPO="repo_winbin_dir <- Sys.getenv('R_WINBIN_REPO_DIR_UNIX') ; tools::write_PACKAGES(dir=repo_winbin_dir, type = 'win.binary')"

set R_SRC_DIR_UNIX=%R_SRC_DIR:\=/%
set CMD_W_SRC_REPO="repo_dir <- Sys.getenv('R_SRC_DIR_UNIX') ; tools::write_PACKAGES(dir=repo_dir, type = 'source')"


```

```bat
:: ############# Build binary packages for R 3.6 ##############
set R_EXE="%R_PROG_DIR%\R-3.6.1\bin\x64\R.exe"
if not exist %R_EXE% echo ERROR: R.exe not found at location %R_EXE%
set R_VANILLA=%R_EXE% --no-save --no-restore-data

%R_VANILLA% -e %CMD_W_SRC_REPO%


set R_WINBIN_REPO_DIR=%R_REPO_DIR%\bin\windows\contrib\3.6
set R_BINZIP=%SOFTW_DIR%\R_bin36\
if not exist %R_WINBIN_REPO_DIR% md %R_WINBIN_REPO_DIR%
if not exist %R_BINZIP% md %R_BINZIP%

cd %R_BINZIP%
del /Q *.zip

%R_VANILLA% CMD INSTALL --build %R_SRC_DIR%transr_*.tar.gz
del /Q %R_WINBIN_REPO_DIR%\*.*
xcopy *.zip %R_WINBIN_REPO_DIR%  %COPYOPTIONS%

set R_WINBIN_REPO_DIR_UNIX=%R_WINBIN_REPO_DIR:\=/%
%R_VANILLA% -e %CMD_W_WINBIN_REPO%

:: R 3.5

set R_EXE="%R_PROG_DIR%\R-3.5.3\bin\x64\R.exe"
if not exist %R_EXE% echo ERROR: R.exe not found at this location
set R_VANILLA=%R_EXE% --no-save --no-restore-data
set R_WINBIN_REPO_DIR=%R_REPO_DIR%\bin\windows\contrib\3.5
set R_BINZIP=%SOFTW_DIR%\R_bin35\
if not exist %R_WINBIN_REPO_DIR% md %R_WINBIN_REPO_DIR%
if not exist %R_BINZIP% md %R_BINZIP%

cd %R_BINZIP%
del /Q *.zip

set R_WINBIN_REPO_DIR_UNIX=%R_WINBIN_REPO_DIR:\=/%
%R_VANILLA% CMD INSTALL --build %R_SRC_DIR%transr_*.tar.gz
del /Q %R_WINBIN_REPO_DIR%\*.*
xcopy *.zip %R_WINBIN_REPO_DIR%  %COPYOPTIONS%

set R_WINBIN_REPO_DIR_UNIX=%R_WINBIN_REPO_DIR:\=/%
%R_VANILLA% -e %CMD_W_WINBIN_REPO%

```

