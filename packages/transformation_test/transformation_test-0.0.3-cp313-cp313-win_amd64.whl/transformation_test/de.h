#pragma once

#include <iostream>
#include <vector>
#include <functional>
#include <random>
#include <algorithm>
#include <numeric>

#include <Eigen/Dense>
using namespace Eigen;
using namespace std;


namespace DE {


    // helper function for converting Eigen Matrix to std vector
    vector<double> EigMatToVector(MatrixXd& mat, int row) {

        vector<double> newVec = vector<double>(mat.cols());
        for (int col_i=0; col_i < mat.cols(); col_i++) {

            newVec[col_i] = mat(row, col_i);
        }
        return newVec;

    }


    // helper function for converting Eigen Vector to std vector
    vector<double> EigVecToVector(VectorXd& vec) {

        vector<double> newVec = vector<double>(vec.size());
        for (int col_i=0; col_i < vec.size(); col_i++) {

            newVec[col_i] = vec(col_i);
        }
        return newVec;

    }

    // helper function for calculating mean from a std vector
    template <class D>
    double mean(const std::vector<D>& v)
    {
        double sum = 0;

        for (auto &each: v)
            sum += each;

        return sum / v.size();
    }


    // helper function for calculating standard deviation from a std vector
    template<class D>
    double sd(const std::vector<D>& v)
    {
        double square_suof_difference = 0;
        double mean_var = mean(v);
        auto len = v.size();

        double tmp;
        for (auto &each: v) {
            tmp = each - mean_var;
            square_suof_difference += tmp * tmp;
        }

        return std::sqrt(square_suof_difference / (len - 1));
    }

    // mutation operation
    template<class V>
    V mutation(const V& a, const V& b, const V& c, double F){

        return  a + (F * (b - c));

    }


    template<class D, class OP>
    tuple <std::vector<D>,int>
    optimise(OP objFunc, std::vector<D> lowerBounds, std::vector<D> upperBounds, int nPop, double F, double CR)

    {

        default_random_engine randomGenerator;
        double maxIters = 10000;
        int nParams = lowerBounds.size();

         // Uniform random samplers for standard uniform and indices for parameters and population members
        uniform_real_distribution<double> distUniformStd{0,1};
        uniform_int_distribution<int> distUniformParams{0,nParams-1};
        uniform_int_distribution<int> distUniformIndex{0,nPop-1};


        // initialise a population of candidate solutions randomly within the specified bounds
        MatrixXd population = MatrixXd(nPop, nParams);

    for (int i=0; i < nParams; i++) {

        uniform_real_distribution<double> distUniformBounds{lowerBounds[i],upperBounds[i]};

        for (int j=0; j < nPop; j++) {
            population(j,i) = distUniformBounds(randomGenerator);
            }
    }


    // a vector to store the current objective value for each population member
    vector<double> objectives = vector<double>(nPop);

    // Begin the iterative approach
    int iter_i = 0;
    for (iter_i=0; iter_i < maxIters; iter_i++ )
    {


        // For each population member identify three distinct vectors for the mutation
        int rand_idx;
        for (int pop_i=0; pop_i < nPop; pop_i++)
        {

            vector<int> rci = {pop_i, -1, -1, -1};

            // a messy but efficient way to randomly sample candidates without replacement
            for (int k=0; k < 3; k++)
            {

                bool unverified = true;
                while (unverified)
                {
                    rand_idx = distUniformIndex(randomGenerator);
                    for (int m=2; m>=0; m--)
                    {
                        if (m==0 && rand_idx != rci[m])
                        {
                            unverified = false;
                        } else if (rand_idx == rci[m])
                        {
                            break;
                        }
                    }
                }

                rci[k+1] = rand_idx;
            }



            // mutate using the three random selections to get the mutated vector

            VectorXd a = population.row(rci[1]);
            VectorXd b = population.row(rci[2]);
            VectorXd c = population.row(rci[3]);
            VectorXd mutated = mutation(a, b, c, F);


            // restrict mutated vector to bounds
            for (int param_i=0; param_i < nParams; param_i++)
            {

                if (mutated(param_i) < lowerBounds[param_i])
                {
                    mutated(param_i) = lowerBounds[param_i];
                }
                else if (mutated(param_i) > upperBounds[param_i])
                {
                    mutated(param_i) = upperBounds[param_i];
                }
            }


            // Mix up the original and mutated vector params to get a trial vector
            int R = distUniformParams(randomGenerator);
            VectorXd newPos(nParams);
            for (int param_i=0; param_i < nParams; param_i++) {

                //using binomial approach replace if random prob less than recombination prob but always replace when i == R
                double r = distUniformStd(randomGenerator);
                if (param_i == R || r < CR)
                    {
                        newPos(param_i) = mutated(param_i);
                    }
              else  {
                        newPos(param_i) = population(pop_i,param_i);}
                    }

            // write the modified vec back to the population if the objective is improved

            vector<double> v1 = EigVecToVector(newPos);
            vector<double> v2 = EigMatToVector(population, pop_i);

            if (objFunc(v1) <= objFunc(v2))
            {
                population.row(pop_i) = newPos;
            }
            vector<double> v3 = EigMatToVector(population, pop_i);
            objectives[pop_i] = objFunc(v3);


        }


        // The stopping condition is from Scipy:
        // std(objectives)/mean(objectives) <= tol
        // i.e. all the individuals have converged to approximately the same cost function value.
        double tol = 1E-6;
        if (sd(objectives) <= tol * abs(mean(objectives)))
        {
            cout << "DE converged after " << iter_i << " iterations" << endl;
            break;
        } else {

        }


    }


    // return the parameter set with the lowest cost function value (i.e. minimum objective)
    vector<double> testParams;
    vector<double> finalParams;
    double finalObj = 1E20;
    double testObj;
    for (int pop_i=0; pop_i < nPop; pop_i++)
    {
        testParams = EigMatToVector(population, pop_i);
        testObj = objFunc(testParams);
        if (testObj < finalObj)
        {
            finalObj = testObj;
            finalParams = testParams;
        }
    }


    return make_tuple(finalParams, iter_i);



    }


}
