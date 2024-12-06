

#include "Transformation.h"

using namespace std;


YeoJohnsonTransformation::YeoJohnsonTransformation()
{
    m_transLambda = 1.0;
    m_scale = 1.0;
    m_shift = 0.0;
    m_transMean = -9999.;
    m_transStdDev = -9999.;
}



YeoJohnsonTransformation::YeoJohnsonTransformation(double transLambda)
{
    m_transLambda = transLambda;
    m_scale = 1.0;
    m_shift = 0.0;
    m_transMean = -9999.;
    m_transStdDev = -9999.;
}



YeoJohnsonTransformation::YeoJohnsonTransformation(double transLambda, double scale, double shift)
{
    m_transLambda = transLambda;
    m_scale = scale;
    m_shift = shift;
    m_transMean = -9999.;
    m_transStdDev = -9999.;
}



double YeoJohnsonTransformation::transformOne(double value)
{
    return transformOne(value, m_transLambda);
}



double YeoJohnsonTransformation::invTransformOne(double value)
{
    return invTransformOne(value, m_transLambda);
}



double YeoJohnsonTransformation::transformOne(double value, double transLambda)
{

	double transValue;

	if (value >= 0)
	{
		if (abs(transLambda) > 0.0000001)
		{

			transValue = (pow(value + 1, transLambda) - 1) / transLambda;

		}
		else
		{
			transValue = log(value + 1);
		}
	}
	else
	{
		if (abs(transLambda - 2.0) > 0.0000001)
		{
			transValue = -(pow(-value + 1.0, 2.0 - transLambda) - 1.0) / (2.0 - transLambda);
		}
		else
		{
			transValue = -log(-value + 1.0);
		}
	}


	return transValue;
}



double YeoJohnsonTransformation::invTransformOne(double value, double transLambda)
{

	double transValue;

	if (value >= 0)
	{
		if (abs(transLambda) > 0.0000001)
		{
			transValue = pow(transLambda * value + 1, 1 / transLambda) - 1;
		}
		else
		{
			transValue = exp(value) - 1;
		}
	}
	else
	{
		if (abs(transLambda - 2.0) > 0.0000001)
		{
			transValue = 1 - pow(-(2.0 - transLambda) * value + 1.0, 1.0 / (2.0 - transLambda));
		}
		else
		{
			transValue = 1 - exp(-value);
		}
	}

	return transValue;

}


double YeoJohnsonTransformation::logDensityTransformed(vector<double>& params, double transData, double data, double leftCensThresh, double rightCensThresh)
{


    double transLambda = params[0];
    double mean = params[1];
    double stdDev = params[2];

    double logDens;

    if (transData > leftCensThresh && transData < rightCensThresh) {

        //logDens = log(normPdf(transData, mean, stdDev));
		logDens = normLogPdf(transData, mean, stdDev);

        // Jacobian
        if (data >= 0) {
            logDens += log(pow(data + 1, transLambda - 1.0));
        } else {
            logDens += log(pow(-data + 1, 1.0 - transLambda));
        }

    } else if (transData <= leftCensThresh) {

        logDens = log(stdNormCdf((leftCensThresh-mean)/stdDev) );

    } else {

        logDens = log(1 - stdNormCdf((rightCensThresh-mean)/stdDev) );

    }

    return logDens;

}

double YeoJohnsonTransformation::logJacobianTransformed(vector<double>& params, double transData, double data, double leftCensThresh, double rightCensThresh)
{


    double transLambda = params[0];
    double mean = params[1];
    double stdDev = params[2];

    double logJac;

    if (transData > leftCensThresh && transData < rightCensThresh) {

        // Jacobian
        if (data >= 0) {
            logJac = log(pow(data + 1.0, transLambda - 1.0));
        } else {
            logJac = log(pow(-data + 1.0, 1.0 - transLambda));
        }

    } else if (transData <= leftCensThresh) {

        logJac = 0.0;

    } else {

        logJac = 0.0;
    }

    return logJac;

}



vector<double> YeoJohnsonTransformation::convertParams(vector<double>& params)
{

    vector<double> newParams = {params[0], params[1], exp(params[2])};

    m_transLambda = newParams[0];
    m_transMean = newParams[1];
    m_transStdDev = newParams[2];

    return newParams;
}


double YeoJohnsonTransformation::priorDensity() {

    //return log(normPdf(m_transLambda, getPriorMean(), getPriorStdDev()));
	return normLogPdf(m_transLambda, getPriorMean(), getPriorStdDev());

}

vector<double> YeoJohnsonTransformation::getScaleShift() {

    vector<double> params = {m_scale, m_shift};

    return params;

}


vector<double> YeoJohnsonTransformation::getTransformationParams () {

    vector<double> params = {m_transLambda};

    return params;

}

vector<double> YeoJohnsonTransformation::getDistributionParams () {

    vector<double> params = {m_transLambda, m_transMean, m_transStdDev};

    return params;

}