add_targets("a.txt", "b.txt", "t.txt")

rule build_a:
  output:
     t = T("t.txt")
  log:  **(LFS('t.txt'))
  shell:
    "(time touch {output.t} \
           > {log.O}  \
           2> {log.E} \
     ) 2> {log.T}"

rule build_ab:
  output:
    T("a.txt"), T("b.txt")
  log:  **(LFS('b.txt'))
  shell:
    "touch {output[0]}; "
    "touch {output[1]}; "

