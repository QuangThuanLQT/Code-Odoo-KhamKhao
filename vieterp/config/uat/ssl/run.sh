#!/usr/bin/env bash

kubectl create secret generic ttsapp-keys --from-file=./fullchain.pem --from-file=./privkey.pem --from-file=./ssl-dhparams.pem --from-file=./options-ssl-nginx.conf --namespace uat