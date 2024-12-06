#ifndef IMM_PAIR_H
#define IMM_PAIR_H

#include "imm_static_assert.h"
#include <stdint.h>

struct imm_pair
{
  struct
  {
    union
    {
      struct
      {
        uint16_t src;
        uint16_t dst;
      };
      uint32_t key;
    };
  } id;

  struct
  {
    struct
    {
      int16_t src;
      int16_t dst;
    };
  } idx;
};

imm_static_assert(sizeof(struct imm_pair) == 8, "struct pair must be packed");

struct imm_pair imm_pair(int src_id, int dst_id);

#endif
