#ifndef IMM_ZSPAN_H
#define IMM_ZSPAN_H

#include "imm_assume.h"
#include "imm_compiler.h"
#include "imm_range.h"
#include "imm_state.h"
#include <stdbool.h>
#include <stdint.h>

IMM_CONST int8_t imm_zspan(int min, int max)
{
  imm_assume(min <= IMM_STATE_MAX_SEQSIZE);
  imm_assume(max <= IMM_STATE_MAX_SEQSIZE);
  return (int8_t)((min << 4) | max);
}

IMM_CONST int_fast8_t imm_zspan_min(int8_t x) { return (int_fast8_t)(x >> 4); }

IMM_CONST int_fast8_t imm_zspan_max(int8_t x) { return (int_fast8_t)(x & 0xF); }

IMM_CONST struct imm_range imm_zspan_range(int8_t x)
{
  return imm_range(imm_zspan_min(x), imm_zspan_max(x) + 1);
}

#endif
