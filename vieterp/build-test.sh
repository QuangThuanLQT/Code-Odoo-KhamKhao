#!/bin/bash

sed -i "s/<PROJECT>/${PROJECT}/g" ./config/docker/vieterp/Dockerfile
sed -i "s/<SHA>/${SHA}/g" ./worker/${BRANCH}/Dockerfile
sed -i "s/<BRANCH>/${BRANCH}/g" ./worker/${BRANCH}/Dockerfile
sed -i "s/<PROJECT>/${PROJECT}/g" ./worker/${BRANCH}/Dockerfile
sed -i "s/<SHA>/${SHA}/g" ./config/${BRANCH}/vieterp-test.yaml
sed -i "s/<BRANCH>/${BRANCH}/g" ./config/${BRANCH}/vieterp-test.yaml
sed -i "s/<PROJECT>/${PROJECT}/g" ./config/${BRANCH}/vieterp-test.yaml