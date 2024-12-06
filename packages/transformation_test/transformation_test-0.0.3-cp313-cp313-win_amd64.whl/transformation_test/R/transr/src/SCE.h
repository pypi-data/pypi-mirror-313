
//#include "randomnums.h"
#include <math.h>
#include <vector>
#include <algorithm>
#include <random>
#include <tuple>
#include <iostream>

namespace SCE{

	std::default_random_engine generator;
	std::uniform_real_distribution<double> unidist(0.0, 1.0);

	double rand_uniform()
	{
		double x = unidist(generator);
		return (x);
	}

	template<class D>
	bool getInFeas(vector<D> param, int nParam, vector<D> lowPar, vector<D> highPar)
	{
		bool result;
		int i;
		result = false;
		for (i = 0; i < nParam; i++)
		{
			if (param[i] < lowPar[i] || param[i] > highPar[i])
			{
				result = true;
			}
		}
		return result;
	}

	template<class D>
	void getNewPt(std::vector<D> &param, int nParam, std::vector<D> low, std::vector<D> high)
	{
		int i;
		for (i = 0; i < nParam; i++)
		{
			D runif = (D) rand_uniform();
			param[i] = low[i] + runif * (high[i] - low[i]);
		}
		return;
	}

	template<class D>
	void gaSiSort(std::vector<D> &value, std::vector<int> &point, int nl, int nlx)
	{
		std::vector< std::pair<D, int> > sdata(nl);
		int i = 0;
		for (auto& p : sdata)
		{
			p.first = value[i];
			p.second = point[i];
			i++;
		}
		std::sort(sdata.begin(), sdata.end(), [](std::pair<D, int> const&i, std::pair<D, int> const&j) {return i.first > j.first; });
		i = 0;
		for (auto&p : sdata)
		{
			value[i] = p.first;
			point[i] = p.second;
			i++;
		}
	}

