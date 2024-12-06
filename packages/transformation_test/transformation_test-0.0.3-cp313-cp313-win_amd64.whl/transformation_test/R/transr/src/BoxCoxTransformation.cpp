
#include "Transformation.h"

using namespace std;


BoxCoxTransformation::BoxCoxTransformation()
{
    m_transLambda = 1.0;
    m_transEpsilon = 0.0;
    m_scale = 1.0;
    m_shift = 0.0;
}



BoxCoxTransformation::BoxCoxTransformation(double transLambda, double transEpsilon)
{
    m_transLambda = transLambda;
    m_transEpsilon = transEpsilon;
    m_scale = 1.0;
    m_shift = 0.0;
}



BoxCoxTransformation::BoxCoxTransformation(double transLambda, double transEpsilon, double scale)
{
    m_transLambda = transLambda;
    m_transEpsilon = transEpsilon;
    m_scale = scale;
    m_shift = 0.0;
}



double BoxCoxTransformation::transformOne(double value)
{
	return transformOne(value, m_transLambda, m_transEpsilon);
}



double BoxCoxTransformation::transformOne(double value, double transLambda, double transEpsilon)
{

	double transValue;

	if (abs(transLambda) > 0.0000001)
	{
		transValue = (pow((value + transEpsilon), transLambda) - 1) / transLambda;
	}
	else
	{
		transValue = log(value + transEpsilon);
	}

	return transValue;
}



double BoxCoxTransformation::invTransformOne(double value)
{
	return invTransformOne(value, m_transLambda, m_transEpsilon);
}



double BoxCoxTransformation::invTransformOne(double value, double transLambda, double transEpsilon)
{

	double transValue;

	if (abs(transLambda) > 0.0000001)
	{
		transValue = pow(transLambda * value + 1, 1 / transLambda) - transEpsilon;
		if ( (transLambda * value + 1) <= 0 &&  isnan(transValue))
		{
			transValue = -transEpsilon;
		}
	}
	else
	{
		transValue = exp(value) - transEpsilon;
	}

	return transValue;
}


double BoxCoxTransformation::logDensityTransformed(vector<double>& params, double transData, double data, double leftCensThresh)
{

    double mean = params[2];
    double stdDev = params[3];
    double transLambda = params[0];
    double transEpsilon = params[1];

    double logDens;

    if (transEpsilon < exp(-25.0) || transEpsilon > exp(1.0) ) {
        return -1E20;
    }

    if (transData > leftCensThresh) {

        //logDens = log(normPdf(transData, mean, stdDev));
		logDens = normLogPdf(transData, mean, stdDev);
        // Jacobian
		logDens += log(pow(data + transEpsilon, transLambda - 1.0));

    } else {

		logDens = log(stdNormCdf((leftCensThresh - mean) / stdDev));
    }

    return logDens;

}

double BoxCoxTransformation::logJacobianTransformed(vector<double>& params, double transData, double data, double leftCensThresh)
{

    double mean = params[2];
    double stdDev = params[3];
    double transLambda = params[0];
    double transEpsilon = params[1];

    double logJac;

    if (transData > leftCensThresh) {

		logJac = log(pow(data + transEpsilon, transLambda - 1.0));

    } else {

        logJac = 0.0;

    }

    return logJac;

}



vector<double> BoxCoxTransformation::convertParams(vector<double>& params)
{

    double stdDev = exp(params[3]);

    // lambda, epsilon, mean, stdev
    vector<double> newParams = {(params[0]), exp(params[1]), params[2]*stdDev, stdDev};

    // set transformation parameter fields
    m_transLambda = newParams[0];
    m_transEpsilon = newParams[1];

    return newParams;
}



double BoxCoxTransformation::priorDensity() {

    //return log(normPdf(log(m_transLambda), getPriorMean(), getPriorStdDev()));
	return normLogPdf((m_transLambda), getPriorMean(), getPriorStdDev());

}



vector<double> BoxCoxTransformation::getParams() {

    vector<double> params = {m_transLambda, m_transEpsilon, m_scale};

    return params;

}
