for p in proj*; do
    (cd $p; 
        . ./setenv.sh
        build_object_graph.py createDirs
        run_snake.sh -j 
    )
done
