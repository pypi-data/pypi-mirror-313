#!/bin/bash

# define all target directories
declare -a dirs=(
    "bec_ipython_client"
    "bec_lib"
    "bec_server"
    "pytest_bec_e2e"
)

mkdir dist

# loop over all directories and run the build command
for dir in "${dirs[@]}"
do
    echo "Building $dir"
    cd $dir
    python -m build
    cp dist/* ../dist
    rm -r ./dist
    cd ..
done
