

docker run -it \
    --name hazibot \
    --mount type=bind,source="$(pwd)",dst=/debug \
    -p 5000:5000 \
    python:3.10.4-buster \
    //bin/bash

