#!/bin/bash

git add ../../
git stash
git checkout develop
git pull --rebase
git push
git checkout vieterp
git pull --rebase
git rebase develop
git push
git checkout develop
git stash pop