#ifndef IMM_ARRAY_SIZE_FIELD_H
#define IMM_ARRAY_SIZE_FIELD_H

#include "imm_sizeof_field.h"

#define imm_array_size_field(T, M)                                             \
  (imm_sizeof_field(T, M) / sizeof(((((T *)0)->M))[0]))

#endif
