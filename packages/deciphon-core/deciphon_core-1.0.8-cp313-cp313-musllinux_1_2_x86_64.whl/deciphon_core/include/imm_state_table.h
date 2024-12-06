#ifndef IMM_STATE_TABLE_H
#define IMM_STATE_TABLE_H

#include "imm_assume.h"
#include "imm_compiler.h"
#include "imm_range.h"
#include "imm_state.h"
#include "imm_zspan.h"
#include <stdint.h>

struct imm_dp_cfg;

struct imm_state_table
{
  int nstates;
  uint16_t *ids;
  int16_t start_state_idx;
  int16_t end_state_idx;
  int8_t *span;

  // Debugging purpose
  struct
  {
    imm_state_name *state_name;
  } debug;
};

void imm_state_table_init(struct imm_state_table *);
void imm_state_table_debug_setup(struct imm_state_table *, imm_state_name *);
void imm_state_table_cleanup(struct imm_state_table *);
int imm_state_table_reset(struct imm_state_table *, struct imm_dp_cfg const *);
int imm_state_table_idx(struct imm_state_table const *, int id);
char *imm_state_table_name(struct imm_state_table const *, int idx);
int imm_state_table_id(struct imm_state_table const *, int idx);
struct imm_range imm_state_table_range(struct imm_state_table const *, int idx);
void imm_state_table_dump(struct imm_state_table const *, FILE *restrict);

IMM_PURE int8_t imm_state_table_zspan(struct imm_state_table const *x,
                                      int state_idx)
{
  return x->span[state_idx];
}

#endif
