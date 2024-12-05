#include <math.h>


double cap(double x1, double y1, double x2, double y2, double r){
  /*The area of a cap like this: |) 

    x1, y1 and x2,y2 are the coordinates of the 2 intersections
    between the circle and the segment and r is the radius of the circle
   */
  double d = sqrt((x2 - x1) * (x2 - x1) + (y2 - y1) * (y2 - y1));
  double theta = 2 * asin(0.5 * d / r);
  return 0.5 * r * r * (theta - sin(theta));
}

typedef struct aperture{
  double flux;
  double variance;
  double other;
  double bad;
} aperture;

aperture circular_aperture(double * f, double * variance, int * segmentation, long * dims, int id, double xc, double yc, double r){
  /*
    Sum pixel flux in a circular aperture of radius r > \sqrt{2}
    Assume pixels are unit squares.

    The condition r > \sqrt{2} is not checked for (it is done in the
    python wrapper though).
   */
  //printf("x, y = %f, %f\n", xc, yc);
  int n = dims[0], m = dims[1];
  double r2 = r * r;
  aperture ap = {0.,0.,0.,0.};
  int ymin = floor(yc - r);
  int ymax = ceil(yc + r);
  if (ymin < 0)
    ymin = 0;
  if (ymax >= n)
    ymax = n-1;
  //printf("%d <x<%d, %d<y<%d\n", xmin, xmax, ymin, ymax);
  
  for (int j = ymin; j <= ymax; j++){
    double y = fabs(j - yc);
    double xr = y - 0.5 > r? 0 : sqrt(r2 - (y - 0.5) * (y - 0.5));
    int xmin = floor(xc - xr)-1;
    int xmax = ceil(xc + xr)+1;
    if (xmin < 0)
      xmin = 0;
    if (xmax >= m)
      xmax = m-1;
    for (int i = xmin; i <= xmax; i++){
      // The problem has symetries
      double x1 = fabs(i - xc);
      double I = 0;
      double y1;
      if (x1 > y){
	y1 = x1+0.5;
	x1 = y+0.5;
      }else{
	y1 = y+0.5;
	x1 += 0.5;
      }
      
      if (x1 * x1 + y1 * y1 < r2){
	// Included entirely
	int p = j* m + i;
	ap.flux += f[p];
	if (variance[p] < __DBL_MAX__)
	  ap.variance += variance[p];
	else
	  ap.bad += f[p];
	if ((segmentation[p] != 0) && (segmentation[p] != id))
	  ap.other += f[p];
	  
	//flux += 1;
	//f[p] = 1;
      }
      else{
	double x0 = x1 - 1;
	double y0 = y1 - 1;
	if ((x0 > 0 ? x0 * x0 + y0 * y0 : y0 * y0) < r2){
	  // area above y1
	  if (y1 * y1 < r2){
	    double xinter = sqrt(r2 - y1 * y1);
	    if (xinter > x0){
	      double ya = y1;
	      double xstart = -xinter;
	      if (-xinter < x0){
		xstart = x0;
		ya = sqrt(r2 - x0 * x0);
	      }
	      I -= cap (xstart, ya, xinter, y1, r);
	      I -= (xinter - xstart) * 0.5 * (ya - y1);
	    }
	  }
	  // area above y0
	  {
	    double xinter = sqrt(r2 - y0 * y0);
	    double ya = y0;
	    double yb = y0;
	    if (x0 < -xinter)
	      x0 = -xinter;
	    else
	      ya = sqrt(r2 - x0 * x0);
	    if (x1 > xinter)
	      x1 = xinter;
	    else
	      yb = sqrt(r2 - x1 * x1);
	    I += cap(x0, ya, x1, yb, r);
	    I += (x1 - x0) * (0.5 *(ya + yb) - y0);
	    //double theta1 = acos(x0/r);
	    //double theta0 = acos(x1/r);
	    // area below y0

	    int p = j* m + i;
	    ap.flux += f[p] * I;
	    if (variance[p] < __DBL_MAX__)
	      ap.variance += variance[p] * I * I;
	    else
	      ap.bad += f[p] * I;
	    if (variance[p] == 0)
	      ap.bad += f[p] * I;
	    if ((segmentation[p] != 0) && (segmentation[p] != id))
	      ap.other += f[p] * I;
	    //flux += I;
	    //f[p] = I;
	  }
	}
      }
    }
  }
  return ap;
}
//printf("i,j=%d,%d,x0=%f, x1=%f, y0=%f, y1=%f\n", i, j, x0, x1, y0, y1);
//printf("xstart=%f, xinter=%f, %f, %f, %f\n", xstart, xinter, theta1, theta0, I);
