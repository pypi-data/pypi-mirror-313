# Copyright (c) 2023-2024 Datalayer, Inc.
#
# Datalayer License

import os
import secrets

os.environ.setdefault("DATALAYER_JWT_ISSUER", "https://test.datalayer.io")
os.environ.setdefault("DATALAYER_JWT_SECRET", secrets.token_hex(32))
os.environ.setdefault("DATALAYER_JWT_ACCESS_TOKEN_EXPIRES", "1")

# We strongly advice developing within the dev container
os.environ.setdefault("DATALAYER_SOLR_ZK_HOST", "zoo1:2181")
