addi t1, zero, 2
addi t3,zero,2
slli t2, t1, 0x4
slli t4, t3, 0x5
fcvt.s.lu fa4, t1
fcvt.s.lu fa5, t2
fcvt.s.lu fa6, t4
fdiv.s fa5, fa5, fa4
fdiv.s fa6, fa6, fa4 //just repeat this
fdiv.s fa5, fa5, fa4
fdiv.s fa5, fa5, fa4
fdiv.s fa5, fa5, fa4
fcvt.lu.s t2, fa5, rtz
