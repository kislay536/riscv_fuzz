addi t1, zero, 2
slli t2, t1, 0x4
fcvt.s.lu fa4, t1
fcvt.s.lu fa5, t2
fdiv.s fa5, fa5, fa4
fdiv.s fa5, fa5, fa4
fdiv.s fa5, fa5, fa4
fdiv.s fa5, fa5, fa4
fcvt.lu.s t2, fa5, rtz
