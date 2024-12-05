#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <stdio.h>


void minimap(double * data, int * segmap, long * dims, int nsidex, int nsidey, double * mean, double * std, int * num){
  int m, n, M, N;
  m = dims[0];
  n = dims[1];
  M = m/nsidex;
  N = n/nsidey;
  int k;
  double * sum = malloc(M*N *sizeof(double));
  double * squares = malloc(M*N *sizeof(double));
  //int * num = malloc(M*N *sizeof(int));
  memset(sum, 0., M*N *sizeof(double));
  memset(squares, 0., M*N *sizeof(double));
  //memset(num, 0, M*N *sizeof(int));
  double diff = 0;

  for (int i = 0; i < M; i++){
    for (int x = 0; x < nsidex; x++){
      for (int j = 0; j < N; j++){
	int K = i*N + j;
	k = i*nsidex * n + j * nsidey + x*n;
	for(int y = 0; y < nsidey; y++){
	  double toto = segmap[k] == 0 ? (num[K]++,data[k]): 0;
	  sum[K] += toto;
	  squares[K] += toto * toto;
	  k++;
	}
      }
    }
  }

  while(1){
    int converged = 1;
    for(k = 0; k < M*N; k++){
      mean[k] = sum[k] / num[k];
      diff = std[k];
      std[k] = 3 * sqrt(squares[k] / num[k] - mean[k] * mean[k]);
      sum[k] = 0;
      squares[k] = 0;
      if ((num[k] >2) && (fabs(diff / std[k] - 1) > 1e-3))
	converged = 0;
      num[k] = 0;
    }
    if (converged)
      break;

    for (int i = 0; i < M; i++){
      for (int x = 0; x < nsidex; x++){
	for (int j = 0; j < N; j++){
	  int K = i*N + j;
	  k = i*nsidex * n + j * nsidey + x*n;
	  for(int y = 0; y < nsidey; y++){
	    double toto = (segmap[k] == 0) && (fabs(data[k] - mean[K]) < std[K]) ? (num[K]++,data[k]): 0;
	    sum[K] += toto;
	    squares[K] += toto * toto;
	    k++;
	  }
	}
      }
    }
  }
  free(sum);
  free(squares);
}
