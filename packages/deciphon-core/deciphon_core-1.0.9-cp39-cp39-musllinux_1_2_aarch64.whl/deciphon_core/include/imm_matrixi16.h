#ifndef IMM_MATRIXI16_H
#define IMM_MATRIXI16_H

#include "imm_compiler.h"
#include <stdint.h>

struct imm_matrixi16
{
  int16_t *data;
  int rows;
  int cols;
};

void imm_matrixi16_init(struct imm_matrixi16 *);
void imm_matrixi16_empty(struct imm_matrixi16 *);
void imm_matrixi16_set(struct imm_matrixi16 *, int r, int c, int16_t v);
void imm_matrixi16_cleanup(struct imm_matrixi16 *);
int imm_matrixi16_resize(struct imm_matrixi16 *, int rows, int cols);

IMM_PURE int16_t imm_matrixi16_get(struct imm_matrixi16 const *x, int r, int c)
{
  return x->data[r * x->cols + c];
}

#endif
