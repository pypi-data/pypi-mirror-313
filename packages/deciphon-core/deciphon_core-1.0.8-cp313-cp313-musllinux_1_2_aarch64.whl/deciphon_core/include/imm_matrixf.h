#ifndef IMM_MATRIXF_H
#define IMM_MATRIXF_H

#include "imm_compiler.h"

struct imm_matrixf
{
  float *data;
  int rows;
  int cols;
};

int imm_matrixf_init(struct imm_matrixf *, int rows, int cols);
void imm_matrixf_empty(struct imm_matrixf *);
void imm_matrixf_fill(struct imm_matrixf *, float);
float *imm_matrixf_get_ptr(struct imm_matrixf const *, int r, int c);
float const *imm_matrixf_get_ptr_c(struct imm_matrixf const *, int r, int c);
void imm_matrixf_cleanup(struct imm_matrixf *);
int imm_matrixf_resize(struct imm_matrixf *, int rows, int cols);

IMM_PURE float imm_matrixf_get(struct imm_matrixf const *x, int r, int c)
{
  return x->data[r * x->cols + c];
}

IMM_INLINE void imm_matrixf_set(struct imm_matrixf *x, int r, int c, float v)
{
  x->data[r * x->cols + c] = v;
}

#endif
