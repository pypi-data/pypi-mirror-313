#define CATCH_CONFIG_MAIN  // This tells Catch to provide a main() - only do this in one cpp file

#include <vector>
#include "catch/catch.hpp"

#define USING_TRANS_R_CORE

#include "../transr/src/Transformation.h"

TEST_CASE("Test the private API to specify the configuration of the ECM in the catchment", "[Error Correction Model]")
{

	std::vector<double> x = { 0, 0, 0, 0, 2.0, 10, 5, 3, 2, 1, .5, .1, 0 };
	double transLambda = 1;
	double transEpsilon = 1;
	double scale = 5/10.0;
	LogSinhTransformation tr(transLambda, transEpsilon, scale);

	double leftCensThresh = 0.0;
	bool doRescale = true;
	bool isMap = true;
	std::vector<double> params = tr.optimParams(x, leftCensThresh, doRescale, isMap);

	// Poorly documented, but params has (seem to be):
	// lambda, epsilon, normalised_mean, log_stdev
	auto x_scaled = tr.rescaleMany(x);
	double log_like = tr.negLogPosterior(params, x_scaled, leftCensThresh, isMap);
}


