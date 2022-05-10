docker run --name postgres -p 5432:5432 -e POSTGRES_PASSWORD=password -d postgres

docker run -it \
    --name hazibot \
    --mount type=bind,source="$(pwd)",dst=/debug \
    -p 5000:5000 \
    python:3.10.4-buster \
    //bin/bash

