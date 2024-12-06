#ifndef IMM_IPOW_H
#define IMM_IPOW_H

#include "imm_compiler.h"

IMM_CONST long imm_ipow(long const x, int const e)
{
  // TODO: use our own assertion instead (to avoid #include <assert.h>)
  // assert(e >= 0);
  long r = 1;
  long xx = x;
  int ee = e;
  do
  {
    if (ee & 1) r *= xx;
    ee >>= 1;
    xx *= xx;
  } while (ee);
  return r;
}

#endif
