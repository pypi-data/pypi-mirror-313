
#pragma once

#include <cmath>
#include <iostream>
#include <vector>
#include <tuple>

#include <boost/math/constants/constants.hpp>


#pragma once

#ifndef TRANS_R_DLL_LIB_MODIFIERS

#ifdef _WIN32
#ifdef USING_TRANS_R_CORE
#define TRANS_R_CORE_DLL_LIB __declspec(dllimport)
#else
#define TRANS_R_CORE_DLL_LIB __declspec(dllexport)
// To prevent warnings such as:
// Warning	C4251	'datatypes::io::IoHelper::DefaultFilePattern' : class 'std::basic_string<char,std::char_traits<char>,std::allocator<char>>' needs to have dll - interface to be used by clients of class 'datatypes::io::IoHelper'
#pragma warning (disable : 4251)
#endif
#else
#define TRANS_R_CORE_DLL_LIB // nothing
#endif

// You can define the following to activate the Visual Leak Detector tool for visual C++
// https://vld.codeplex.com

//#define TRANS_R_USE_VLD

#else  //  TRANS_R_DLL_LIB_MODIFIERS is defined
#define TRANS_R_CORE_DLL_LIB TRANS_R_DLL_LIB_MODIFIERS 
#endif 

using namespace std;

class TRANS_R_CORE_DLL_LIB Transformation  {

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

    vector<double> optimParams(vector<double> data, double leftCensThresh, bool doRescale, bool isMap);
	vector<double> optimParamsSCE(vector<double> data, double leftCensThresh, bool doRescale, bool isMap);
    double negLogPosterior(vector<double>& params, vector<double>& data, double leftCensThresh, bool isMap);
	double LogPosterior(vector<double>& params, vector<double>& data, double leftCensThresh, bool isMap);
    virtual double logDensity(vector<double>& params, double value, double leftCensThresh, bool doRescale);
    virtual double logJacobian(vector<double>& params, double value, double leftCensThresh, bool doRescale);

    virtual int getNumParams() = 0;
    virtual vector<double> getStartValues() = 0;
	virtual vector<double> getMinValues() = 0;
	virtual vector<double> getMaxValues() = 0;
    virtual vector<double> convertParams(vector<double>& params) = 0;
    virtual double priorDensity() = 0;
    virtual vector<double> getParams() = 0;




protected:

    double m_scale;
    double m_shift;

    double stdNormCdf(double x);
	double normLogPdf(double x, double mean, double stdDev);

    virtual double logDensityTransformed(vector<double>& params, double transData, double rescaledData, double leftCensThresh) = 0;
    virtual double logJacobianTransformed(vector<double>& params, double transData, double rescaledData, double leftCensThresh) = 0;


};

class TRANS_R_CORE_DLL_LIB YeoJohnsonTransformation : public Transformation {

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

	vector<double> getMinValues() { vector<double> vec = { -3.0, -100.0, -10.0 }; return vec; };
	vector<double> getMaxValues() { vector<double> vec = { 3.0,  100.0, 10.0 }; return vec; };


    double priorDensity();
    vector<double> convertParams(vector<double>& params);
    virtual vector<double> getParams();




protected:

    double m_transLambda;

    double getPriorMean() {return 1.0;};
    double getPriorStdDev() {return 0.4;};

    double logDensityTransformed(vector<double>& params, double transData, double rescaledData, double leftCensThresh);
    double logJacobianTransformed(vector<double>& params, double transData, double rescaledData, double leftCensThresh);


};


class TRANS_R_CORE_DLL_LIB LogSinhTransformation : public Transformation {

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

	vector<double> getMinValues() { vector<double> vec = { -25.0, -25.0, -100.0, -10.0 }; return vec; };
	vector<double> getMaxValues() { vector<double> vec = { 0.0, 5.0, 100.0, 10.0 }; return vec; };


    double priorDensity();
    vector<double> convertParams(vector<double>& params);
    virtual vector<double> getParams();


protected:


    double m_transLambda;
    double m_transEpsilon;

    double getPriorMean() {return 0.0;};
    double getPriorStdDev() {return 1.0;};

    double logDensityTransformed(vector<double>& params, double transData, double rescaledData, double leftCensThresh);
    double logJacobianTransformed(vector<double>& params, double transData, double rescaledData, double leftCensThresh);



};


class TRANS_R_CORE_DLL_LIB BoxCoxTransformation : public Transformation {

public:

	BoxCoxTransformation();
	BoxCoxTransformation(double transLambda, double transEpsilon);
	BoxCoxTransformation(double transLambda, double transEpsilon, double scale);

	double transformOne(double value); // Uses object's current transformation and rescaling parameters
	double transformOne(double value, double transLambda, double transEpsilon);
	double invTransformOne(double value);
	double invTransformOne(double value, double transLambda, double transEpsilon);

	int getNumParams() { return 2; }
	vector<double> getStartValues() { vector<double> vec = { -0.01, -1.01, -1.01, 1.01 }; return vec; };

	vector<double> getMinValues() { vector<double> vec = { -3.0, -25.0, -100.0, -10.0 }; return vec; };
	vector<double> getMaxValues() { vector<double> vec = { 3.0, 0.0, 100.0, 10.0 }; return vec; };



	double priorDensity();
	vector<double> convertParams(vector<double>& params);
	virtual vector<double> getParams();


protected:


	double m_transLambda;
	double m_transEpsilon;

	double getPriorMean() { return 1.0; };
	double getPriorStdDev() { return 0.4; };

	double logDensityTransformed(vector<double>& params, double transData, double rescaledData, double leftCensThresh);
	double logJacobianTransformed(vector<double>& params, double transData, double rescaledData, double leftCensThresh);



};