# distutils: language = c++

import time

import numpy as np
cimport numpy as np
from libcpp.vector cimport vector
from libcpp cimport bool


cdef extern from "Transformation.h":

    cdef cppclass Transformation:

        Transformation() except +

        double m_transLambda
        double m_transEpsilon
        double m_transMean
        double m_transStdDev

        double transformOne(double value)
        double invTransformOne(double value)

        double rescaleOne(double value)
        double invRescaleOne(double value)

        vector[double] transformMany(vector[double] values)
        vector[double] invTransformMany(vector[double] values)

        vector[double] rescaleMany(vector[double] values)
        vector[double] invRescaleMany(vector[double] values);

        int getNumParams()
        vector[double] optimParams(vector[double] data, double leftCensThresh, double rightCensThresh, bool doRescale, bool isMap)
        vector[double] optimParamsDE(vector[double] data, double leftCensThresh, double rightCensThresh, bool doRescale, bool isMap)
        vector[double] optimParamsSCE(vector[double] data, double leftCensThresh, double rightCensThresh, bool doRescale, bool isMap)

        double logDensity(vector[double] params, double value, double leftCensThresh, double rightCensThresh, bool doRescale)
        double logJacobian(vector[double] params, double value, double leftCensThresh, double rightCensThresh, bool doRescale)

        vector[double] getScaleShift()
        vector[double] getTransformationParams()
        vector[double] getDistributionParams()
        vector[double] getOptimisedParams()

    cdef cppclass YeoJohnsonTransformation(Transformation):

        YeoJohnsonTransformation() except +
        YeoJohnsonTransformation(double transLambda, double scale, double shift) except +

        double transformOne(double value, double transLambda)
        double invTransformOne(double value, double transLambda)

    cdef cppclass LogSinhTransformation(Transformation):

        LogSinhTransformation() except +
        LogSinhTransformation(double transLambda, double transEpsilon, double scale) except +

        double transformOne(double value, double transLambda, double transEpsilon)
        double invTransformOne(double value, double transLambda, double transEpsilon)

    cdef cppclass SinhAsinhTransformation(Transformation):
        SinhAsinhTransformation() except +
        SinhAsinhTransformation(double transDelta, double transEpsilon, double scale, double shift) except +

        double transformOne(double value, double transDelta, double transEpsilon)
        double invTransformOne(double value, double transDelta, double transEpsilon)

cdef class PyYJT:


    cdef YeoJohnsonTransformation yj_trans      # hold a C++ instance which we're wrapping
    cdef double[:] trans_params

    def __cinit__(self, double trans_lambda=1.0, scale=1.0, shift=0.0):

        self.yj_trans = YeoJohnsonTransformation(trans_lambda, scale, shift)
        self.trans_params = None


    def transform_one(self, double value, trans_lambda=None):

        if trans_lambda is None:
            return self.yj_trans.transformOne(value)
        else:
            return self.yj_trans.transformOne(value, trans_lambda)



    def transform_many(self, double[:] values):

        cdef vector[double] vec

        for i in range(len(values)):
            vec.push_back(values[i])

        trans_vec = self.yj_trans.transformMany(vec)

        return np.fromiter(trans_vec, dtype = float)



    def inv_transform_many(self, double[:] values):

        cdef vector[double] vec

        for i in range(len(values)):
            vec.push_back(values[i])

        trans_vec = self.yj_trans.invTransformMany(vec)

        return np.fromiter(trans_vec, dtype = float)



    def rescale_one(self, double value):

        return self.yj_trans.rescaleOne(value)



    def inv_rescale_one(self, double value):

        return self.yj_trans.invRescaleOne(value)



    def rescale_many(self, double[:] values):

        cdef vector[double] vec

        for i in range(len(values)):
            vec.push_back(values[i])

        trans_vec = self.yj_trans.rescaleMany(vec)

        return np.fromiter(trans_vec, dtype = float)



    def inv_rescale_many(self, double[:] values):

        cdef vector[double] vec

        for i in range(len(values)):
            vec.push_back(values[i])

        trans_vec = self.yj_trans.invRescaleMany(vec)

        return np.fromiter(trans_vec, dtype = float)


    def optim_params(self, double[:] data, double left_cens_thresh, double right_cens_thresh, bool do_rescale, bool is_map):

        cdef vector[double] vec

        for i in range(len(data)):
            vec.push_back(data[i])

        trans_vec = self.yj_trans.optimParams(vec, left_cens_thresh, right_cens_thresh, do_rescale, is_map)

        self.trans_params = np.fromiter(trans_vec, dtype = float)


    def optim_paramsDE(self, double[:] data, double left_cens_thresh, double right_cens_thresh, bool do_rescale, bool is_map):

        cdef vector[double] vec

        for i in range(len(data)):
            vec.push_back(data[i])

        trans_vec = self.yj_trans.optimParamsDE(vec, left_cens_thresh, right_cens_thresh, do_rescale, is_map)

        self.trans_params = np.fromiter(trans_vec, dtype = float)


    def optim_paramsSCE(self, double[:] data, double left_cens_thresh, double right_cens_thresh, bool do_rescale, bool is_map):

        cdef vector[double] vec

        for i in range(len(data)):
            vec.push_back(data[i])

        trans_vec = self.yj_trans.optimParamsSCE(vec, left_cens_thresh, right_cens_thresh, do_rescale, is_map)

        self.trans_params = np.fromiter(trans_vec, dtype = float)


    def get_optimised_params(self):

        return self.yj_trans.getOptimisedParams()

    def get_scale_shift(self):

        return self.yj_trans.getScaleShift()

    def get_transformation_params(self):

        return self.yj_trans.getTransformationParams()

    def get_distribution_params(self):

        return self.yj_trans.getDistributionParams()



    def log_density(self, double[:] params, double value, double left_cens_thresh, double right_cens_thresh, bool do_rescale):

        cdef vector[double] params_vec

        for i in range(len(params)):
            params_vec.push_back(params[i])

        logDens = self.yj_trans.logDensity(params_vec, value, left_cens_thresh, right_cens_thresh, do_rescale)

        return logDens



    def log_jacobian(self, double[:] params, double value, double left_cens_thresh, double right_cens_thresh, bool do_rescale):

        cdef vector[double] params_vec

        for i in range(len(params)):
            params_vec.push_back(params[i])

        logJac = self.yj_trans.logJacobian(params_vec, value, left_cens_thresh, right_cens_thresh, do_rescale)

        return logJac



    def __str__(self):
        return "PyYJT"



