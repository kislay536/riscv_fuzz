addi t1, zero, 2        # t1 = 2
slli t2, t1, 0x4        # t2 = t1 << 5 (shift left by 5 places)
fcvt.s.lu fa4, t1       # Convert t1 to float and store in fa4
fcvt.s.lu fa5, t2       # Convert t2 to float and store in fa5
fdiv.s fa5, fa5, fa4    # fa5 = fa5 / fa4
fdiv.s fa5, fa5, fa4    # fa5 = fa5 / fa4
fdiv.s fa5, fa5, fa4    # fa5 = fa5 / fa4
fdiv.s fa5, fa5, fa4    # fa5 = fa5 / fa4
fcvt.lu.s t2, fa5, rtz  # Convert fa5 to integer (round towards zero) and store in t2
