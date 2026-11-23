# lpa_kiv v4: consensus of KIV-2 A, B, C units, KIV-3 and KIV-1 (2026-11-23)

- `LPA_KIV_units112_aln.fa`: all 112 kringle-IV unit rows of the six v3 haplotype sets (72 KIV-2 A, 23 B, 3 C, 7 KIV-3,
  7 KIV-1), ungapped and realigned together with MAFFT v7 `--auto`; rows sorted by type. Units are cut in Chin 2022 phase:
  each row starts 1,743 bp before its own 160-bp exon 1, so the 182-bp exon near the row start is the previous kringle's exon 2.
- `LPA_KIV_consensus_ABC_aln.fa`: majority consensus of each type (gap-only columns removed): `cons_KIV2_A_n72`,
  `cons_KIV2_B_n23`, `cons_KIV2_C_n3`, `cons_KIV3_n7`, `cons_KIV1_n7`.
- `LPA_KIV_consensus_ABC.bed`: features per consensus row (ungapped coordinates): exon 1, exon-1 sites 14/41/86 with their
  bases, the A/B stretch (1,096 bp before exon 1 to site 41; 107 fixed A/B positions), the previous kringle's exon 2, and
  the oligos of the Lanktree "exon 4"/"exon 5" qPCR sets, the Innsbruck ddPCR set, the Kamstrup 2009 set, Design A2 and
  the A/B duplex assay (name suffix = mismatches, <= 2).
- `consensus_report.txt`, `make_consensus.py`: how it was made.
Differing consensus columns inside / outside the A/B stretch: A vs B 112 / 17; B vs KIV-3 0 / 1,394; B vs C 0 / 15; A vs C 112 / 20.
