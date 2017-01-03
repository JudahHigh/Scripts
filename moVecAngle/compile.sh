#!/bin/bash

cp ./moVecAngle.f90 ./BACKmoVecAngle.f90
gfortran -O3 moVecAngle.f90 -o a
