
#pragma once

#include <cmath>
#include <iostream>
#include <vector>
#include <tuple>

#include <boost/math/constants/constants.hpp>

using namespace std;

//#include "de.h"
//#include "SCE.h"
#include "simplex.h"


using BT::Simplex;


class Transformation  {

public:

    Transformation();
    ~Transformation();

    // pure virtual functions must be implemented in derived classes
    virtual double transformOne(double value) = 0; // Uses object's current value of transLambda
    virtual double invTransformOne(double value) = 0;

    vector<double> transformMany(vector<double> values); // Uses object's current transformation parameters
    vector<double> invTransformMany(vector<double> values);

    double rescaleOne(double value); // Uses object's current value of scale and shift
    vector<double> rescaleMany(vector<double> values);

    double invRescaleOne(double value);
    vector<double> invRescaleMany(vector<double> values);

    double invRescaleOne(double value, double scale, double shift);
    double rescaleOne(double value, double scale, double shift);

    vector<double> optimParams(vector<double> data, double leftCensThresh, double rightCensThresh, bool doRescale, bool isMap);
    vector<double> optimParamsDE(vector<double> data, double leftCensThresh, double rightCensThresh, bool doRescale, bool isMap);
    vector<double> optimParamsSCE(vector<double> data, double leftCensThresh, double rightCensThresh, bool doRescale, bool isMap);

    double negLogPosterior(vector<double>& params, vector<double>& data, double leftCensThresh, double rightCensThresh, bool isMap);
    double LogPosterior(vector<double>& params, vector<double>& data, double leftCensThresh, double rightCensThresh, bool isMap);
    virtual double logDensity(vector<double>& params, double value, double leftCensThresh, double rightCensThresh, bool doRescale);
    virtual double logJacobian(vector<double>& params, double value, double leftCensThresh, double rightCensThresh, bool doRescale);

    virtual int getNumParams() = 0;
    virtual vector<double> getStartValues() = 0;
    virtual vector<double> getLowerBounds() = 0;
    virtual vector<double> getUpperBounds() = 0;
    virtual vector<double> convertParams(vector<double>& params) = 0;
    virtual double priorDensity() = 0;

    virtual vector<double> getScaleShift() = 0;
    virtual vector<double> getTransformationParams() = 0;
    virtual vector<double> getDistributionParams() = 0;

    vector<double> getOptimisedParams();




protected:

    double m_scale;
    double m_shift;
    vector<double> m_optimisedParams;

    double stdNormCdf(double x);
	double normLogPdf(double x, double mean, double stdDev);

    virtual double logDensityTransformed(vector<double>& params, double transData, double rescaledData, double leftCensThresh, double rightCensThresh) = 0;
    virtual double logJacobianTransformed(vector<double>& params, double transData, double rescaledData, double leftCensThresh, double rightCensThresh) = 0;


};

class YeoJohnsonTransformation : public Transformation {

public:

    YeoJohnsonTransformation();
    YeoJohnsonTransformation(double transLambda);
    YeoJohnsonTransformation(double transLambda, double scale, double shift);

    double transformOne(double value);
    double transformOne(double value, double transLambda); // Uses given transLambda
    double invTransformOne(double value);
    double invTransformOne(double value, double transLambda);

    int getNumParams() {return 1;}
    vector<double> getStartValues() { vector<double> vec = {1.0, 0.01, 0.01}; return vec; };
    vector<double> getLowerBounds() { vector<double> vec = {-100,-100,-100}; return vec; };
    vector<double> getUpperBounds() { vector<double> vec = {100,100,100}; return vec; };

    double priorDensity();
    vector<double> convertParams(vector<double>& params);
    virtual vector<double> getScaleShift();
    virtual vector<double> getTransformationParams();
    virtual vector<double> getDistributionParams();


protected:

    double m_transLambda;
    double m_transMean;
    double m_transStdDev;

    double getPriorMean() {return 1.0;};
    double getPriorStdDev() {return 0.4;};

    double logDensityTransformed(vector<double>& params, double transData, double rescaledData, double leftCensThresh, double rightCensThresh);
    double logJacobianTransformed(vector<double>& params, double transData, double rescaledData, double leftCensThresh, double rightCensThresh);


};


class LogSinhTransformation : public Transformation {

public:

    LogSinhTransformation();
    LogSinhTransformation(double transLambda, double transEpsilon);
    LogSinhTransformation(double transLambda, double transEpsilon, double scale);

    double transformOne(double value); // Uses object's current transformation and rescaling parameters
    double transformOne(double value, double transLambda, double transEpsilon);
    double invTransformOne(double value);
    double invTransformOne(double value, double transLambda, double transEpsilon);

    int getNumParams() {return 2;}
    vector<double> getStartValues() { vector<double> vec = {-0.01, -1.01, -1.01, 1.01}; return vec; };
    vector<double> getLowerBounds() { vector<double> vec = {-25,-25,-100,-10}; return vec; };
    vector<double> getUpperBounds() { vector<double> vec = {0.0,5.0,100,10}; return vec; };

    double priorDensity();
    vector<double> convertParams(vector<double>& params);
    virtual vector<double> getScaleShift();
    virtual vector<double> getTransformationParams();
    virtual vector<double> getDistributionParams();


protected:


    double m_transLambda;
    double m_transEpsilon;
    double m_transMean;
    double m_transStdDev;

    double getPriorMean() {return 0.0;};
    double getPriorStdDev() {return 1.0;};

    double logDensityTransformed(vector<double>& params, double transData, double rescaledData, double leftCensThresh, double rightCensThresh);
    double logJacobianTransformed(vector<double>& params, double transData, double rescaledData, double leftCensThresh, double rightCensThresh);


};



class SinhAsinhTransformation : public Transformation {

public:

    SinhAsinhTransformation();
    SinhAsinhTransformation(double transDelta, double transEpsilon);
    SinhAsinhTransformation(double transDelta, double transEpsilon, double scale, double shift);

    double transformOne(double value); // Uses object's current transformation and rescaling parameters
    double transformOne(double value, double transDelta, double transEpsilon);
    double invTransformOne(double value);
    double invTransformOne(double value, double transDelta, double transEpsilon);

    int getNumParams() {return 2;}
    vector<double> getStartValues() { vector<double> vec = {0.5, 0.5, 0.5, 0.5}; return vec; };
    vector<double> getLowerBounds() { vector<double> vec = {0.001,-0.999,-0.999,0.001}; return vec; };
    vector<double> getUpperBounds() { vector<double> vec = {0.999,0.999,0.999,0.999}; return vec; };

    double priorDensity();
    vector<double> convertParams(vector<double>& params);
    virtual vector<double> getScaleShift();
    virtual vector<double> getTransformationParams();
    virtual vector<double> getDistributionParams();


protected:


    double m_transDelta;
    double m_transEpsilon;
    double m_transMean;
    double m_transStdDev;

    double getPriorMean() {return 0.5;};
    double getPriorStdDev() {return 0.05;};

    double logDensityTransformed(vector<double>& params, double transData, double rescaledData, double leftCensThresh, double rightCensThresh);
    double logJacobianTransformed(vector<double>& params, double transData, double rescaledData, double leftCensThresh, double rightCensThresh);


};