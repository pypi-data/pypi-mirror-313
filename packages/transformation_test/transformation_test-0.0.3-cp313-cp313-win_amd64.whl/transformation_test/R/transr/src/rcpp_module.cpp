// -*- mode: C++; c-indent-level: 4; c-basic-offset: 4; indent-tabs-mode: nil; -*-
//
// rcpp_module.cpp: Rcpp R/C++ interface class library -- Rcpp Module examples
//
// Copyright (C) 2010 - 2012  Dirk Eddelbuettel and Romain Francois
//
// This file is part of Rcpp.
//
// Rcpp is free software: you can redistribute it and/or modify it
// under the terms of the GNU General Public License as published by
// the Free Software Foundation, either version 2 of the License, or
// (at your option) any later version.
//
// Rcpp is distributed in the hope that it will be useful, but
// WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU General Public License for more details.
//
// You should have received a copy of the GNU General Public License
// along with Rcpp.  If not, see <http://www.gnu.org/licenses/>.

#include <Rcpp.h>
#include "Transformation.h"

double na = Rcpp::NumericVector::get_na();

// translated from PyLogSinh. May be largely superfluous in R
class RLogSinh
{
public:
	LogSinhTransformation logsinh_trans;
	std::vector<double> trans_params;

    RLogSinh(double trans_lambda=1.0, double trans_epsilon=0.01, double scale=1.0):
		logsinh_trans(trans_lambda, trans_epsilon, scale)
	{
	}

	double transform_one(double value, double trans_lambda = na, double trans_epsilon = na)
	{
		if (Rcpp::NumericVector::is_na(trans_lambda))
			return this->logsinh_trans.transformOne(value);
		else
			return this->logsinh_trans.transformOne(value, trans_lambda, trans_epsilon);
	}

	std::vector<double> transform_many(std::vector<double> values)
	{
		return this->logsinh_trans.transformMany(values);
	}

	std::vector<double> inv_transform_many(std::vector<double>& values)
	{
		return this->logsinh_trans.invTransformMany(values);
	}

    double rescale_one(double value)
	{
		return this->logsinh_trans.rescaleOne(value);
	}

	double inv_rescale_one(double value)
	{
		return this->logsinh_trans.invRescaleOne(value);
	}

	std::vector<double> rescale_many(std::vector<double>& values)
	{
		return this->logsinh_trans.rescaleMany(values);
	}

	std::vector<double> inv_rescale_many(std::vector<double>& values)
	{
		return this->logsinh_trans.invRescaleMany(values);
	}

	std::vector<double> optim_params(std::vector<double>& data, double left_cens_thresh, bool do_rescale, bool is_map)
	{
		auto trans_vec = this->logsinh_trans.optimParams(data, left_cens_thresh, do_rescale, is_map);
		this->trans_params = trans_vec;
		return this->trans_params;
	}

	std::vector<double> optim_params_sce(std::vector<double>& data, double left_cens_thresh, bool do_rescale, bool is_map)
	{
		auto trans_vec = this->logsinh_trans.optimParamsSCE(data, left_cens_thresh, do_rescale, is_map);
		this->trans_params = trans_vec;
		return this->trans_params;
	}

	std::vector<double> get_trans_params()
	{
		return this->trans_params;
	}

	std::vector<double> get_params()
	{
		return this->logsinh_trans.getParams();
	}

	double log_density(std::vector<double>& params, double value, double leftCensThresh, bool do_rescale)
	{
		return this->logsinh_trans.logDensity(params, value, leftCensThresh, do_rescale);
	}

	double log_jacobian(std::vector<double>& params, double value, double leftCensThresh, bool do_rescale)
	{
		return this->logsinh_trans.logJacobian(params, value, leftCensThresh, do_rescale);
	}

    //def __str__(self):
    //    return "RLogSinh"

	double neg_log_posterior(vector<double>& params, vector<double>& data, double leftCensThresh, bool is_map)
	{
		return this->logsinh_trans.negLogPosterior(params, data, leftCensThresh, is_map);
	}

	vector<double> convert_params(vector<double>& params)
	{
		return this->logsinh_trans.convertParams(params);
	}

};

class RYeoJohnson
{
public:
	YeoJohnsonTransformation yeojohnson_trans;
	std::vector<double> trans_params;

	RYeoJohnson(double trans_lambda = 1.0, double scale = 1.0, double shift = 0.01) :
		yeojohnson_trans(trans_lambda, scale, shift)
	{
	}

	double transform_one(double value, double trans_lambda = na)
	{
		if (Rcpp::NumericVector::is_na(trans_lambda))
			return this->yeojohnson_trans.transformOne(value);
		else
			return this->yeojohnson_trans.transformOne(value, trans_lambda);
	}