cdef class PyLogSinh:


    cdef LogSinhTransformation logsinh_trans      # hold a C++ instance which we're wrapping
    cdef double[:] trans_params

    def __cinit__(self, double trans_lambda=1.0, double trans_epsilon=0.0, scale=1.0):

        self.logsinh_trans = LogSinhTransformation(trans_lambda, trans_epsilon, scale)
        self.trans_params = None



    def transform_one(self, double value, trans_lambda=None, trans_epsilon=None):

        if trans_lambda is None:
            return self.logsinh_trans.transformOne(value)
        else:
            return self.logsinh_trans.transformOne(value, trans_lambda, trans_epsilon)



    def transform_many(self, double[:] values):

        cdef vector[double] vec

        for i in range(len(values)):
            vec.push_back(values[i])

        trans_vec = self.logsinh_trans.transformMany(vec)

        return np.fromiter(trans_vec, dtype = float)



    def inv_transform_many(self, double[:] values):

        cdef vector[double] vec

        for i in range(len(values)):
            vec.push_back(values[i])

        trans_vec = self.logsinh_trans.invTransformMany(vec)

        return np.fromiter(trans_vec, dtype = float)



    def rescale_one(self, double value):

        return self.logsinh_trans.rescaleOne(value)



    def inv_rescale_one(self, double value):

        return self.logsinh_trans.invRescaleOne(value)



    def rescale_many(self, double[:] values):

        cdef vector[double] vec

        for i in range(len(values)):
            vec.push_back(values[i])

        trans_vec = self.logsinh_trans.rescaleMany(vec)

        return np.fromiter(trans_vec, dtype = float)



    def inv_rescale_many(self, double[:] values):

        cdef vector[double] vec

        for i in range(len(values)):
            vec.push_back(values[i])

        trans_vec = self.logsinh_trans.invRescaleMany(vec)

        return np.fromiter(trans_vec, dtype = float)



    def optim_params(self, double[:] data, double left_cens_thresh, double right_cens_thresh, bool do_rescale, bool is_map):

        cdef vector[double] vec

        for i in range(len(data)):
            vec.push_back(data[i])

        trans_vec = self.logsinh_trans.optimParams(vec, left_cens_thresh, right_cens_thresh, do_rescale, is_map)

        self.trans_params = np.fromiter(trans_vec, dtype = float)


    def optim_paramsDE(self, double[:] data, double left_cens_thresh, double right_cens_thresh, bool do_rescale, bool is_map):

        cdef vector[double] vec

        for i in range(len(data)):
            vec.push_back(data[i])

        trans_vec = self.logsinh_trans.optimParamsDE(vec, left_cens_thresh, right_cens_thresh, do_rescale, is_map)

        self.trans_params = np.fromiter(trans_vec, dtype = float)


    def optim_paramsSCE(self, double[:] data, double left_cens_thresh, double right_cens_thresh, do_rescale, bool is_map):

        cdef vector[double] vec

        for i in range(len(data)):
            vec.push_back(data[i])

        trans_vec = self.logsinh_trans.optimParamsSCE(vec, left_cens_thresh, right_cens_thresh, do_rescale, is_map)

        self.trans_params = np.fromiter(trans_vec, dtype = float)


    def get_optimised_params(self):

        return self.logsinh_trans.getOptimisedParams()

    def get_scale_shift(self):

        return self.logsinh_trans.getScaleShift()

    def get_transformation_params(self):

        return self.logsinh_trans.getTransformationParams()

    def get_distribution_params(self):

        return self.logsinh_trans.getDistributionParams()



    def log_density(self, double[:] params, double value, double left_cens_thresh, double right_cens_thresh, bool do_rescale):

        cdef vector[double] params_vec

        for i in range(len(params)):
            params_vec.push_back(params[i])

        logDens = self.logsinh_trans.logDensity(params_vec, value, left_cens_thresh, right_cens_thresh, do_rescale)

        return logDens



    def log_jacobian(self, double[:] params, double value, double left_cens_thresh, double right_cens_thresh, bool do_rescale):

        cdef vector[double] params_vec

        for i in range(len(params)):
            params_vec.push_back(params[i])

        logJac = self.logsinh_trans.logJacobian(params_vec, value, left_cens_thresh, right_cens_thresh, do_rescale)

        return logJac



    def __str__(self):
        return "PyLogSinh"



