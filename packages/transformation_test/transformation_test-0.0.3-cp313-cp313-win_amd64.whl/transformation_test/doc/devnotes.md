
```
setwd('C:/src/csiro/stash/transformation/bindings/R')
library(Rcpp)
Rcpp.package.skeleton(name = "transr", list = character(), 
	environment = .GlobalEnv, path = ".", force = FALSE, 
	code_files = character(), cpp_files = character(),
	example_code = TRUE, attributes = TRUE, module = TRUE, 
	author = "Jean-Michel Perraud", 
	maintainer = "Jean-Michel Perraud", 
	email = "per202@csiro.au", 
	license = "GPL (>= 2)"
	)
```

I want to have Visual Studio as an IDE (but not with an intend to use Visual CPP for package compilation)

```
copy C:\src\csiro\stash\datatypes\bindings\R\pkgs\uchronia\src\uchronia_r.vcxproj* transr\src\
```

Adapt manually the vcxproj files

I also copy the C and H files from the top level into src in the R package. 

To my surprise, compiles out of the box (surprised even if I have a custim Rcpp set up for interop with VS)

`cp C:\src\csiro\stash\datatypes\bindings\R\pkgs\uchronia\.Rbuildignore transr\`

```
R CMD build transr
R CMD INSTALL transr.blah.tar.gz
```

```
*** arch - i386                                                                                                                                                 
c:/Rtools/mingw_32/bin/g++  -I"C:/PROGRA~1/R/R-33~1.3/include" -DNDEBUG    -I"c:/RLib/Rcpp/include" -I"d:/Compiler/gcc-4.9.3/local330/include"     -O2 -Wall  -mtune=core2 -c LogSinhTransformation.cpp -o LogSinhTransformation.o                                                                                              
In file included from C:/Rtools/mingw_32/i686-w64-mingw32/include/c++/tuple:35:0,                                   from Transformation.h:7,                                                                           from LogSinhTransformation.cpp:2:                                                 C:/Rtools/mingw_32/i686-w64-mingw32/include/c++/bits/c++0x_warning.h:32:2: error: #error This file requires compiler and library support for the ISO C++ 2011 standard. This support is currently experimental, and must be enabled with the -std=c++11 or -std=gnu++11 compiler options.             #error This file requires compiler and library support for the \                                  In file included from LogSinhTransformation.cpp:2:0:                                               Transformation.h:9:46: fatal error: boost/math/constants/constants.hpp: No such file or directory   #include <boost/math/constants/constants.hpp>                                                            
```

First, add a `src/Makevars` to tell Rcpp about c++11 things. Still an issue it seems.

I do have `c:\local\include\boost\math\constants\constants.hpp` though. 

Take cues from [rcppbdt by eddelbuettel](https://github.com/eddelbuettel/rcppbdt/blob/master/src/RcppBDTdt.cpp)

 


```
setwd('C:/src/csiro/stash/transformation/bindings/R')
library(Rcpp)
Rcpp.package.skeleton(name = "rcppskeleton", list = character(), 
	environment = .GlobalEnv, path = ".", force = FALSE, 
	code_files = character(), cpp_files = character(),
	example_code = TRUE, attributes = TRUE, module = TRUE, 
	author = "Jean-Michel Perraud", 
	maintainer = "Jean-Michel Perraud", 
	email = "per202@csiro.au", 
	license = "GPL (>= 2)"
	)
```