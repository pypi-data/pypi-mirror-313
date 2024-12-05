#include <math.h>
#include <stdio.h>
#include <fenv.h>

void gaussian2d(double * data, long Nx, long Ny,
                double x0, double y0, double alpha,
                double beta, double gamma, double A, double b){
  long k = 0;
  int i, j;
  double X, Y;
  for (i = 0; i < Nx; i++){
    X = i - x0;
    for (j = 0; j < Ny; j++){
      Y = j - y0;
      data[k++] = A * exp(-(alpha * X * X + beta * Y * Y + gamma * X * Y)) + b;
    }
  }
}

void gaussian2d_der(double * data, long Nx, long Ny,
		    double x0, double y0, double alpha,
		    double beta, double gamma, double A, double b){
  long k = 0;
  int i, j;
  double X, Y, G, AG;
  for (i = 0; i < Nx; i++){
    X = i - x0;
    for (j = 0; j < Ny; j++){
      Y = j - y0;
      G = exp(-(alpha * X * X + beta * Y * Y + gamma * X * Y));
      AG = A * G;
      data[k++] = (2 * alpha * X + Y * gamma) * AG; // dx0
      data[k++] = (2 * beta * Y + X * gamma) * AG; // dy0
      data[k++] = -(X * X) * AG; // dalpha
      data[k++] = -(Y * Y) * AG; // dbeta
      data[k++] = -(X * Y) * AG; // dgamma
      data[k++] = G; // dA
      data[k++] = 1;
    }
  }
}

#define NSIGMA 32
int gaussian_weighted_moments(double * data,
			      long * dims,
			      double* xc, double* yc,
			      double* mxxold, double* myyold, double* mxyold
			      ){
  //feenableexcept(FE_INVALID | FE_OVERFLOW);
  double det, mxx, myy, mxy, wxx, wyy, wxy, dx, dy, wg, x1, y1, f;
  int flag=1;
  int xmin, xmax, ymin, ymax;
  //int npix, nunused;
  int n = dims[0], m = dims[1];
  //printf("m = %d, n = %d\n", m,n);

  for (int iter = 0; iter < 30; iter++){
    //printf("iter = %d\n", iter);
    det = *mxxold * *myyold - *mxyold * *mxyold;
    wxx = *myyold / det;
    wyy = *mxxold / det;
    wxy = -*mxyold /det;
    //printf("%d, %f, %f, %f, %f, %f\n", iter, *xc, *yc, *mxxold, *myyold, det);
    // Compute the window extension
    xmin = floor(*xc - sqrt(NSIGMA* *mxxold));
    xmax = ceil(*xc + sqrt(NSIGMA* *mxxold));
    if(xmax > m){
      xmax = m;
    }
    if(xmin < 0){
      xmin = 0;
    }
    
    ymin = floor(*yc - sqrt(NSIGMA * *myyold));
    ymax = ceil(*yc + sqrt(NSIGMA * *myyold));
    if(ymax > n){
      ymax = n;
    }
    if(ymin < 0){
      ymin = 0;
    }

    mxx = 0;
    myy = 0;
    mxy = 0;
    x1 = 0;
    y1 = 0;
    f = 0;
    //npix = 0;
    //nunused = 0;
    //printf("xmin=%d,xmax=%d,ymin=%d,ymax=%d\n", xmin, xmax, ymin, ymax);


    for (int y=ymin; y<ymax; y++){      
      for (int x=xmin; x<xmax; x++){
	int p = y* m + x;
	dx = x - *xc;
	dy = y - *yc;
	wg = wxx * dx * dx + wyy * dy * dy + 2 * wxy * dx * dy;
	// 4 sigmas
	if (wg > NSIGMA){
	  //nunused++;
	  continue;
	}
	wg = exp(-0.25 * wg) * data[p];
	mxx += wg * dx * dx;
	myy += wg * dy * dy;
	mxy += wg * dx * dy;
	f += wg;
	x1 += x * wg;
	y1 += y * wg;
      }
    }
    //printf("npix = %d, nused = %d\n", npix, npix-nunused);
    //printf("f = %f\n", f);
    mxx /= f;
    myy /= f;
    mxy /= f;
    x1 /= f;
    y1 /= f;
    //printf("%f, %f\n", x1, y1);

    if (fabs(mxx - *mxxold) + fabs(mxy - *mxyold) + fabs(myy - *myyold) < 1e-5){
      flag = 0;
      break;
    }
    if ((fabs(x1 - *xc) + fabs(y1 - *yc)) > 2)
      //shifting
      break;
    *mxxold = mxx > 0.25 ? mxx : 0.25;
    *myyold = myy > 0.25 ? myy : 0.25;
    *mxyold = mxy;
    *xc = x1;
    *yc = y1;
  }
  *mxxold = 2 * mxx;
  *myyold = 2 * myy;
  *mxyold = 2 * mxy;
  *xc = x1;
  *yc = y1;
  return flag;
}
