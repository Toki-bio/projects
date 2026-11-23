"""Consensus rows for KIV-2 A, B, C units, KIV-3 and KIV-1 from the joint MAFFT alignment of 112 unit rows
(6 haplotype sets of github Toki-bio/projects lpa_kiv/v3). Writes:
  LPA_KIV_consensus_ABC_aln.fa  - 5 consensus rows (gap-only columns removed), units cut in Chin 2022 phase
  LPA_KIV_consensus_ABC.bed     - features on each consensus row (ungapped coordinates, BED chrom = row name)
  LPA_KIV_units112_aln.fa       - all 112 rows, sorted A, B, C, KIV-3, KIV-1 (for inspection)
  consensus_report.txt          - differing columns between consensus rows, site 14/41/86 bases, oligo hits"""
import collections, os
W = os.path.dirname(os.path.abspath(__file__))
rc = lambda s: s[::-1].translate(str.maketrans('ACGT-', 'TGCA-'))
rows = []
for l in open(os.path.join(W, 'units_all_aln.fa'), encoding='utf-8'):
    l = l.strip()
    if l.startswith('>'): rows.append([l[1:], ''])
    else: rows[-1][1] += l.upper()
def group(n):
    t = n.split('|')[1]
    t = t.replace('pat_', '').replace('mat_', '')
    if t.startswith('KIV2_'): return 'KIV2_' + t[-1]
    return t
G = collections.defaultdict(list)
for n, s in rows: G[group(n)].append(s)
order = ['KIV2_A', 'KIV2_B', 'KIV2_C', 'KIV3', 'KIV1']
L = len(rows[0][1])
def cons(seqs):
    out = []
    for c in range(L):
        cnt = collections.Counter(s[c] for s in seqs)
        out.append(cnt.most_common(1)[0][0])
    return ''.join(out)
C = {g: cons(G[g]) for g in order}
keep = [c for c in range(L) if any(C[g][c] != '-' for g in order)]
C2 = {g: ''.join(C[g][c] for c in keep) for g in order}
names = {'KIV2_A': 'cons_KIV2_A_n%d' % len(G['KIV2_A']), 'KIV2_B': 'cons_KIV2_B_n%d' % len(G['KIV2_B']),
         'KIV2_C': 'cons_KIV2_C_n%d' % len(G['KIV2_C']), 'KIV3': 'cons_KIV3_n%d' % len(G['KIV3']), 'KIV1': 'cons_KIV1_n%d' % len(G['KIV1'])}
with open(os.path.join(W, 'LPA_KIV_consensus_ABC_aln.fa'), 'w', encoding='utf-8') as w:
    for g in order:
        w.write('>' + names[g] + '\n')
        s = C2[g]
        for i in range(0, len(s), 80): w.write(s[i:i+80] + '\n')
with open(os.path.join(W, 'LPA_KIV_units112_aln.fa'), 'w', encoding='utf-8') as w:
    for g in order:
        for n, s in rows:
            if group(n) == g:
                w.write('>' + g + '|' + n.replace('|', '_') + '\n')
                for i in range(0, len(s), 80): w.write(s[i:i+80] + '\n')
# features
EX1 = 'CCAACATGTTTCTCTATGCTC'  # placeholder, replaced below by the real exon-1 start taken from Coassin's unit
ref = ''.join(l.strip() for l in open(os.path.join(W, '..', 'assays', 'kiv2_6.fasta'), encoding='utf-8') if not l.startswith('>')).upper()
exon1 = ref[580:740]; exon2 = ref[4743:4925]
OLIGOS = {
 'Lanktree_ex4_F': 'GTCAGGTGGGAGTACTGCAA', 'Lanktree_ex4_probe': 'CCTGACGCAATGCTCA', 'Lanktree_ex4_R': 'CGACGGCAGTCCCTTCTG',
 'Lanktree_ex5_F': 'GCACATACTCCACCACTGTCA', 'Lanktree_ex5_probe': 'CTTGGCAGGTTCTTCC', 'Lanktree_ex5_R': 'GCGAGTGTGGTGTCATAGATGA',
 'Innsbruck_F': 'GTGGCAGCTCCTTATTGTTATACG', 'Innsbruck_probe': 'TACTGCAACCTGACGCAATGCTCAGAC',
 'Kamstrup_F': 'ATCCAGATGCTGTGGCAGCT', 'Kamstrup_probe': 'CAACCTGACGCAATGC', 'Kamstrup_R': 'GCGACGGCAGTCCCTTCT',
 'A2_F': 'CCTAGTTCTATTGAGCAGAAG', 'A2_probe': 'AGGACCAGACACTTAGATTACCCTTCCA', 'A2_R': 'GTCTCCATTGACGTTTAGTTG',
 'AB_assay_F': 'TAATTCTCATAGACTCCTTTCTG', 'AB_assay_R': 'GTCGGTGCTGAAATGAAA',
 'AB_probe_A': 'CATGTTTCTCTATGCTC', 'AB_probe_B': 'CATATTTCGTTATTCTCA',
}
def find(u, q, maxmm=2):
    best = None
    for qq, strand in ((q, '+'), (rc(q), '-')):
        for i in range(len(u) - len(qq) + 1):
            mm = sum(a != b for a, b in zip(u[i:i+len(qq)], qq))
            if mm <= maxmm and (best is None or mm < best[2]): best = (i, i + len(qq), mm, strand)
    return best
