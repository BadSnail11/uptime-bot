#!/bin/bash

set -euo pipefail

echo "starting worker"
exec python3 -m app.worker.celery_app