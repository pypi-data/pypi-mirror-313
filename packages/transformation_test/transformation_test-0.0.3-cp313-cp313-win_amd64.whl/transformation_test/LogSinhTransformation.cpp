
#include "Transformation.h"

using namespace std;


LogSinhTransformation::LogSinhTransformation()
{
    m_transLambda = 1.0;
    m_transEpsilon = 0.0;
    m_scale = 1.0;
    m_shift = 0.0;
    m_transMean = -9999.;
    m_transStdDev = -9999.;
}



LogSinhTransformation::LogSinhTransformation(double transLambda, double transEpsilon)
{
    m_transLambda = transLambda;
    m_transEpsilon = transEpsilon;
    m_scale = 1.0;
    m_shift = 0.0;
    m_transMean = -9999.;
    m_transStdDev = -9999.;
}



LogSinhTransformation::LogSinhTransformation(double transLambda, double transEpsilon, double scale)
{
    m_transLambda = transLambda;
    m_transEpsilon = transEpsilon;
    m_scale = scale;
    m_shift = 0.0;
    m_transMean = -9999.;
    m_transStdDev = -9999.;
}



double LogSinhTransformation::transformOne(double value)
{
	return transformOne(value, m_transLambda, m_transEpsilon);
}



double LogSinhTransformation::transformOne(double value, double transLambda, double transEpsilon)
{

	return (1.0 / transLambda) * log(sinh(transEpsilon + transLambda * value));
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


double LogSinhTransformation::logDensityTransformed(vector<double>& params, double transData, double data, double leftCensThresh, double rightCensThresh)
{

    double mean = params[2];
    double stdDev = params[3];
    double transLambda = params[0];
    double transEpsilon = params[1];

    double logDens;

    if (transEpsilon < exp(-20.0) || transEpsilon > exp(0.0) ) {
        return -1E20;
    }

    if (transData > leftCensThresh && transData < rightCensThresh) {

        //logDens = log(normPdf(transData, mean, stdDev));
		logDens = normLogPdf(transData, mean, stdDev);
        // Jacobian
        logDens += log( 1.0 / tanh(transEpsilon + (transLambda * data)) );

    } else if (transData <= leftCensThresh) {


        logDens = log(stdNormCdf((leftCensThresh-mean)/stdDev) );

    } else {

        logDens = log(1 - stdNormCdf((rightCensThresh-mean)/stdDev) );
    }

    return logDens;

}

double LogSinhTransformation::logJacobianTransformed(vector<double>& params, double transData, double data, double leftCensThresh, double rightCensThresh)
{

    double mean = params[2];
    double stdDev = params[3];
    double transLambda = params[0];
    double transEpsilon = params[1];

    double logJac;

    if (transData > leftCensThresh && transData < rightCensThresh) {

        logJac = log( 1.0 / tanh(transEpsilon + (transLambda * data)) );

    } else if (transData <= leftCensThresh) {

        logJac = 0.0;

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
    m_transMean = newParams[2];
    m_transStdDev = newParams[3];

    return newParams;
}



double LogSinhTransformation::priorDensity() {

    //return log(normPdf(log(m_transLambda), getPriorMean(), getPriorStdDev()));
	return normLogPdf(log(m_transLambda), getPriorMean(), getPriorStdDev());

}


vector<double> LogSinhTransformation::getScaleShift() {

    vector<double> params = {m_scale, m_shift};

    return params;
}


vector<double> LogSinhTransformation::getTransformationParams () {

    vector<double> params = {m_transLambda, m_transEpsilon};

    return params;
}

vector<double> LogSinhTransformation::getDistributionParams () {

    vector<double> params = {m_transLambda, m_transEpsilon, m_transMean, m_transStdDev};

    return params;

}