	//!
	//! CCE algorithm
	template<class D, class OP>
	void cceEvolve(int alpha, int nfit, int m, std::vector<int> &ptC, std::vector<D> &cumProb, std::vector<int> &ptB, std::vector<int> point,
		std::vector<int>  &ptL, std::vector<D> &newF, std::vector<D> &oldF, std::vector<std::vector<D>> &u, std::vector<D> g, int &neval, int mPop, int mx,
		int npx, std::vector<D> &xFit, std::vector<D> lowPar, std::vector<D> highPar, int nMutate, int maxEval, bool cancel,	OP objFunc)
	{
		int i;
		int j, count;
		bool ok, infeasible;
		double prob, move, totProb, gFit, low, high;
		bool upReflect = false, weight = false, bestCube = true;
		double bigF = -1e10, scaleCube = 4.0;

		//!------
		//! Implement Duan et al (1992) competitive complex evolution search
		//!------
		//! Initialise
		double reflect = 1.0;
		int beta = m;
		int q = nfit + 1;

		//! Initially m points in complex are ordered		   
		for (i = 0; i < m; i++)
		{
			point[i] = i;
		}

		//! Beta loop --> Allow sub-complex to evolve beta times
		int bLoop;
		for (bLoop = 0; bLoop < beta; bLoop++) {
			//! Select q distinct points from A complex by randomly sampling
			//! from triangular distribution --> This defines the B complex
			//! ptB points to locations in original arrays
			for (i = 0; i < q; i++) {
				ok = false;
				while (ok == false) {
					prob = rand_uniform();
					for (j = 0; j < m; j++) {
						if (prob <= cumProb[j]) {
							ptB[i] = ptC[point[j]];
							break;
						}
					}
					ok = true;
					for (j = 0; j < i; j++)
					{
						if (ptB[i] == ptB[j])
						{
							ok = false;
							break;
						}
					}
				}
			}

			//!-------
			//! Alpha loop --> worst point in complex is reflected or contracted
			//!                to seek an improvement alpha times
			int aLoop;
			for (aLoop = 0; aLoop < alpha; aLoop++) {
				//!
				//! Sort points in B complex using POINTER ptL
				for (i = 0; i < q; i++) {
					newF[i] = oldF[ptB[i]];
					ptL[i] = ptB[i];
				}
				gaSiSort(newF, ptL, q, q);
				//! Find centroid g excluding worst point and
				//! compute reflection of worst point about centroid 2g - u(worst)
				if (upReflect) {
					move = (double)aLoop * reflect;
				}
				else {
					move = reflect;
				}
				for (i = 0; i < nfit; i++) {
					g[i] = 0.0;
					if (weight) totProb = 0.0;
					for (j = 0; j < (q - 1); j++) {
						if (weight) {
							prob = 2.0 * (double)(q - j) / (double)(q*(q - 1));
							g[i] = g[i] + u[ptL[j]][i] * prob;
							totProb = totProb + prob;
						}
						else {
							g[i] = g[i] + u[ptL[j]][i]; 
						}
					}
					if (weight) {
						g[i] = g[i] / totProb;
					}
					else {
						g[i] = g[i] / (double)(q - 1);
					}
					xFit[i] = move*(g[i] - u[ptL[q - 1]][i]) + g[i];
				}
				//! Get new obj FUNCTION value
				infeasible = getInFeas(xFit, nfit, lowPar, highPar);
				if (infeasible == false)
				{
					gFit = objFunc(xFit); 
					neval++; 
					reflect = 1.0;
				}
				else {
					reflect = 0.5 * reflect;
					gFit = bigF;
				}
				//! If point is infeasible perform mutation
				count = 0;
				while (ok == false || gFit <= bigF || infeasible == true)
				{
					//! Compute smallest hypercube enclosing A complex and randomly sample
					//! a point within it
					count = count + 1;
					//            count = count + 1
					for (i = 0; i < nfit; i++)
					{
						low = u[ptC[0]][i];
						high = low;
						for (j = 1; j < m; j++) {
							if (u[ptC[j]][i] <= low) low = u[ptC[j]][i];
							if (u[ptC[j]][i] >= high) high = u[ptC[j]][i];
						}
						xFit[i] = low + rand_uniform()*(high - low);
					}
					infeasible = getInFeas(xFit, nfit, lowPar, highPar);
					if (infeasible == false) {
						gFit = objFunc(xFit);
						neval++; // = neval +1;
						nMutate = nMutate + 1;
					}

					//! Give up mutations IF unsuccessful after nfit tries
					if (count > nfit) {
						gFit = oldF[ptL[q - 1]] - 100.0;
						break;
					}
				}

				//! Either replace worst point with better point
				//! or contract to midpoint between centroid and worst point
				if (gFit > oldF[ptL[q - 1]]) {
					for (j = 0; j < nfit; j++) u[ptL[q - 1]][j] = xFit[j];
					oldF[ptL[q - 1]] = gFit;
				}
				else {
					for (j = 0; j < nfit; j++) g[j] = (g[j] + u[ptL[q - 1]][j]) / 2.0;

					//! Evaluate contracted point
					//! If better than worst point replace worst point
					//! Otherwise mutate and replace worst point regardless of outcome

					infeasible = getInFeas(g, nfit, lowPar, highPar);
					if (infeasible == false) {
						gFit = objFunc(g);
						neval++; 
					}

					if (ok == true || gFit > oldF[ptL[q - 1]] || infeasible == true) {
						for (j = 0; j < nfit; j++)  u[ptL[q - 1]][j] = g[j];
						oldF[ptL[q - 1]] = gFit;
					}
					else {
						//! Compute small hypercube and randomly sample a point within it
						ok = false;
						gFit = bigF;
						count = 0;

						while (ok == false || gFit <= bigF)
							count++;
						if (count > nfit) break;

						for (i = 0; i < nfit; i++) {
							if (bestCube) {
								low = fabs(u[ptL[1]][i] - u[ptL[0]][i]) / ((double)count * scaleCube);
								high = u[ptL[0]][i] + low;
								low = u[ptL[0]][i] - low;
								g[i] = low + rand_uniform() * (high - low);
							}
							else {
								low = u[i][ptC[0]];
								high = low;
								for (j = 1; j < m; j++) {
									if (u[ptC[j]][i] < low) low = u[ptC[j]][i];
									if (u[ptC[j]][i] > high) high = u[ptC[j]][i];
								}
								g[i] = low + rand_uniform()*(high - low);
							}
						}

						infeasible = getInFeas(g, nfit, lowPar, highPar);
						if (infeasible == false) {
							gFit = objFunc( g);
							neval++; // = neval +1;
							nMutate = nMutate + 1;
						}
						else {
							ok = false;
						}
					}
					//! Replace worst point with new point regardless of its value
					for (j = 0; j < nfit; j++) u[ptL[q - 1]][j] = g[j];
					oldF[ptL[q - 1]] = gFit;
					//               u(1:nfit,ptL(q)) = g(1:nfit)
					//               oldF(ptL(q)) = gFit
				}
				//            END IF
			}

			//! Order points in complex using the POINTER point
			for (i = 0; i < m; i++) {
				newF[i] = oldF[ptC[i]];
				point[i] = i;
			}
			gaSiSort(newF, point, m, m);
		}
	}

