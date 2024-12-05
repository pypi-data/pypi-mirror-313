#include <stdlib.h>
#include <stdio.h>
/**
 * Fill holes in image by diffusing the border in the holes
 * data: a n x m image.
 * mask: the list of the nhole pixels to inpaint.
 */
void inpaint(double * data, int * mask, long * dims, int nhole, double moff){
  int m, n, n_it=0;
  m = dims[0];
  n = dims[1];
  double * tmp = malloc(sizeof(double)*nhole);
  double delta_max = 2*moff;
  //int pmax = 0;
  int p;
  printf("%d pixels to be filled\n",nhole);
  for (p = 0 ; p < nhole ; p++){
    int k = mask[p];
    tmp[p] = data[k];
  }
  
  while (delta_max > moff){ 
    n_it++;
    for (p = 0 ; p < nhole ; p++){
      int k = mask[p];
      tmp[p] = 0.2 * data[k];
      int i = k/n;
      int j = k%n;
      if (i+1 < m)
	tmp[p] += 0.2 * data[(i+1)*n+j];
      if (i>0)
	tmp[p] += 0.2 * data[(i-1)*n+j];
      if (j+1 < n)
	tmp[p] += 0.2 * data[i*n+j+1];
      if (j > 0)
	tmp[p] += 0.2 * data[i*n+j-1];
    }
    delta_max = 0;
    for (p = 0 ; p < nhole ; p++){
      int k = mask[p];
      if (abs(data[k] - tmp[p]) > delta_max){
	delta_max = abs(data[k] - tmp[p]);
	//pmax = p;
      }
      data[k] = tmp[p];
    }
  }
  printf("maximal evolution after %d iterations:%.2g\n", n_it, delta_max);
  free (tmp);
}
