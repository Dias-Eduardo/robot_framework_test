#!/usr/bin/bash

sudo git add *
echo -e "Para a conseguir realizar o commit utilize o token a seguir no campo de senha"
echo -e  "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"

sudo git commit -m "$1"

sudo git push 


