#ifndef IMM_LOGSUM_H
#define IMM_LOGSUM_H

#define logsum_nargs(...) (sizeof((int[]){__VA_ARGS__}) / sizeof(int))

#define logsum(...)                                                            \
  imm_lprob_sum(logsum_nargs(__VA_ARGS__),                                     \
                (float[logsum_nargs(__VA_ARGS__)]){__VA_ARGS__})

#endif
