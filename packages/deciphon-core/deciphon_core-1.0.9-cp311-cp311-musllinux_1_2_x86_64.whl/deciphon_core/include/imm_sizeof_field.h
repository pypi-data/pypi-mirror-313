#ifndef IMM_SIZEOF_FIELD_H
#define IMM_SIZEOF_FIELD_H

/**
 * imm_sizeof_field() - Report the size of a struct field in bytes
 *
 * @TYPE: The structure containing the field of interest
 * @MEMBER: The field to return the size of
 */
#define imm_sizeof_field(TYPE, MEMBER) sizeof((((TYPE *)0)->MEMBER))

#endif