rep = open(os.path.join(W, 'consensus_report.txt'), 'w', encoding='utf-8')
bed = open(os.path.join(W, 'LPA_KIV_consensus_ABC.bed'), 'w', encoding='utf-8')
colors = {'exon': '31,122,109', 'site': '160,82,122', 'stretch': '181,101,29', 'oligo': '90,110,170'}
# A/B differing alignment columns (consensus A vs consensus B)
diff = [k for k in range(len(C2['KIV2_A'])) if C2['KIV2_A'][k] != C2['KIV2_B'][k]]
rep.write('alignment columns (gap-only removed): %d\nA vs B consensus differing columns: %d (first %d, last %d)\n' % (len(C2['KIV2_A']), len(diff), diff[0] + 1, diff[-1] + 1))
for g in order:
    a = C2[g]; u = a.replace('-', '')
    col2u = {}; k = -1
    for c, ch in enumerate(a):
        if ch != '-': k += 1
        col2u[c] = k
    e1 = find(u, exon1, 8); e2 = find(u, exon2, 10)
    rep.write('\n%s ungapped %d bp; exon1 %s; exon2 %s\n' % (names[g], len(u), e1, e2))
    if e1:
        bed.write('%s\t%d\t%d\texon1_160bp\t0\t+\t%d\t%d\t%s\n' % (names[g], e1[0], e1[1], e1[0], e1[1], colors['exon']))
        for site in (14, 41, 86):
            p = e1[0] + site - 1
            bed.write('%s\t%d\t%d\tsite%d_%s\t0\t+\t%d\t%d\t%s\n' % (names[g], p, p + 1, site, u[p], p, p + 1, colors['site']))
            rep.write('  site %d = %s\n' % (site, u[p]))
    if e2: bed.write('%s\t%d\t%d\tprevious_kringle_exon2_182bp\t0\t+\t%d\t%d\t%s\n' % (names[g], e2[0], e2[1], e2[0], e2[1], colors['exon']))
    if g != 'KIV1' and e1:
        s0, s1 = e1[0] - 1096, e1[0] + 41   # documented A/B stretch: 1,096 bp before exon 1 to exon-1 site 41 (107 fixed positions)
        lab = 'A_B_stretch_107_sites' if g.startswith('KIV2') else 'KIV3_junction_stretch_identical_to_B'
        bed.write('%s\t%d\t%d\t%s\t0\t+\t%d\t%d\t%s\n' % (names[g], s0, s1, lab, s0, s1, colors['stretch']))
    for on, q in OLIGOS.items():
        f = find(u, q, 2)
        if f:
            bed.write('%s\t%d\t%d\t%s_mm%d\t0\t%s\t%d\t%d\t%s\n' % (names[g], f[0], f[1], on, f[2], f[3], f[0], f[1], colors['oligo']))
            rep.write('  %-20s mm %d at %d %s\n' % (on, f[2], f[0], f[3]))
        else:
            rep.write('  %-20s no match <= 2 mismatches\n' % on)
for x, y in (('KIV2_A', 'KIV2_C'), ('KIV2_B', 'KIV2_C'), ('KIV2_B', 'KIV3'), ('KIV2_A', 'KIV3'), ('KIV2_A', 'KIV1')):
    d = sum(1 for k in range(len(C2[x])) if C2[x][k] != C2[y][k])
    rep.write('\n%s vs %s differing columns: %d' % (x, y, d))
rep.write('\n')
rep.close(); bed.close()
print(open(os.path.join(W, 'consensus_report.txt'), encoding='utf-8').read())
