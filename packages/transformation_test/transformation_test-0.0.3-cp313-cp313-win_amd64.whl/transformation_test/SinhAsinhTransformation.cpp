
#include "Transformation.h"

using namespace std;


SinhAsinhTransformation::SinhAsinhTransformation()
{
    m_transDelta = 0.0;
    m_transEpsilon = 1.0;
    m_scale = 1.0;
    m_shift = 0.0;
    m_transMean = -9999.;
    m_transStdDev = -9999.;
}



SinhAsinhTransformation::SinhAsinhTransformation(double transDelta, double transEpsilon)
{
    m_transDelta = transDelta;
    m_transEpsilon = transEpsilon;
    m_scale = 1.0;
    m_shift = 0.0;
    m_transMean = -9999.;
    m_transStdDev = -9999.;
}



SinhAsinhTransformation::SinhAsinhTransformation(double transDelta, double transEpsilon, double scale, double shift)
{
    m_transDelta = transDelta;
    m_transEpsilon = transEpsilon;
    m_scale = scale;
    m_shift = shift;
    m_transMean = -9999.;
    m_transStdDev = -9999.;
}


double SinhAsinhTransformation::transformOne(double value)
{
	return transformOne(value, m_transDelta, m_transEpsilon);
}



double SinhAsinhTransformation::transformOne(double value, double transDelta, double transEpsilon)
{

	return sinh(transDelta * asinh(value) + transEpsilon);
}



double SinhAsinhTransformation::invTransformOne(double value)
{
	return invTransformOne(value, m_transDelta, m_transEpsilon);
}



double SinhAsinhTransformation::invTransformOne(double value, double transDelta, double transEpsilon)
{

	double transValue = sinh((asinh(value) - transEpsilon) / transDelta);

	return transValue;
}


double SinhAsinhTransformation::logDensityTransformed(vector<double>& params, double transData, double data, double leftCensThresh, double rightCensThresh)
{

    double mean = params[2];
    double stdDev = params[3];
    double transDelta = params[0];
    double transEpsilon = params[1];

    double logDens;

    if (transData > leftCensThresh && transData < rightCensThresh) {

		logDens = normLogPdf(transData, mean, stdDev);
        // Jacobian
        logDens += log(transDelta * cosh(transDelta * asinh(data) + transEpsilon) / sqrt(pow(data,2) + 1));

    } else if (transData <= leftCensThresh) {

        logDens = log(stdNormCdf((leftCensThresh-mean)/stdDev) );

    } else {

        logDens = log(1 - stdNormCdf((rightCensThresh-mean)/stdDev) );

    }

    return logDens;

}

double SinhAsinhTransformation::logJacobianTransformed(vector<double>& params, double transData, double data, double leftCensThresh, double rightCensThresh)
{

    double mean = params[2];
    double stdDev = params[3];
    double transDelta = params[0];
    double transEpsilon = params[1];

    double logJac;

    if (transData > leftCensThresh && transData < rightCensThresh) {

        logJac = log( transDelta * cosh(transDelta * asinh(data) + transEpsilon) * 1/sqrt(pow(data,2) + 1));

    } else if (transData <= leftCensThresh) {

        logJac = 0.0;

    } else {

        logJac = 0.0;

    }

    return logJac;

}



vector<double> SinhAsinhTransformation::convertParams(vector<double>& params)
{

    // Delta, epsilon, mean, stdev

    double delta = params[0] / (1 - params[0]);
    vector<double> newParams = {delta,
                                params[1] / sqrt(1 - pow(params[1],2)),
                                params[2] / sqrt(1 - pow(params[2],2)),
                                delta * params[3] / (1 - params[3])};

    // set transformation parameter fields
    m_transDelta = newParams[0];
    m_transEpsilon = newParams[1];
    m_transMean = newParams[2];
    m_transStdDev = newParams[3];

    return newParams;
}



double SinhAsinhTransformation::priorDensity() {

    double reparam_delta = m_transDelta / (1 + m_transDelta);
    double reparam_epsilon = m_transEpsilon / sqrt(1 + m_transEpsilon*m_transEpsilon);

    return (normLogPdf(reparam_delta, getPriorMean(), getPriorStdDev()) + normLogPdf(reparam_epsilon, 0.0,1.0));

}


vector<double> SinhAsinhTransformation::getScaleShift() {

    vector<double> params = {m_scale, m_shift};

    return params;
}


vector<double> SinhAsinhTransformation::getTransformationParams () {

    vector<double> params = {m_transDelta, m_transEpsilon};

    return params;
}

vector<double> SinhAsinhTransformation::getDistributionParams () {

    vector<double> params = {m_transDelta, m_transEpsilon, m_transMean, m_transStdDev};

    return params;

}