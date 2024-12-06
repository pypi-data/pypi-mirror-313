#ifndef IMM_ESEQ_H
#define IMM_ESEQ_H

#include "imm_code.h"
#include "imm_compiler.h"
#include "imm_matrixi16.h"

struct imm_abc;
struct imm_code;
struct imm_seq;

struct imm_eseq
{
  struct imm_matrixi16 data;
  struct imm_code const *code;
};

void                  imm_eseq_init(struct imm_eseq *, struct imm_code const *);
void                  imm_eseq_cleanup(struct imm_eseq *);
struct imm_abc const *imm_eseq_abc(struct imm_eseq const *);
int                   imm_eseq_size(struct imm_eseq const *);
int                   imm_eseq_setup(struct imm_eseq *, struct imm_seq const *);
struct imm_eseq       imm_eseq_slice(struct imm_eseq const *, struct imm_range);

IMM_PURE int imm_eseq_get(struct imm_eseq const *x, int pos, int size,
                          int min_seq)
{
  int16_t val = imm_matrixi16_get(&x->data, pos, size);
  return imm_code_translate(x->code, val, min_seq);
}

#endif
