#ifndef IMM_SWAP_H
#define IMM_SWAP_H

#define imm_swap(a, b)                                                         \
  ({                                                                           \
    __typeof__(a) _t = (a);                                                    \
    (a) = (b);                                                                 \
    (b) = _t;                                                                  \
  })

#endif
