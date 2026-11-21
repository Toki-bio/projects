# SRY in Eulipotyphla (public rows)

Multiple alignment of SRY (ORF ± 200 bp where available) in moles, desmans, shrews, hedgehogs and *Solenodon*, with human as outgroup.
46 rows, 1,444 columns, MAFFT L-INS-i (`mafft --localpair --maxiterate 1000`, input order).

**Open in ViewAlign:**
https://toki-bio.github.io/MSA-viewer/?url=https%3A%2F%2Fraw.githubusercontent.com%2FToki-bio%2Fprojects%2Fmain%2Fsry_eulipotyphla%2FSRY_Eulipotyphla_public_aln.fa&bed=https%3A%2F%2Fraw.githubusercontent.com%2FToki-bio%2Fprojects%2Fmain%2Fsry_eulipotyphla%2FSRY_Eulipotyphla_public.bed&title=SRY%20Eulipotyphla

Files
- `SRY_Eulipotyphla_public_aln.fa`: the alignment. Row names: family | species | accession | locus/notes (orf = ORF position in the row, sex = sex of the sequenced individual as deposited).
- `SRY_Eulipotyphla_public.bed`: annotations in each row's own ungapped coordinates (ORF, HMG box, primers, span of the published 154-bp desman fragment).

Sources: NCBI assemblies and GenBank entries named in each row. *Atelerix albiventris* row = consensus of public male WGS reads SRR12697342 (156-aa ORF, intact HMG box; 100 % identical to the 1996 fragment X90866).

Notes
- The 1996 *Neomys anomalus* and *Crocidura suaveolens* fragments (X90864, X90865) are identical to mole SRY, not to the shrew SRY found in 10 shrew genomes, and are likely carry-over.
- Unpublished sequences used in the full working alignment are not included here.