	std::vector<double> transform_many(std::vector<double> values)
	{
		return this->yeojohnson_trans.transformMany(values);
	}

	std::vector<double> inv_transform_many(std::vector<double>& values)
	{
		return this->yeojohnson_trans.invTransformMany(values);
	}

	double rescale_one(double value)
	{
		return this->yeojohnson_trans.rescaleOne(value);
	}

	double inv_rescale_one(double value)
	{
		return this->yeojohnson_trans.invRescaleOne(value);
	}

	std::vector<double> rescale_many(std::vector<double>& values)
	{
		return this->yeojohnson_trans.rescaleMany(values);
	}

	std::vector<double> inv_rescale_many(std::vector<double>& values)
	{
		return this->yeojohnson_trans.invRescaleMany(values);
	}

	std::vector<double> optim_params(std::vector<double>& data, double left_cens_thresh, bool do_rescale, bool is_map)
	{
		auto trans_vec = this->yeojohnson_trans.optimParams(data, left_cens_thresh, do_rescale, is_map);
		this->trans_params = trans_vec;
		return this->trans_params;
	}

	std::vector<double> optim_params_sce(std::vector<double>& data, double left_cens_thresh, bool do_rescale, bool is_map)
	{
		auto trans_vec = this->yeojohnson_trans.optimParamsSCE(data, left_cens_thresh, do_rescale, is_map);
		this->trans_params = trans_vec;
		return this->trans_params;
	}

	std::vector<double> get_trans_params()
	{
		return this->trans_params;
	}

	std::vector<double> get_params()
	{
		return this->yeojohnson_trans.getParams();
	}

	double log_density(std::vector<double>& params, double value, double leftCensThresh, bool do_rescale)
	{
		return this->yeojohnson_trans.logDensity(params, value, leftCensThresh, do_rescale);
	}

	double log_jacobian(std::vector<double>& params, double value, double leftCensThresh, bool do_rescale)
	{
		return this->yeojohnson_trans.logJacobian(params, value, leftCensThresh, do_rescale);
	}

	double neg_log_posterior(vector<double>& params, vector<double>& data, double leftCensThresh, bool is_map)
	{
		return this->yeojohnson_trans.negLogPosterior(params, data, leftCensThresh, is_map);
	}

	vector<double> convert_params(vector<double>& params)
	{
		return this->yeojohnson_trans.convertParams(params);
	}

	//def __str__(self):
	//    return "RLogSinh"

};


class RBoxCox
{
public:
	BoxCoxTransformation boxcox_trans;
	std::vector<double> trans_params;

	RBoxCox(double trans_lambda = 1.0, double trans_epsilon = 0.01, double scale = 1.0) :
		boxcox_trans(trans_lambda, trans_epsilon, scale)
	{
	}

	double transform_one(double value, double trans_lambda = na, double trans_epsilon = na)
	{
		if (Rcpp::NumericVector::is_na(trans_lambda))
			return this->boxcox_trans.transformOne(value);
		else
			return this->boxcox_trans.transformOne(value, trans_lambda, trans_epsilon);
	}

	std::vector<double> transform_many(std::vector<double> values)
	{
		return this->boxcox_trans.transformMany(values);
	}

	std::vector<double> inv_transform_many(std::vector<double>& values)
	{
		return this->boxcox_trans.invTransformMany(values);
	}

	double rescale_one(double value)
	{
		return this->boxcox_trans.rescaleOne(value);
	}

	double inv_rescale_one(double value)
	{
		return this->boxcox_trans.invRescaleOne(value);
	}

	std::vector<double> rescale_many(std::vector<double>& values)
	{
		return this->boxcox_trans.rescaleMany(values);
	}

	std::vector<double> inv_rescale_many(std::vector<double>& values)
	{
		return this->boxcox_trans.invRescaleMany(values);
	}

	std::vector<double> optim_params(std::vector<double>& data, double left_cens_thresh, bool do_rescale, bool is_map)
	{
		auto trans_vec = this->boxcox_trans.optimParams(data, left_cens_thresh, do_rescale, is_map);
		this->trans_params = trans_vec;
		return this->trans_params;
	}

	std::vector<double> optim_params_sce(std::vector<double>& data, double left_cens_thresh, bool do_rescale, bool is_map)
	{
		auto trans_vec = this->boxcox_trans.optimParamsSCE(data, left_cens_thresh, do_rescale, is_map);
		this->trans_params = trans_vec;
		return this->trans_params;
	}

