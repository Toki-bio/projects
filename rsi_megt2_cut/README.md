# *Rhinolophus sinicus* MEG-T2: the copies the new per-consensus score cut drops

SINEderella's reproducibility fix (branch `reproducible`, 2026-11-21) replaced `ssearch36 -z 11`
(clock-seeded shuffled statistics) with `-z 3` fixed Altschul-Gish statistics plus a per-consensus
score cut computed from 2000 seeded shuffled genome windows (`tools/shuffle_cut.py`).
For MEG-T2 the applied cut is **75.8 bits** (step1 log of the new run).

Two full *R. sinicus* runs on the same genome and the same 21-consensus bank:

| | run | MEG-T2 loci with verdict SINE |
|---|---|---|
| old | `rsi_final_20261102/run_20261101_235602` (main f2457a8) | 94 |
| new | `repro/rsi_full/B/run_20261123_072054` (fixed code) | 10 |

**84 loci** that the old run called MEG-T2 / SINE are absent from the new run altogether — they are
below the new cut at the search step, so they never reach assignment.
All 84 carry flankscan stage-9 status `unique` on both sides in the old run (the owner's
unique-flanks gate); none were excluded.

**Open in ViewAlign:**
https://toki-bio.github.io/MSA-viewer/?url=https%3A%2F%2Fraw.githubusercontent.com%2FToki-bio%2Fprojects%2Fmain%2Frsi_megt2_cut%2Frsi_MEG-T2_cut_aln.fa&bed=https%3A%2F%2Fraw.githubusercontent.com%2FToki-bio%2Fprojects%2Fmain%2Frsi_megt2_cut%2Frsi_MEG-T2_cut.bed&title=rsi%20MEG-T2%20dropped%20by%20the%20new%20score%20cut

Files
- `rsi_MEG-T2_cut_aln.fa` — 95 rows, 686 columns. Row 1 is the MEG-T2 bank consensus (232 bp);
  then the 10 copies the new code **keeps** and the 84 it **drops**. Row name carries the group,
  the new-scale bit score, its distance from the 75.8-bit cut, the old-scale bit score and the locus.
  Element uppercase, 100 bp upstream + 120 bp downstream flank lowercase, degapped and packed
  against the copy's own first/last element base.
- `rsi_MEG-T2_cut.bed` — the element span of every row in that row's own ungapped coordinates.
- `scores.tsv` — locus, group, new-scale bits, distance from the cut, old-scale bits.

Scores (bit scores on the two scales are **not** comparable: `-z 3` runs about 2.1-2.3x the fitted
`-z 11` values)

| group | n | new-scale bits (cut 75.8) | old-scale bits |
|---|---|---|---|
| kept | 10 | 76.2 - 86.3 | 37.5 - 41.8 |
| dropped | 84 | 67.9 - 75.7 | 34.1 - 37.5 |

The highest-scoring dropped copy is 0.1 bit below the cut. *R. sinicus* genome: GCF_001017535
(public).

How the plate was built: locus spans from the old run's `loci_verdict.tsv`; flanks 50+50 up / 70+50
down, the step8a base plus the step7 `general` confirmed boundary; `mafft --localpair --maxiterate
1000 --ep 0.123 --nuc --reorder --preservecase` (SubFam's own final command, never `--add`);
consensus forced back to row 1; flanks justified by the `postprocess_flanks` rule
(`disc/fix_alignments.justify`) with each row's own element boundary. New-scale scores are
`ssearch36 -g -3 -Q -n -z 3 -w 95 -W 70 -m 8` of the MEG-T2 consensus against each copy, the same
settings the new `sear` uses; the 10 kept copies reproduce the new run's own recorded scores to
within 0.1 bit.
