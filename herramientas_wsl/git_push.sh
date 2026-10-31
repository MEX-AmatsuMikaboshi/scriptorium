#!/usr/bin/env bash
# git push desde Linux: el Control inteligente de aplicaciones bloquea el libcurl de Git para Windows.
# Usa las credenciales de GitHub guardadas en el administrador de credenciales de Windows (firmado).
cd "$HOME/scriptorium" || exit 1
gcm="/mnt/c/Program Files/Git/mingw64/bin/git-credential-manager.exe"
git -c credential.helper= -c "credential.helper=!\"$gcm\"" -c core.filemode=false push "$@"
