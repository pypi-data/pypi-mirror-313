\docType{class}
\name{transr::RBoxCox}
\alias{RBoxCox}
\alias{BoxCox}
\title{BoxCox Transformation Class
}
\description{
\describe{
\item{Class representing the BoxCox data transformation and BoxCox transformed censored normal distribution. This distribution is useful to normalise rainfall and streamflow data. The BoxCox transformation is given by:\cr\cr}{}

\item{If \eqn{\lambda\ne0}{\lambda} is not equal to 0:
\deqn{y=\frac{(x+\epsilon)^\lambda - 1}{\lambda}}{y=((x+\epsilon)^\lambda - 1)/\lambda} }{}

\item{If \eqn{\lambda=0}{\lambda=0}:
\deqn{y=\log(x+\epsilon)}{y=log(x+\epsilon)}}{}

\item{Experience suggests that the data \eqn{x} are best rescaled prior to fitting the transformation so that consistent parameter bounds can be use for different datasets. The suggested scaling factor is \eqn{5/max(X)} where \eqn{X=x_1,x_2,...,x_n}\cr\cr}{}

\item{The transformation is fitted by finding the maximimum likelihood or maximum a posteriori solution to BoxCox transformed normal distribution. To handle zero values, left censoring is used, which assumes that values of \eqn{X} that are less than or equal to the threshold have unknown exact values.\cr\cr}{}

\item{If a maximum a posteriori solution is used to fit the BoxCox transformed normal distribution, a normal prior is placed on the transformation parameter \eqn{(\lambda)} with a mean 1.0 and standard deviation of 0.4.\cr\cr}{}

\item{Functions available to apply forward and inverse of transformation, and fit transformation to data.}{}
}
}
\section{Methods}{

\describe{
\item{\code{$new(log_epsilon0,lambda0,scale_parameter)}}{Transformation constructor with initial values of \eqn{\epsilon} and \eqn{\lambda}, and the scaling applied to the data}}

\describe{
\item{\code{$optim_params_sce(data,censor_threshold,apply_scaling,use_MAP))}}{Obtains the transformation parameters to data using the Shuffled Complex Evolution optimization algorithm (Duan). SCE algorithm is slower but consistently obtains the correct parameter estimates. Recommended that apply_scaling=TRUE and use_MAP= TRUE}}

\describe{
\item{\code{$optim_params(data,censor_threshold,apply_scaling,use_MAP))}}{Obtains the transformation parameters to data using the Nelder-Mead Simplex optimization algorithm. Simplex is fast, but doesn't necessarily find the optimal parameter estimates. Recommended that apply_scaling=TRUE and use_MAP= TRUE }}

\describe{
\item{\code{$rescale_one(data_value)}}{Rescales a single data value using scaling factor provided in constructor}}

\describe{
\item{\code{$rescale_many(data)}}{Rescales a vector of data using scaling factor provided in constructor}}

\describe{
\item{\code{$inv_rescale_one(data_value)}}{Applies inverse scaling to a single data value using scaling factor provided in constructor}}

\describe{
\item{\code{$inv_rescale_many(data)}}{Applies inverse scaling to a vector of data using scaling factor provided in constructor}}

\describe{
\item{\code{$transform_one(data_value,log_epsilon,lambda)}}{Applies logsinh transformation to a single data value using either provided values of log_epsilon and lambda, or if log_epsilon=NA and lambda=NA then the (optimal) parameter values held in the class are used}}

\describe{
\item{\code{$transform_many(data)}}{Applies logsinh transformation to a data_vector using the (optimal) parameter values held in the class are used }}

\describe{
\item{\code{$inv_transform_one(data_value,log_epsilon,lambda)}}{Applies the inverse of the logsinh transformation to a single data value using either provided values of log_epsilon and lambda, or if log_epsilon=NA and lambda=NA then the (optimal) parameter values held in the class are used }}

\describe{
\item{\code{$inv_transform_many(data)}}{Applies inverse of the logsinh transformation to a data_vector using the (optimal) parameter values held in the class are used }}

\describe{
\item{\code{$get_trans_params()}}{Returns vector of transformation parameters \{log_epsilon, lambda, mu/sigma, log_sigma \} where mu is the mean and sigma the variance of the transformed data}}

\describe{
\item{\code{$convert_params(parameter_vector)}}{Converts transformation parameter_vector \{log_epsilon, lambda, mu/sigma, log_sigma \} to \{epsilon, lambda, mu, sigma \}}}

\describe{
\item{\code{$neg_log_posterior(parameter_vector), data, censor_threshold, use_MAP}}{Computes the log of the posterior density function for the provided set of parameters \{epsilon, lambda, mu, sigma \}, data vector, censor threshold, and solution method maximum likelihood (use_MAP=FALSE) or maximum a posterior (use_MAP=TRUE) }

\describe{
\item{\code{$log_density(parameter_vector), data_value, censor_threshold, use_MAP}}{Computes the log of the normal density function for the provided set of parameters \{epsilon, lambda, mu, sigma \}, data value, censor threshold, and solution method maximum likelihood (use_MAP=FALSE) or maximum a posterior (use_MAP=TRUE), in the transformed space }}

\describe{
\item{\code{$log_jacobian(parameter_vector), data_value, censor_threshold, use_MAP}}{Computes the log of the transformation jacobian for the provided set of parameters \{epsilon, lambda, mu, sigma \}, data value, censor threshold, and solution method maximum likelihood (use_MAP=FALSE) or maximum a posterior (use_MAP=TRUE) }}
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
\item{Box, G. E. P. and Cox, D. R. (1964) An analysis oftransformations. \emph{Journal Royal Statistical Society: Series B} \bold{26} 211--246. https://doi.org/10.1111/j.2517-6161.1964.tb00553.x}{}

}
}

\examples{
trans_obs = cvobs[which(!is.na(cvobs[,j])),j]        
scalex <- 5/max(trans_obs,na.rm=TRUE)         
trans <- transr::RLogSinh$new(1,1,scalex)     

}
\keyword{data transformation, BoxCox, Box-Cox, streamflow, rainfall}
