#!/bin/bash

NETWORK_NAME="data-net"

# Verifica se a rede já existe
if ! docker network ls | grep -q $NETWORK_NAME; then
  echo "Criando a rede Docker: $NETWORK_NAME..."
  docker network create $NETWORK_NAME
  echo "Rede criada com sucesso!"
else
  echo "A rede $NETWORK_NAME já existe. Nenhuma ação necessária."
fi