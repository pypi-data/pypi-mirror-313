#ifndef IMM_CTRANS_H
#define IMM_CTRANS_H

#include "imm_static_assert.h"
#include <stdint.h>

struct imm_ctrans
{
  float score; /**< Transition score.  */
  int16_t src; /**< Source state.      */
  int16_t dst; /**< Destination state. */
};

imm_static_assert(sizeof(struct imm_ctrans) == 8, "");

#endif