	//!
	//! SCE search finds std::maximum of objective function
	template<class D, class OP>
	tuple < std::vector<D>, int >
		sceSearch(OP objFunc,
		std::vector<D> lowPar,
		std::vector<D> highPar,
		int maxConverge = 20,
		int maxEval = 100000,
		D tol = 1e-6)
	{

		int nfit = int(lowPar.size());
		int p = nfit;
		D bestF;
		//SUBROUTINE sceSearch (maxConverge, p, nfit, maxEval, tol, lowPar, highPar, &
		//                      bestF, bestPar, error, neval, dump, du, name, objFunc)
		//!------
		//! Implement Duan et al (1992) SCE-UA probabilistic search
		//! Full details in Water Resources Research, 28(4), 1015-1031, 1992
		//!
		//! Input arguments:
		//!   maxConverge = std::max consecutive times iteration fails to improve
		//!                 fitness before convergence is declared
		//!   p = number of complexes (recommend = number of fitted parameters)
		//!   nfit = number of fitted parameters
		//!   maxEval = std::max number of FUNCTION evaluations
		//!   tol = convergence tolerance
		//!   lowPar = lower bound on parameters
		//!   highPar = upper bound on parameters
		//!
		//! Output arguments:
		//!   bestF = best fitness
		//!   bestPar = PARAMETER corresponding to best fitness
		//!   error = error flag
		//!   neval = number of FUNCTION evaluations
		//!----
		//IMPLICIT NONE
		int i, j, m, converge, mPop, nMutate, alpha, bestPt;

		//! probFlag = 1 uniform assignment of points to complex
		//!            2 trapezoidal
		int probFlag = 1;
		//INTEGER, PARAMETER :: probFlag=2
		std::vector<int> ptB, ptL, point;
		std::vector<D> bestPar;
		std::vector<std::vector<int>> ptC;

		std::vector<D> oldF, newF, cumProb, g, xFit;
		std::vector<std::vector<D>> u;

		double try1, oldBestF;
		double largeF = -1.0e30;
		bool ok, infeasible;
		bool uniform = true;
		long idum = -3 * 153351;
		
		//! Initialise objective function evaluator
		bool error = false;
		//! Initialise shuffled complex evolution (SCE) algorithm
		//! Allocate memory

		converge = 0;
		m = 2 * nfit + 1;
		mPop = p*m;

		oldF.resize(mPop);
		newF.resize(mPop);
		ptB.resize(m);
		ptL.resize(m);
		point.resize(mPop);
		cumProb.resize(m);
		g.resize(nfit);
		xFit.resize(nfit);
		bestPar.resize(nfit);
		ptC.resize(p, std::vector<int>(m));
		u.resize(mPop, std::vector<D>(nfit));

		oldBestF = largeF;
		int neval = 0;
		nMutate = 0;
		alpha = 1;

		if (probFlag == 1) {
			try1 = (D)m;
			for (i = 0; i < m; i++) cumProb[i] = ((D)(i + 1)) / try1;
		}
		else {
			try1 = (D)m*(m + 1);
			cumProb[0] = ((D)(2 * m)) / try1;
			for (i = 1; i < m; i++) cumProb[i] = ((D)(2 * (m + 1 - (i + 1)))) / try1 + cumProb[i - 1];
		}
		i = 0;

		while (i < mPop) {
			ok = false;
			oldF[i] = largeF;
			while (ok == false && oldF[i] <= largeF) {
				//! Select random points in fitted PARAMETER space
				getNewPt(u[i], nfit, lowPar, highPar);
				infeasible = getInFeas(u[i], nfit, lowPar, highPar);
				// If feasible evaluate fitness
				if (infeasible == false){
					oldF[i] = objFunc(u[i]);
					neval++;
				}
				else {
					ok = false;
				}
			}

			point[i] = i;
			newF[i] = oldF[i];
			i++;
		}
		//! Rank points in terms of fitness
		gaSiSort(newF, point, mPop, mPop);
		bestPt = 0;
		while (converge < maxConverge) {
			//! Partition populations into p complexes distributing points
			//! evenly between complexes
			for (i = 0; i < p; i++) {
				for (j = 0; j < m; j++) {
					ptC[i][j] = point[i + p*(j)];
				}
			}
			//! Evolve each complex according to competitive complex evolution
			//! (CCE) algorithm
			for (i = 0; i < p; i++) {
				cceEvolve(alpha, nfit, m, ptC[i], cumProb, ptB, point,
					ptL, newF, oldF, u, g, neval, mPop,
					m, nfit, xFit, lowPar, highPar, nMutate, maxEval, error, objFunc);
				if (error == true) {
					error = true;
					if (bestPt >= 0) {
						for (j = 0; j < nfit; j++)
						{
							bestPar[j] = u[bestPt][j];
						}
					}
					else {
						bestF = -1.0e30;
					}
				}
			}
			//! Rank all points in terms of fitness
			for (i = 0; i < mPop; i++) {
				newF[i] = oldF[i];
				point[i] = i;
			}
			gaSiSort(newF, point, mPop, mPop);
			//! Check for convergence
			//! If no improvement increase alpha to increase chance of sub-complexes evolving
			bestPt = point[0];
			bestF = oldF[bestPt];
			
			if (fabs(bestF) > 1.0e-6) {
				if (fabs(bestF - oldBestF) <= fabs(oldBestF*tol)) {
					converge++;
					if ((converge + 1) > 2) {
						alpha = converge + 1;
					}
					else {
						alpha = 2;
					}
					oldBestF = bestF;
				}
				else {
					oldBestF = bestF;
					converge = 0;
					alpha = 1;
				}
			}
			else {
				if (fabs(bestF - oldBestF) <= tol) {
					converge++;
					if ((converge + 1) > 2) {
						alpha = converge + 1;
					}
					else {
						alpha = 2;
					}
					oldBestF = bestF;
				}
				else {
					oldBestF = bestF;
					converge = 0;
					alpha = 1;
				}
			}

			//! Force EXIT IF std::max evaluations are exceeded

			if (neval > maxEval) break;

		}
		//   END DO
		//!
		//! Save best PARAMETER
		for (i = 0; i < nfit; i++) bestPar[i] = u[bestPt][i];

		return make_tuple(bestPar, neval);
	}
}