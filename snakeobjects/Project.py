import os,sys,yaml,re
from pathlib import Path
import importlib.resources as importlib_resources
from snakeobjects.ObjectGraph import ObjectGraph, load_object_graph


def load_yaml_with_envirnomemnt_interpolation(file_name):

    CF = open(file_name, 'r')
    config = yaml.safe_load(CF)
    CF.close()

    ptn = re.compile(r'(^\[E\:)(.*)(\])')

    for k,v in config.items():
        if type(v) != str:
            continue
        m = ptn.match(v)
        if m:
            s = m.span()
            name = m.groups(0)[1]
            n = os.environ[name]
            if n:
                config[k] = v.replace(v[s[0]:s[1]],n)
            else:
                print('Varianble %s is not defined' % name, file=sys.stderr)
                exit(1) 
    return config  

def find_so_project_directory():
    """     
    Determines the direcotry for the current snakeobject project.
    
    Several approaches are attempted and the first suitable directory found 
    is returned. If everything fails, the current working directory is returned.

    1. If the SO_PROJECT envirnoment variable exits, its values is returned.
    2. If the current working directory contains a file named so_project.yaml, 
       the current working direcoty is returned.
    3. The partents of the current working directory are examined recursivelly 
       and the first one containing so_project.yaml file is returned. 
    """
    if "SO_PROJECT" in os.environ:
        return os.environ["SO_PROJECT"]
    cw = Path(os.getcwd())
    for d in [cw] + list(cw.parents):
        if os.path.isfile(d / "so_project.yaml"):
            return str(d)
    return os.getcwd()

class Project:
    """
        Each objects of the Project class represents a snakeobject project. 
        
        The project directory is given as the ``directory`` parameter. If ``direcotry`` is none,
        the :py:func:`find_project_directory` function is used to determine the project directory.

        A snakeobject project attributes are:

        * ``directory``, the project directory 
        * ``parameters``, a key value dictionalry for global project lelvel parameters.
        * ``objectGraph``, the objectGraph for the project
    """

    def __init__(self,directory=None):
        self.directory = directory if directory else find_so_project_directory()
        self._porojectFileName = self.directory + "/so_project.yaml"
        self._objectGraphFileName = self.directory + "/objects/.snakeobjects/OG.json"

        if os.path.isfile(self._porojectFileName):
            self.parameters = load_yaml_with_envirnomemnt_interpolation(self._porojectFileName)
        else:
            self.parameters = {}

        if os.path.isfile(self._objectGraphFileName):
            self.objectGraph = load_object_graph(self._objectGraphFileName)
        else:
            self.objectGraph = ObjectGraph()

    def get_pipeline_directory(self):
        if "so_pipeline" in self.parameters:
            ppd = self.parameters['so_pipeline']
            if not os.path.isabs(ppd):
                ppd = self.directory + "/" + ppd
        elif "SO_PIPELINE" in os.environ:
            ppd = os.environ['SO_PIPELINE']
        else:
            ppd = self.directory
        return os.path.abspath(ppd)


    def prepare(self, newObjectGraph, ARGV=None):

        if not ARGV: ARGV = sys.argv 
        cmd = 'prepareTest' if len(ARGV) < 2 else ARGV[1]

        if cmd == 'prepareTest':
            print("Current graph stats")
            print("+++++++++++++++++++")
            self.objectGraph.print_stats()
            print("\n")
            print("New graph stats")
            print("+++++++++++++++")
            newObjectGraph.print_stats()
        elif cmd == 'prepare':
            self.objectGraph = newObjectGraph 
            self.prepare_objects()
        else:
            print(f"unkown command {cmd}. The known commands are 'prepareTest' and 'prepare'")

    def prepare_objects(self):
        os.chdir(self.directory)
        os.system("mkdir -p objects/.snakeobjects")
        self.objectGraph.save("objects/.snakeobjects/OG.json")
        self.write_main_snakefile()
        self.create_object_directories()

    def ensure_object_type_snakefile_exists(self,ot):
        sfile = self.get_pipeline_directory() + "/" + ot + ".snakefile"
        if not os.path.exists(sfile): 
            with open(sfile, 'w') as f:
                f.write(f'rule {ot}:\n')
                f.write(f'  input:\n')
                f.write(f'    DT("obj.flag")\n') 
                f.write(f'  output:\n') 
                f.write(f'    touch(T("obj.flag"))\n\n')
        return sfile
        
    def write_main_snakefile(self):
        mf=self.directory+'/objects/.snakeobjects/main.snakefile'

        header = importlib_resources.read_text(__package__,'header.snakefile')
        with open(mf, 'w') as f:
            f.write(header)

            for ot in self.objectGraph.get_object_types():
               
                sfile = self.ensure_object_type_snakefile_exists(ot) 

                f.write(f'include: "{sfile}"\n')
                f.write(f'rule all_{ot}:\n')
                f.write(f'  input:\n')
                f.write(f'    expand("{{of}}", of=project.get_all_object_flags("{ot}"))\n\n')

    def get_object_flag(self,o):
        return f'{o.type}/{o.name}/obj.flag'

    def get_object_directory(self,o):
        return f'{self.directory}/objects/{o.type}/{o.name}'

    def create_object_directories(self):
        for tp in sorted(self.objectGraph.get_object_types()):
            for o in self.objectGraph[tp]:
                oDir = self.get_object_directory(o)

                logDir = oDir + "/log"
                if not os.path.exists(logDir):
                    os.makedirs(logDir)

                for k,v in list(o.params.items()):
                    if not k.startswith("symlink."):
                        continue
                    dst = oDir + "/" + k[8:]
                    src = v
                    os.system("ln -sf %s %s" % (src,dst))
                    os.system("touch -h -r %s %s" % (src,dst))

    def get_all_object_flags(self,otype=None):
        OG = self.objectGraph
        if otype:
            return [self.get_object_flag(o) for o in OG[otype]]
        return [self.get_object_flag(o) for otype in OG.get_object_types() for o in OG[otype]]

if __name__ == "__main__":
    print("hi")
    p = Project()
    print("Project directory",p.directory)
    print("Project parameters",p.parameters)
    print("Number of object types in object graph",len(p.objectGraph.O))
    print("Number of objects in object graph",sum([len(x) for x in p.objectGraph.O.values()]))
    print("Pipeline directory is",p.get_pipeline_directory())