cdef class PySinhAsinh:


    cdef SinhAsinhTransformation sash_trans      # hold a C++ instance which we're wrapping
    cdef double[:] trans_params

    def __cinit__(self, double trans_delta=1.0, double trans_epsilon=0.0, scale=1.0, shift=0.0):

        self.sash_trans = SinhAsinhTransformation(trans_delta, trans_epsilon, scale, shift)
        self.trans_params = None



    def transform_one(self, double value, trans_delta=None, trans_epsilon=None):

        if trans_delta is None:
            return self.sash_trans.transformOne(value)
        else:
            return self.sash_trans.transformOne(value, trans_delta, trans_epsilon)



    def transform_many(self, double[:] values):

        cdef vector[double] vec

        for i in range(len(values)):
            vec.push_back(values[i])

        trans_vec = self.sash_trans.transformMany(vec)

        return np.fromiter(trans_vec, dtype = float)



    def inv_transform_many(self, double[:] values):

        cdef vector[double] vec

        for i in range(len(values)):
            vec.push_back(values[i])

        trans_vec = self.sash_trans.invTransformMany(vec)

        return np.fromiter(trans_vec, dtype = float)



    def rescale_one(self, double value):

        return self.sash_trans.rescaleOne(value)



    def inv_rescale_one(self, double value):

        return self.sash_trans.invRescaleOne(value)



    def rescale_many(self, double[:] values):

        cdef vector[double] vec

        for i in range(len(values)):
            vec.push_back(values[i])

        trans_vec = self.sash_trans.rescaleMany(vec)

        return np.fromiter(trans_vec, dtype = float)



    def inv_rescale_many(self, double[:] values):

        cdef vector[double] vec

        for i in range(len(values)):
            vec.push_back(values[i])

        trans_vec = self.sash_trans.invRescaleMany(vec)

        return np.fromiter(trans_vec, dtype = float)



    def optim_params(self, double[:] data, double left_cens_thresh, double right_cens_thresh, bool do_rescale, bool is_map):

        cdef vector[double] vec

        for i in range(len(data)):
            vec.push_back(data[i])

        trans_vec = self.sash_trans.optimParams(vec, left_cens_thresh, right_cens_thresh, do_rescale, is_map)

        self.trans_params = np.fromiter(trans_vec, dtype = float)


    def optim_paramsDE(self, double[:] data, double left_cens_thresh, double right_cens_thresh, bool do_rescale, bool is_map):

        cdef vector[double] vec

        for i in range(len(data)):
            vec.push_back(data[i])

        trans_vec = self.sash_trans.optimParamsDE(vec, left_cens_thresh, right_cens_thresh, do_rescale, is_map)

        self.trans_params = np.fromiter(trans_vec, dtype = float)

    def optim_paramsSCE(self, double[:] data, double left_cens_thresh, double right_cens_thresh, bool do_rescale, bool is_map):

        cdef vector[double] vec

        for i in range(len(data)):
            vec.push_back(data[i])

        trans_vec = self.sash_trans.optimParamsSCE(vec, left_cens_thresh, right_cens_thresh, do_rescale, is_map)

        self.trans_params = np.fromiter(trans_vec, dtype = float)


    def get_optimised_params(self):

        return self.sash_trans.getOptimisedParams()

    def get_scale_shift(self):

        return self.sash_trans.getScaleShift()

    def get_transformation_params(self):

        return self.sash_trans.getTransformationParams()

    def get_distribution_params(self):

        return self.sash_trans.getDistributionParams()



    def log_density(self, double[:] params, double value, double left_cens_thresh, double right_cens_thresh, bool do_rescale):

        cdef vector[double] params_vec

        for i in range(len(params)):
            params_vec.push_back(params[i])

        logDens = self.sash_trans.logDensity(params_vec, value, left_cens_thresh, right_cens_thresh, do_rescale)

        return logDens



    def log_jacobian(self, double[:] params, double value, double left_cens_thresh, double right_cens_thresh, bool do_rescale):

        cdef vector[double] params_vec

        for i in range(len(params)):
            params_vec.push_back(params[i])

        logJac = self.sash_trans.logJacobian(params_vec, value, left_cens_thresh, right_cens_thresh, do_rescale)

        return logJac



    def __str__(self):
        return "PySinhASinh"





