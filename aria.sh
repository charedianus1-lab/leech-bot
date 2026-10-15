aria2c --allow-overwrite=true --auto-file-renaming=true \
        --enable-rpc=true \
       --rpc-max-request-size=1024M --max-connection-per-server=10 --max-concurrent-downloads=1 --split=8 \
       --seed-ratio=0 --check-integrity=true --continue=true --daemon=true --disk-cache=40M --force-save=true \
       --min-split-size=10M --check-certificate=false --optimize-concurrent-downloads=true \
       --http-accept-gzip=true --max-file-not-found=0 --max-tries=20  --reuse-uri=true \
       --content-disposition-default-utf8=true --user-agent=Wget/1.12 --quiet=true \
       --summary-interval=0 --max-upload-limit=1K