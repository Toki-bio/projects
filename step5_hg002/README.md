# sineclose lr, plan step 5 part 2: HG002 fills against both parents (2026-11-27)

One plate per artificial gap in the HG002 Q100 v1.1 MATERNAL genome (public GIAB/HPRC data). Rows:
MAT = the removed maternal stretch with 2 kb maternal flanks (flanks lower case); PAT = the paternal sequence at the same place;
fill_default = lr's fill (one read's bases) between the maternal flanks; fill_consensus = the same with --read-consensus.
`artNNNN.aln.fa` (mafft --auto --preservecase), `artNNNN.bed` marks the removed stretch on the MAT row; `cases.tsv` gives each
case's class, pool size and edit distances (NM) of both fills to MAT and PAT.
