#!/bin/bash

# Log-Datei erstellen oder vorhandene Log-Datei öffnen
log_file="log.txt"

# Hole die IDs aller 'Exited'-Container
exited_containers=$(sudo docker ps -a | grep 'Exited' | awk '{print $1}')

# Überprüfe, ob es exited Container gibt
if [ -z "$exited_containers" ]; then
    echo "$(date): Keine beendeten Container gefunden." | tee -a $log_file
else
    # Durchlaufe alle IDs und starte die entsprechenden Container
    for container in $exited_containers; do
        echo "$(date): Starte Container $container..." | tee -a $log_file
        sudo docker start $container
        if [ $? -eq 0 ]; then
            echo "$(date): Container $container erfolgreich gestartet." | tee -a $log_file
        else
            echo "$(date): Fehler beim Starten von Container $container." | tee -a $log_file
        fi
    done
fi





