#!/bin/bash

workloads=("traces/DataServing/00-L1d" "traces/MapReduce/00-L1d" "traces/MediaStreaming/00-L1d" "traces/SATSolver/00-L1d" "traces/TPCCDB2/00-L1d" "traces/TPCCOracle/00-L1d" "traces/WebFrontend/00-L1d" "traces/WebSearch/00-L1d")
replacementPolicy=("LRU" "NMRU" "Random")
prefetching=("next_line" "Stride")

for j in ${prefetching[@]}
do
    echo -e "-------->\033[0;31mPrefetching Algorithm \033[1;33m$j\033[0m<--------"
    for i in ${workloads[@]}
    do
        echo -e "\033[0;31mstart \033[1;33m$i\033[0m"
        python3 run.py -c 32 -b 64 -a 8 -r LRU -p $j -s y -w $i
        echo -e "----------------------> \033[0;32mfinish\033[0m <----------------------"
        echo ""
    done
done