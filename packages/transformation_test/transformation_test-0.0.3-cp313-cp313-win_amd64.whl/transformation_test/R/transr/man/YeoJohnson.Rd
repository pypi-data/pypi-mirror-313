\docType{class}
\name{transr::RYeoJohnson}
\alias{RYeoJohnson}
\alias{YeoJohnson}
\title{YeoJohnson Transformation Class
}
\description{
\describe{
\item{Class representing the YeoJohnson data transformation and YeoJohnson transformed censored normal distribution. This distribution is useful to normalise skewed data that take positive and negative values. The YeoJohnson transformation is given by:\cr\cr}{}

\item{If \eqn{y\ge0}{y} is greater than or equal to 0:}{}

\item{}{If \eqn{\lambda\ne0}{\lambda} is not equal to 0:
\deqn{y =\frac{(x+1)^\lambda - 1}{\lambda}}{y=((x+1)^\lambda - 1)/\lambda}}
\item{}{For \eqn{\lambda=0}{\lambda=0},
\deqn{y=\log(x+1)}{y=log(x+1)}}

\item{If \eqn{y\le0}{y} is less than 0:}{}

\item{}{If \eqn{\lambda\ne2}{\lambda} is not equal to 2:
\deqn{y =\frac{(x+1)^(2-\lambda) - 1}{2-\lambda}}{y=((x+1)^(2-\lambda) - 1)/(2-\lambda)}}
\item{}{For \eqn{\lambda=2}{\lambda=2}:
\deqn{y=-\log(x+1)}{y=log(-x+1)}}

\item{Experience suggests that the data \eqn{x} are best standarised prior to fitting the transformation so that consistent parameters bounds can be use for different datasets. The suggested standardisation is \eqn{(x_k-mean(X))/std(X)} where \eqn{X=x_1,x_2,...,x_n}\cr\cr}{}

\item{The transformation is fitted finding the maximimum likelihood or maximum a posteriori solution to YeoJohnson transformed normal distribution. Left censoring can be applied if values of \eqn{X} that are less than or equal to a threshold have unknown exact values.\cr\cr}{}

\item{If a maximum a posteriori solution is used to fit the YeoJohnson transformed normal distribution, a normal prior is placed on the transformation parameter  \eqn{(\lambda)}  with a mean 1.0 and standard deviation of 0.4.\cr\cr}{}

\item{Functions available to apply forward and inverse of transformation, and fit transformation to data.}{}
}
}
\section{Methods}{

\describe{
\item{\code{$new(lambda0,scale_parameter)}}{Transformation constructor with initial value of \eqn{\lambda}, and the scaling applied to the data}}

\describe{
\item{\code{$optim_params_sce(data,censor_threshold,apply_scaling,use_MAP))}}{Obtains the transformation parameters to data using the Shuffled Complex Evolution optimization algorithm (Duan). SCE algorithm is slower but consistently obtains the correct parameter estimates. Recommended that apply_scaling=TRUE and use_MAP= TRUE}}

\describe{
\item{\code{$optim_params(data,censor_threshold,apply_scaling,use_MAP))}}{Obtains  the transformation parameters to data using the Nelder-Mead Simplex optimization algorithm. Simplex is fast, but doesn't necessarily find the optimal parameter estimates. Recommended that apply_scaling=TRUE and use_MAP= TRUE }}

\describe{
\item{\code{$rescale_one(data_value)}}{Rescales a single data value using scaling factor provided in constructor}}

\describe{
\item{\code{$rescale_many(data)}}{Rescales a vector of data using scaling factor provided in constructor}}

\describe{
\item{\code{$inv_rescale_one(data_value)}}{Applies inverse scaling to a single data value using scaling factor provided in constructor}}

\describe{
\item{\code{$inv_rescale_many(data)}}{Applies inverse scaling to a vector of data using scaling factor provided in constructor}}

\describe{
\item{\code{$transform_one(data_value,lambda)}}{Applies YeoJohnson transformation to a single data value using either a provided value of lambda, or if lambda=NA then the (optimal) parameter value held in the class is used}}

\describe{
\item{\code{$transform_many(data)}}{Applies YeoJohnson transformation to a data_vector using the (optimal) parameter value held in the class is used }}

\describe{
\item{\code{$inv_transform_one(data_value,lambda)}}{Applies the inverse of the YeoJohnson transformation to a single data value using either a provided value of lambda, or if lambda=NA then the (optimal) parameter value held in the class are used }}

\describe{
\item{\code{$inv_transform_many(data,lambda)}}{Applies inverse of the YeoJohnson transformation to a data_vector using the (optimal) parameter value held in the class is used }}

\describe{
\item{\code{$get_trans_params()}}{Returns vector of transformation parameters \{lambda, mu/sigma, log_sigma \} where mu is the mean and sigma the variance of the transformed data}}

\describe{
\item{\code{$convert_params(parameter_vector)}}{Converts transformation parameter_vector \{lambda, mu/sigma, log_sigma \} to \{lambda, mu, sigma \}}}

\describe{
\item{\code{$neg_log_posterior(parameter_vector), data, censor_threshold, use_MAP}}{Computes the log of the posterior density function for the provided set of parameters \{lambda, mu, sigma \}, data vector, censor threshold, and solution method maximum likelihood (use_MAP=FALSE) or maximum a posterior (use_MAP=TRUE) }

\describe{
\item{\code{$log_density(parameter_vector), data_value, censor_threshold, use_MAP}}{Computes the log of the normal density function for the provided set of parameters \{lambda, mu, sigma \}, data value, censor threshold, and solution method maximum likelihood (use_MAP=FALSE) or maximum a posterior (use_MAP=TRUE), in the transformed space }}

\describe{
\item{\code{$log_jacobian(parameter_vector), data_value, censor_threshold, use_MAP}}{Computes the log of the transformation jacobian for the provided set of parameters \{lambda, mu, sigma \}, data value, censor threshold, and solution method maximum likelihood (use_MAP=FALSE) or maximum a posterior (use_MAP=TRUE) }}
}
}

\usage{data("trans")}

\details{
%%  ~~ If necessary, more details than the __description__ above ~~
}
\source{
%%  ~~ reference to a publication or URL from which the data were obtained ~~
}

\references{
%%  ~~ possibly secondary sources and usages ~~
\describe{
\item{Duan, Q. Y., V. K. Gupta and S. Sorooshian (1993). Shuffled complex evolution approach for effective and efficient global minimization. Journal of Optimization Theory and Applications 76(3): 501-521. http://dx.doi.org/10.1007/BF00939380.}{}
}

\describe{
\item{Nelder, J. A. and R. Mead (1965). A Simplex Method for Function Minimization. The Computer Journal 7(4): 308-313. http://dx.doi.org/10.1093/comjnl/7.4.308.}{}
}

\describe{
\item{Yeo, I. K. and R. A. Johnson (2000). A new family of power transformations to improve normality or symmetry. Biometrika 87(4): 954-959. http://dx.doi.org/10.1093/biomet/87.4.954.}{}
}
}

\examples{
trans_obs = cvobs[which(!is.na(cvobs[,j])),j]        
scalex <- 5/max(trans_obs,na.rm=TRUE)         
trans <- transr::RYeoJohnson$new(1,1,scalex)     

}
\keyword{data transformation, YeoJohnson}
