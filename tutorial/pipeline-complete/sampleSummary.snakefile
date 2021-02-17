add_targets("coverage.png")

rule summary_plot:
  input:
    DT("depth.txt")
  output:
    T("coverage.png")
  log:
    **(LFS("coverage.png"))
  shell:
    "$SO_PIPELINE/coveragePlot.py 'Sample Summary Plot' {output} {input} 2>{log.E}"