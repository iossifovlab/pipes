add_targets("ns.bam", \
            "fixmate.bam", \
            "cs.bam", \
            "mdup.bam", "mdup.bam.bai", \
            "coverage.png")

rule merge:
  input:
    DT("sample_ns.bam")
  output:
    T("ns.bam")
  conda:
    "envs/bwa.yaml"
  log:
    **(LFS("ns.bam"))
  shell:
    "samtools merge -n {output} {input} 2>{log.E}"

rule fixmate:
  input:
    T("ns.bam")
  output:
    T("fixmate.bam")
  params:
    ref=PP("ref")
  conda:
    "envs/bwa.yaml"
  log:
    **(LFS("fixmate.bam"))
  shell:
    "samtools fixmate -m --reference {params.ref} -O bam {input} {output} 2>{log.E}"

rule sample_cs:
  input:
    T("fixmate.bam")
  output:
    T("cs.bam")
  conda:
    "envs/bwa.yaml"
  log:
    **(LFS("cs.bam"))
  shell:
    "samtools sort -T {input} -O bam {input} > {output} 2>{log.E}"

rule markdup:
  input:
    T("cs.bam")
  output:
    T("mdup.bam")
  params:
    ref = PP("ref")
  conda:
    "envs/bwa.yaml"
  log:
    **(LFS("mdup.bam"))
  shell:
    "samtools markdup -T {input} -O bam -s --reference {params.ref} {input} {output} 2>{log.E}"

rule sample_idx:
  input:
    T("mdup.bam")
  output:
    T("mdup.bam.bai")
  conda:
    "envs/bwa.yaml"
  shell:
    "samtools index -b {input} {output}"

rule depth:
  input:
    bam=T("mdup.bam"),
    idx=T("mdup.bam.bai")    
  output:
    T("depth.txt")
  conda:
    "envs/bwa.yaml"
  params:
    target=PP("target"),
    ref = PP("ref")
  shell:
    "samtools depth -b {params.target} -q 30 -Q 30 {input.bam} > {output}"

rule sample_plot:
  input:
    T("depth.txt")
  output:
    T("coverage.png")
  log:
    **(LFS("coverage.png"))
  shell:
    "coveragePlot.py {wildcards.oid} {output} {input} 2>{log.E}"

rule clean_sample:
  shell:
    "cd sample; for n in *; do (cd $n; rm -rf *) done"
