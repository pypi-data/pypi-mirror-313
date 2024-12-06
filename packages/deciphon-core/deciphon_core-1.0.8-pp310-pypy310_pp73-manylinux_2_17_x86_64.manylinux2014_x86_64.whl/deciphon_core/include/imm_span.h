#ifndef IMM_SPAN_H
#define IMM_SPAN_H

#include "imm_compiler.h"

struct imm_span
{
  int min;
  int max;
};

IMM_CONST struct imm_span imm_span(int min, int max)
{
  return (struct imm_span){min, max};
}

#endif
