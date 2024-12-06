#ifndef IMM_LOGADDEXP_H
#define IMM_LOGADDEXP_H

#include "imm_compiler.h"

/* For Windows. */
#define _USE_MATH_DEFINES

#include <float.h>
#include <math.h>

#ifndef M_LN2
#define M_LN2 0.69314718055994530942 /* log_e 2 */
#endif

/* Computes ㏒ₑ(𝑒ˣ + 𝑒ʸ) in a safe and accurate way.
 *
 * For example, `log(exp(1e3) + exp(-INFINITY))` will likely overflow,
 * while `logaddexp(1e3, -INFINITY)` will return `1e3`.
 */
IMM_CONST float imm_logaddexp(float x, float y)
{
  float const tmp = x - y;

  if (x == y) return (float)(x + M_LN2);

  if (tmp > 0) return x + log1pf(expf(-tmp));
  else if (tmp <= 0) return y + log1pf(expf(tmp));

  return tmp;
}

#endif
