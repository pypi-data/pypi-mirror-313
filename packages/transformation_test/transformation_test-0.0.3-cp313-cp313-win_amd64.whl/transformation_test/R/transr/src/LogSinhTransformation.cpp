
#include "Transformation.h"

using namespace std;


LogSinhTransformation::LogSinhTransformation()
{
    m_transLambda = 1.0;
    m_transEpsilon = 0.0;
    m_scale = 1.0;
    m_shift = 0.0;
}



LogSinhTransformation::LogSinhTransformation(double transLambda, double transEpsilon)
{
    m_transLambda = transLambda;
    m_transEpsilon = transEpsilon;
    m_scale = 1.0;
    m_shift = 0.0;
}



LogSinhTransformation::LogSinhTransformation(double transLambda, double transEpsilon, double scale)
{
    m_transLambda = transLambda;
    m_transEpsilon = transEpsilon;
    m_scale = scale;
    m_shift = 0.0;
}



double LogSinhTransformation::transformOne(double value)
{
	return transformOne(value, m_transLambda, m_transEpsilon);
}



double LogSinhTransformation::transformOne(double value, double transLambda, double transEpsilon)
{
	double out;
	if ( (transEpsilon + transLambda * value) > 20.0)
	{
		out =  (transEpsilon + transLambda * value - log(2.0))/transLambda ;
	} else {
		out = (1.0 / transLambda) * log(sinh(transEpsilon + transLambda * value));
	}

	return (out);
}



double LogSinhTransformation::invTransformOne(double value)
{
	return invTransformOne(value, m_transLambda, m_transEpsilon);
}



double LogSinhTransformation::invTransformOne(double value, double transLambda, double transEpsilon)
{

	double transValue = (1.0 / transLambda) * (asinh(exp(transLambda * value)) - transEpsilon);

	return transValue;
}


double LogSinhTransformation::logDensityTransformed(vector<double>& params, double transData, double data, double leftCensThresh)
{

    double mean = params[2];
    double stdDev = params[3];
    double transLambda = params[0];
    double transEpsilon = params[1];

    double logDens;

    if (m_transEpsilon < exp(-20.0) || m_transEpsilon > exp(0.0) ) {
        return -1E20;
    }

    if (transData > leftCensThresh) {

        //logDens = log(normPdf(transData, mean, stdDev));
		logDens = normLogPdf(transData, mean, stdDev);
        // Jacobian
        logDens += log( 1.0 / tanh(transEpsilon + (transLambda * data)) );

    } else {


		logDens = log(stdNormCdf((leftCensThresh - mean) / stdDev));

    }

    return logDens;

}

double LogSinhTransformation::logJacobianTransformed(vector<double>& params, double transData, double data, double leftCensThresh)
{

    double mean = params[2];
    double stdDev = params[3];
    double transLambda = params[0];
    double transEpsilon = params[1];

    double logJac;

    if (transData > leftCensThresh) {

        logJac = log( 1.0 / tanh(transEpsilon + (transLambda * data)) );

    } else {

        logJac = 0.0;

    }

    return logJac;

}



vector<double> LogSinhTransformation::convertParams(vector<double>& params)
{

    double stdDev = exp(params[3]);

    // lambda, epsilon, mean, stdev
    vector<double> newParams = {exp(params[0]), exp(params[1]), params[2]*stdDev, stdDev};

    // set transformation parameter fields
    m_transLambda = newParams[0];
    m_transEpsilon = newParams[1];

    return newParams;
}



double LogSinhTransformation::priorDensity() {

    //return log(normPdf(log(m_transLambda), getPriorMean(), getPriorStdDev()));
	return normLogPdf(log(m_transLambda), getPriorMean(), getPriorStdDev());

}



vector<double> LogSinhTransformation::getParams() {

    vector<double> params = {m_transLambda, m_transEpsilon, m_scale};

    return params;

}
