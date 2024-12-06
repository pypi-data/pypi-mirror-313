#ifndef IMM_CELL_H
#define IMM_CELL_H

#include "imm_compiler.h"
#include <stdint.h>

struct imm_cell
{
  int row;
  int_fast16_t state_idx;
  int_fast8_t emission_size;
};

IMM_CONST struct imm_cell imm_cell(int row, int_fast16_t state_idx,
                                   int_fast8_t emissize)
{
  return (struct imm_cell){
      .row = row, .state_idx = state_idx, .emission_size = emissize};
}

#endif
