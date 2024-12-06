#ifndef IMM_CODE_H
#define IMM_CODE_H

#include "imm_compiler.h"
#include "imm_state.h"
#include <stdint.h>

struct imm_abc;
struct imm_code;
struct imm_seq;

struct imm_code
{
  int16_t offset[IMM_STATE_MAX_SEQSIZE + 2];
  int16_t stride[IMM_STATE_MAX_SEQSIZE];
  struct imm_abc const *abc;
};

void imm_code_init(struct imm_code *, struct imm_abc const *);
int imm_code_encode(struct imm_code const *, struct imm_seq const *);

IMM_PURE int imm_code_translate(struct imm_code const *x, int value,
                                int min_seq)
{
  // TODO: use our own assertion instead (to avoid #include <assert.h>)
  /* assert(value >= x->offset[min_seq]); */
  return value - x->offset[min_seq];
}

IMM_PURE int imm_code_size(struct imm_code const *x, struct imm_span span)
{
  return x->offset[span.max + 1] - x->offset[span.min];
}

#endif
