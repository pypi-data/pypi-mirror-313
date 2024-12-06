
// TODO: Go through and see where const can be specified and where pass by reference should be used.


#include "Transformation.h"
#include "simplex.h"
#include "SCE.h"
#include <iostream>

using BT::Simplex;
using namespace std;
using SCE::sceSearch;

Transformation::Transformation() {}
Transformation::~Transformation() {}


double Transformation::rescaleOne(double value)
{

    return rescaleOne(value, m_scale, m_shift);


}



double Transformation::rescaleOne(double value, double scale, double shift)
{

    return (value + shift) * scale;

}


vector<double> Transformation::rescaleMany(vector<double> values)
{

    vector<double> rescaledValues(values.size());

    for(vector<int>::size_type i = 0; i != values.size(); i++) {
        rescaledValues[i] = rescaleOne(values[i]);
    }

    return rescaledValues;

}

vector<double> Transformation::invRescaleMany(vector<double> values)
{

    vector<double> rescaledValues(values.size());

    for(vector<int>::size_type i = 0; i != values.size(); i++) {
        rescaledValues[i] = invRescaleOne(values[i]);
    }

    return rescaledValues;

}



double Transformation::invRescaleOne(double value)
{

    return invRescaleOne(value, m_scale, m_shift);

}



double Transformation::invRescaleOne(double value, double scale, double shift)
{

    return (value / scale) - shift;

}



vector<double> Transformation::transformMany(vector<double> values)
{

    vector<double> transValues(values.size());

    for(vector<int>::size_type i = 0; i != values.size(); i++) {
        transValues[i] = transformOne(values[i]);
    }

    return transValues;

}



vector<double> Transformation::invTransformMany(vector<double> values)
{

    vector<double> transValues(values.size());

    for(vector<int>::size_type i = 0; i != values.size(); i++) {
        transValues[i] = invTransformOne(values[i]);
    }

    return transValues;

}



vector<double> Transformation::optimParams(vector<double> data, double leftCensThresh, bool doRescale, bool isMap)
{

    vector<double> rescaledData;
    if (doRescale) {
        rescaledData = rescaleMany(data);
        leftCensThresh = rescaleOne(leftCensThresh);
    } else {

        rescaledData = data;
    }

    auto optimFunc = std::bind( &Transformation::negLogPosterior, this, placeholders::_1, rescaledData, leftCensThresh, isMap);

    tuple < vector<double>, int > simplexResult =  Simplex(optimFunc, getStartValues());

    vector<double> simplexParams = get<0>(simplexResult);
    int iterations = get<1>(simplexResult);

    return simplexParams;

}

vector<double> Transformation::optimParamsSCE(vector<double> data, double leftCensThresh, bool doRescale, bool isMap)
{

	vector<double> rescaledData;
	if (doRescale) {
		rescaledData = rescaleMany(data);
		leftCensThresh = rescaleOne(leftCensThresh);
	}
	else {

		rescaledData = data;
	}

	auto optimFunc = std::bind(&Transformation::LogPosterior, this, placeholders::_1, rescaledData, leftCensThresh, isMap);
	tuple < vector<double>, int > simplexResult = sceSearch(optimFunc, getMinValues(), getMaxValues());
	vector<double> simplexParams = get<0>(simplexResult);
	int iterations = get<1>(simplexResult);

	return simplexParams;

}



double Transformation::logDensity(vector<double>& params, double value, double leftCensThresh, bool doRescale)
{

    vector<double> convertedParams = convertParams(params);


    if (doRescale) {
        value = rescaleOne(value);
        leftCensThresh = rescaleOne(leftCensThresh);
    }

    double transValue = transformOne(value);
    double transLeftCensThresh = transformOne(leftCensThresh);
    double logDens = logDensityTransformed(convertedParams, transValue, value, transLeftCensThresh);
    return logDens;
}



double Transformation::logJacobian(vector<double>& params, double value, double leftCensThresh, bool doRescale)
{

    vector<double> convertedParams = convertParams(params);


    if (doRescale) {
        value = rescaleOne(value);
        leftCensThresh = rescaleOne(leftCensThresh);
    }

    double transValue = transformOne(value);
    double transLeftCensThresh = transformOne(leftCensThresh);
    double logJac = logJacobianTransformed(convertedParams, transValue, value, transLeftCensThresh);


    return logJac;
}



double Transformation::negLogPosterior(vector<double>& params, vector<double>& data, double leftCensThresh, bool isMap)
{


    vector<double> convertedParams = convertParams(params);
    vector<double> transData = transformMany(data);


    double logPost = 0.0;
    double transLeftCensThresh = transformOne(leftCensThresh);

    for(vector<int>::size_type i = 0; i != transData.size(); i++) {

        logPost += logDensityTransformed(convertedParams, transData[i], data[i], transLeftCensThresh);

    }

    if (isMap) {
        logPost += priorDensity();
    }

    return -logPost;
}

double Transformation::LogPosterior(vector<double>& params, vector<double>& data, double leftCensThresh, bool isMap)
{
	return -negLogPosterior(params, data, leftCensThresh, isMap);
}

double Transformation::stdNormCdf(double x)
{
    // constants
    double a1 =  0.254829592;
    double a2 = -0.284496736;
    double a3 =  1.421413741;
    double a4 = -1.453152027;
    double a5 =  1.061405429;
    double p  =  0.3275911;

    // Save the sign of x
    int sign = 1;
    if (x < 0)
        sign = -1;
    x = fabs(x)/sqrt(2.0);

    // A&S formula 7.1.26
    double t = 1.0/(1.0 + p*x);
    double y = 1.0 - (((((a5*t + a4)*t) + a3)*t + a2)*t + a1)*t*exp(-x*x);

    return 0.5*(1.0 + sign*y);
}



double Transformation::normLogPdf(double x, double m, double s)
{
 	double log_pdf = -0.5 * log(2.0 * boost::math::constants::pi<double>() * s * s)
		- (x - m) * (x - m) / (2.0 * s * s);
	return log_pdf;
}