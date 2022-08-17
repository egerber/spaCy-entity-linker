#!/bin/bash

wget "https://huggingface.co/MartinoMensio/spaCy-entity-linker/resolve/main/knowledge_base.tar.gz" -O /tmp/knowledge_base.tar.gz
tar -xzf /tmp/knowledge_base.tar.gz --directory ./data_spacy_entity_linker
rm /tmp/knowledge_base.tar.gz
