#ifndef IMM_ASSUME_H
#define IMM_ASSUME_H

#include "imm_compiler.h"

#if IMM_HAS_BUILTIN(__builtin_assume)
#define imm_assume(x) __builtin_assume(x)
#else
#define imm_assume(x)                                                          \
  do                                                                           \
  {                                                                            \
    if (!(x)) IMM_UNREACHABLE();                                               \
  } while (0);
#endif

#endif
