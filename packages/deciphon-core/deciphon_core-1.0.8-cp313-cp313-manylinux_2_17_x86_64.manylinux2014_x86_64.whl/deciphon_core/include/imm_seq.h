#ifndef IMM_SEQ_H
#define IMM_SEQ_H

#include "imm_compiler.h"
#include "imm_range.h"
#include "imm_str.h"

struct imm_abc;

struct imm_seq
{
  struct imm_str str;
  struct imm_abc const *abc;
};

// clang-format off
struct imm_seq        imm_seq_unsafe(struct imm_str, struct imm_abc const *);
int                   imm_seq_init(struct imm_seq *, struct imm_str, struct imm_abc const *);
struct imm_abc const *imm_seq_abc(struct imm_seq const *);
int                   imm_seq_size(struct imm_seq const *);
char const *          imm_seq_data(struct imm_seq const *);
int                   imm_seq_symbol_idx(struct imm_seq const *, int idx);
struct imm_seq        imm_seq_slice(struct imm_seq const *, struct imm_range);
// clang-format on

#endif
