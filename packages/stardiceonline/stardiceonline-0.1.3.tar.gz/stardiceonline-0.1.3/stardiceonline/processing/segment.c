//#include "inpaint.h"
#include <stdlib.h>
#include <stdio.h>
#include <assert.h>
#define STACKSIZE 2000000

/**
 * Flag all the connected pixels with flux above the isophotal,
 * starting at position k.
 * Mask data.
 */
void neig_nr(double * data, int * segmap, long * dims, int k, double isophot, int flag){
  int * stack_start = malloc(STACKSIZE * sizeof(int));
  int * stack = stack_start;
  int * stack_end = stack_start + STACKSIZE - 8;
  int m = dims[0], n = dims[1]; 
  int i, j;
  *(stack++) = k;
  while (stack != stack_start){
    if (stack >= stack_end){
      free(stack_start);
      printf("An object exceeded the size of the segmentation stack (%d pixels). Trouble ahead.\n", STACKSIZE);
      return;
    }
    k = *(--stack);
    if (segmap[k] != 0)
      continue;
    else if (data[k] > isophot){
      data[k] = 0;
      segmap[k] = flag;
      i = k / n;
      j = k % n;
      if(i+1 < m){
        *(stack++) = (i+1)*n + j;
        if (j+1 < n)
          *(stack++) = (i+1)*n + j+1;
        if (j-1 >= 0)
          *(stack++) = (i+1)*n + j-1;
      }
      if (j+1 < n)
        *(stack++) = i*n + j+1;
      if (j-1 >= 0)
        *(stack++) = i*n + j-1;
      if(i-1 >= 0){
        *(stack++) = (i-1)*n + j;
        if (j+1 < n)
          *(stack++) = (i-1)*n + j+1;
        if (j-1 >= 0)
          *(stack++) = (i-1)*n + j-1;
      }
    }
  }
  free(stack_start);
}


/**
 * Simple segmentation algorithm.
 *
 * data: a n x m image.
 * segmap: the resulting segmentation map.
 */
int segment(double * data, int * segmap, long * dims, double threshold, double isophot){
  int m, n, nPix;
  m = dims[0];
  n = dims[1];
  nPix = m*n;
  int k;
  int star = 0;
  for (k = 0; k < nPix; k++){
    if (data[k] > threshold){
      star++;
      neig_nr(data, segmap, dims, k, isophot, star);
    }
  }
  return star;
}


/**
 * Same as neig_nr but return flux, isophotal area and pixel list in
 * addition.
 */
int neig_nr_full(double * data, int * segmap, int * pixlist, long * dims, int k, double isophot, int flag, double * flux){
  int * stack_start = malloc(STACKSIZE * sizeof(int));
  int * stack = stack_start;
  int * stack_end = stack_start + STACKSIZE - 8;
  int m = dims[0], n = dims[1]; 
  int i, j;
  int isoarea = 0;
  *flux = 0;
  *(stack++) = k;
  while (stack != stack_start){
    if (stack >= stack_end){
      free(stack_start);
      return isoarea;
    }
    k = *(--stack);
    if (segmap[k] == flag)
      continue;
    else if (data[k] > isophot){
      //data[k] = 0;
      segmap[k] = flag;
      isoarea++;
      *flux += data[k];
      *(pixlist++) = k;
      i = k / n;
      j = k % n;
      if(i+1 < m){
        *(stack++) = (i+1)*n + j;
        if (j+1 < n)
          *(stack++) = (i+1)*n + j+1;
        if (j-1 >= 0)
          *(stack++) = (i+1)*n + j-1;
      }
      if (j+1 < n)
        *(stack++) = i*n + j+1;
      if (j-1 >= 0)
        *(stack++) = i*n + j-1;
      if(i-1 >= 0){
        *(stack++) = (i-1)*n + j;
        if (j+1 < n)
          *(stack++) = (i-1)*n + j+1;
        if (j-1 >= 0)
          *(stack++) = (i-1)*n + j-1;
      }
    }
  }
  free(stack_start);
  return isoarea;
}

int deblend_tree(double * data, int * levelmap, int * pixList, long * dims, int nPix, double * levels, int level, int nlevel, double fluxmin, int n_source, int* segmap){
  int k, p;
  int * subpixlist = malloc(nPix * sizeof(int));
  int isoar;
  double flux = 0;
  double l = levels[level];
  int n_sub_sources;
  if ((nPix < 2) || (level == nlevel)){
    free(subpixlist);
    return 0;
  }
  for (k = 0; k < nPix; k++){
    n_sub_sources = 0;
    p = pixList[k];
    if ((levelmap[p] < level) && (data[p] > l)){
      isoar = neig_nr_full(data, levelmap, subpixlist, dims, p, l, level, &flux);
      if (isoar > nPix)
	printf("Es stink\n");
      if (flux > fluxmin){
	n_sub_sources = deblend_tree(data, levelmap, subpixlist, dims, isoar, levels, level + 1, nlevel, fluxmin, n_source, segmap);
	if (n_sub_sources - n_source < 2){
	   n_source++;
	   for(int i=0; i<isoar; i++)
	     segmap[subpixlist[i]] = n_source;
	}
	else{
	  n_source = n_sub_sources;
	}
      }
    }
  }
  free(subpixlist);
  return n_source;
}