	std::vector<double> get_trans_params()
	{
		return this->trans_params;
	}

	std::vector<double> get_params()
	{
		return this->boxcox_trans.getParams();
	}

	double log_density(std::vector<double>& params, double value, double leftCensThresh, bool do_rescale)
	{
		return this->boxcox_trans.logDensity(params, value, leftCensThresh, do_rescale);
	}

	double log_jacobian(std::vector<double>& params, double value, double leftCensThresh, bool do_rescale)
	{
		return this->boxcox_trans.logJacobian(params, value, leftCensThresh, do_rescale);
	}

	double neg_log_posterior(vector<double>& params, vector<double>& data, double leftCensThresh, bool is_map)
	{
		return this->boxcox_trans.negLogPosterior(params, data, leftCensThresh, is_map);
	}

	vector<double> convert_params(vector<double>& params)
	{
		return this->boxcox_trans.convertParams(params);
	}

	//def __str__(self):
	//    return "RBoxCox"

};


RCPP_MODULE(transformations) {
	// Take cues from https://github.com/eddelbuettel/rcppbdt/blob/master/src/RcppBDTdt.cpp	
	Rcpp::class_<RLogSinh>("RLogSinh")
		// expose the default constructor
		.constructor<double, double, double >("")
		//RLogSinh(double trans_lambda = 1.0, double trans_epsilon = 0.01, double scale = 1.0) :
		//.constructor()
		//double transform_one(double value, double trans_lambda = na, double trans_epsilon = na)
		.method("transform_one", &RLogSinh::transform_one, "transform_one")
		//std::vector<double> transform_many(std::vector<double> values)
		.method("transform_many", &RLogSinh::transform_many, "transform_many")
		//std::vector<double> inv_transform_many(std::vector<double>& values)
		.method("inv_transform_many", &RLogSinh::inv_transform_many, "inv_transform_many")
		//double rescale_one(double value)
		.method("rescale_one", &RLogSinh::rescale_one, "rescale_one")
		//double inv_rescale_one(double value)
		.method("inv_rescale_one", &RLogSinh::inv_rescale_one, "inv_rescale_one")
		//std::vector<double> rescale_many(std::vector<double>& values)
		.method("rescale_many", &RLogSinh::rescale_many, "rescale_many")
		//std::vector<double> inv_rescale_many(std::vector<double>& values)
		.method("inv_rescale_many", &RLogSinh::inv_rescale_many, "inv_rescale_many")
		//std::vector<double> optim_params(std::vector<double>& data, double left_cens_thresh, bool do_rescale, bool is_map)
		.method("optim_params", &RLogSinh::optim_params, "optim_params")
		//std::vector<double> optim_params(std::vector<double>& data, double left_cens_thresh, bool do_rescale, bool is_map)
		.method("optim_params_sce", &RLogSinh::optim_params_sce, "optim_params_sce")
		//std::vector<double> get_trans_params()
		.method("get_trans_params", &RLogSinh::get_trans_params, "get_trans_params")
		//double log_density(std::vector<double>& params, double value, double leftCensThresh, bool do_rescale)
		.method("log_density", &RLogSinh::log_density, "log_density")
		//double log_jacobian(std::vector<double>& params, double value, double leftCensThresh, bool do_rescale)
		.method("log_jacobian", &RLogSinh::log_jacobian, "log_jacobian")
		//double neg_log_posterior(vector<double>& params, vector<double>& data, double leftCensThresh, bool is_map)
		.method("neg_log_posterior", &RLogSinh::neg_log_posterior, "neg_log_posterior")
		//vector<double> convert_params(vector<double>& params)
		.method("convert_params", &RLogSinh::convert_params, "convert_params")
		//std::vector<double> get_params()
		.property("params", &RLogSinh::get_params, "gets the parameters")
		;

	Rcpp::class_<RYeoJohnson>("RYeoJohnson")
		// expose the default constructor
		.constructor<double, double, double >("")
		//RLogSinh(double trans_lambda = 1.0, double scale = 1.0, double shift = 0.0, ) :
		//.constructor()
		//double transform_one(double value, double trans_lambda = na)
		.method("transform_one", &RYeoJohnson::transform_one, "transform_one")
		//std::vector<double> transform_many(std::vector<double> values)
		.method("transform_many", &RYeoJohnson::transform_many, "transform_many")
		//std::vector<double> inv_transform_many(std::vector<double>& values)
		.method("inv_transform_many", &RYeoJohnson::inv_transform_many, "inv_transform_many")
		//double rescale_one(double value)
		.method("rescale_one", &RYeoJohnson::rescale_one, "rescale_one")
		//double inv_rescale_one(double value)
		.method("inv_rescale_one", &RYeoJohnson::inv_rescale_one, "inv_rescale_one")
		//std::vector<double> rescale_many(std::vector<double>& values)
		.method("rescale_many", &RYeoJohnson::rescale_many, "rescale_many")
		//std::vector<double> inv_rescale_many(std::vector<double>& values)
		.method("inv_rescale_many", &RYeoJohnson::inv_rescale_many, "inv_rescale_many")
		//std::vector<double> optim_params(std::vector<double>& data, double left_cens_thresh, bool do_rescale, bool is_map)
		.method("optim_params", &RYeoJohnson::optim_params, "optim_params")
		//std::vector<double> optim_params_sce(std::vector<double>& data, double left_cens_thresh, bool do_rescale, bool is_map)
		.method("optim_params_sce", &RYeoJohnson::optim_params_sce, "optim_params")
		//std::vector<double> get_trans_params()
		.method("get_trans_params", &RYeoJohnson::get_trans_params, "get_trans_params")
		//std::vector<double> get_params()
		.property("params", &RYeoJohnson::get_params, "gets the parameters")
		//double log_density(std::vector<double>& params, double value, double leftCensThresh, bool do_rescale)
		.method("log_density", &RYeoJohnson::log_density, "log_density")
		//double log_jacobian(std::vector<double>& params, double value, double leftCensThresh, bool do_rescale)
		.method("log_jacobian", &RYeoJohnson::log_jacobian, "log_jacobian")
		//double neg_log_posterior(vector<double>& params, vector<double>& data, double leftCensThresh, bool is_map)
		.method("neg_log_posterior", &RYeoJohnson::neg_log_posterior, "neg_log_posterior")
		//vector<double> convert_params(vector<double>& params)
		.method("convert_params", &RYeoJohnson::convert_params, "convert_params")
		//std::vector<double> get_params()
		.property("params", &RYeoJohnson::get_params, "gets the parameters")
		;

	Rcpp::class_<RBoxCox>("RBoxCox")
		// expose the default constructor
		.constructor<double, double, double >("")
		//RBoxCox(double trans_lambda = 1.0, double trans_epsilon = 0.01, double scale = 1.0) :
		//.constructor()
		//double transform_one(double value, double trans_lambda = na, double trans_epsilon = na)
		.method("transform_one", &RBoxCox::transform_one, "transform_one")
		//std::vector<double> transform_many(std::vector<double> values)
		.method("transform_many", &RBoxCox::transform_many, "transform_many")
		//std::vector<double> inv_transform_many(std::vector<double>& values)
		.method("inv_transform_many", &RBoxCox::inv_transform_many, "inv_transform_many")
		//double rescale_one(double value)
		.method("rescale_one", &RBoxCox::rescale_one, "rescale_one")
		//double inv_rescale_one(double value)
		.method("inv_rescale_one", &RBoxCox::inv_rescale_one, "inv_rescale_one")
		//std::vector<double> rescale_many(std::vector<double>& values)
		.method("rescale_many", &RBoxCox::rescale_many, "rescale_many")
		//std::vector<double> inv_rescale_many(std::vector<double>& values)
		.method("inv_rescale_many", &RBoxCox::inv_rescale_many, "inv_rescale_many")
		//std::vector<double> optim_params(std::vector<double>& data, double left_cens_thresh, bool do_rescale, bool is_map)
		.method("optim_params", &RBoxCox::optim_params, "optim_params")
		//std::vector<double> optim_params_sce(std::vector<double>& data, double left_cens_thresh, bool do_rescale, bool is_map)
		.method("optim_params_sce", &RBoxCox::optim_params_sce, "optim_params")
		//std::vector<double> get_trans_params()
		.method("get_trans_params", &RBoxCox::get_trans_params, "get_trans_params")
		//double log_density(std::vector<double>& params, double value, double leftCensThresh, bool do_rescale)
		.method("log_density", &RBoxCox::log_density, "log_density")
		//double log_jacobian(std::vector<double>& params, double value, double leftCensThresh, bool do_rescale)
		.method("log_jacobian", &RBoxCox::log_jacobian, "log_jacobian")
		//double neg_log_posterior(vector<double>& params, vector<double>& data, double leftCensThresh, bool is_map)
		.method("neg_log_posterior", &RBoxCox::neg_log_posterior, "neg_log_posterior")
		//vector<double> convert_params(vector<double>& params)
		.method("convert_params", &RBoxCox::convert_params, "convert_params")
		//std::vector<double> get_params()
		.property("params", &RBoxCox::get_params, "gets the parameters")
		;

}



