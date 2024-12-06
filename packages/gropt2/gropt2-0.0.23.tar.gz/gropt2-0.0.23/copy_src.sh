#!/bin/bash
rsync -ac ../src/*.cpp ./c_src/
rsync -ac ../src/*.hpp ./c_src/
rsync -ac ../src/Eigen ./c_src/
rsync -ac ../src/fftw3 ./c_src/
