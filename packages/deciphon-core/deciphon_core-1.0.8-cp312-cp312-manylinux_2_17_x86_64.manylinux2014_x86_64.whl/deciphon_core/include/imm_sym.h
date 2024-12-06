#ifndef IMM_SYM_H
#define IMM_SYM_H

#include "imm_compiler.h"
#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

enum imm_sym_type
{
  IMM_SYM_NULL = 0,
  IMM_SYM_NORMAL = 1,
  IMM_SYM_ANY = 2,
};

#define IMM_SYM_FIRST_CHAR '!'
#define IMM_SYM_LAST_CHAR '~'

#define IMM_SYM_NULL_ID INT8_MAX
#define IMM_SYM_NULL_IDX INT8_MAX

#define IMM_SYM_ID(c) ((int)(c - IMM_SYM_FIRST_CHAR))
#define IMM_SYM_CHAR(x) ((char)(x + IMM_SYM_FIRST_CHAR))

#define IMM_SYM_SIZE ((IMM_SYM_LAST_CHAR - IMM_SYM_FIRST_CHAR) + 1)

struct imm_sym
{
  int8_t idx[IMM_SYM_SIZE];
};

// clang-format off
void imm_sym_init(struct imm_sym *);
int  imm_sym_id(char c);
char imm_sym_char(int id);
int  imm_sym_idx(struct imm_sym const *, int id);
void imm_sym_set_idx(struct imm_sym *, int id, int idx);
bool imm_sym_valid_char(char c);
bool imm_sym_valid_id(int id);
// clang-format on

#endif
