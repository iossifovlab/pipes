def run(proj,OG):
    OG.add("index","o",{})
    for i in range(5):
        OG.add("sample",str(i),{"bamFile":"/somewhere/sample%d.bam" % (i)},OG['index'])
    OG.add("report","o",{},OG['sample'] + OG['index'])
