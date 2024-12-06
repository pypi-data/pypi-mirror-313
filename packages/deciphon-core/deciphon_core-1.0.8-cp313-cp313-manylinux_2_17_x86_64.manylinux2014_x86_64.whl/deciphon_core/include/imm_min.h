#ifndef IMM_MIN_H
#define IMM_MIN_H

#define imm_min(a, b)                                                          \
  ({                                                                           \
    __typeof__(a) _a = (a);                                                    \
    __typeof__(b) _b = (b);                                                    \
    _a < _b ? _a : _b;                                                         \
  })

#endif
