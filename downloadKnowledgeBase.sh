#!/bin/bash

wget "https://wikidatafiles.nyc3.digitaloceanspaces.com/Hosting/Hosting/SpacyEntityLinker/datafiles.tar.gz" -O /tmp/knowledge_base.tar.gz
tar -xzf /tmp/knowledge_base.tar.gz --directory ./data_spacy_entity_linker
rm /tmp/knowledge_base.tar.gz
