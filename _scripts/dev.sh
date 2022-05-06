docker run -it \
    --name hazibot \
    --mount type=bind,source="$(pwd)",dst=/debug \
    -p 5000:5000 \
    getfutureproof/lap4_debug_multi \
    //bin/bash