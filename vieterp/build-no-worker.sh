#!/bin/bash

sed -i "s/<PROJECT>/${PROJECT}/g" ./config/docker/vieterp/Dockerfile

sed -i "s/<PROJECT>/${PROJECT}/g" ./config/${BRANCH}/vieterp.yaml
sed -i "s/<PROJECT>/${PROJECT}/g" ./config/${BRANCH}/vieterp-db.yaml
sed -i "s/<PROJECT>/${PROJECT}/g" ./config/${BRANCH}/vieterp-nginx.yaml
sed -i "s/<PROJECT>/${PROJECT}/g" ./config/${BRANCH}/vieterp-odoo.yaml
sed -i "s/<PROJECT>/${PROJECT}/g" ./config/${BRANCH}/vieterp-redis.yaml
sed -i "s/<PROJECT>/${PROJECT}/g" ./config/${BRANCH}/vieterp-volume.yaml

sed -i "s/<BRANCH>/${BRANCH}/g" ./config/${BRANCH}/vieterp.yaml
sed -i "s/<BRANCH>/${BRANCH}/g" ./config/${BRANCH}/vieterp-db.yaml
sed -i "s/<BRANCH>/${BRANCH}/g" ./config/${BRANCH}/vieterp-nginx.yaml
sed -i "s/<BRANCH>/${BRANCH}/g" ./config/${BRANCH}/vieterp-odoo.yaml
sed -i "s/<BRANCH>/${BRANCH}/g" ./config/${BRANCH}/vieterp-redis.yaml
sed -i "s/<BRANCH>/${BRANCH}/g" ./config/${BRANCH}/vieterp-volume.yaml

sed -i "s/<SHA>/${SHA}/g" ./config/${BRANCH}/vieterp.yaml
sed -i "s/<SHA>/${SHA}/g" ./config/${BRANCH}/vieterp-db.yaml
sed -i "s/<SHA>/${SHA}/g" ./config/${BRANCH}/vieterp-nginx.yaml
sed -i "s/<SHA>/${SHA}/g" ./config/${BRANCH}/vieterp-odoo.yaml
sed -i "s/<SHA>/${SHA}/g" ./config/${BRANCH}/vieterp-redis.yaml
sed -i "s/<SHA>/${SHA}/g" ./config/${BRANCH}/vieterp-volume.yaml