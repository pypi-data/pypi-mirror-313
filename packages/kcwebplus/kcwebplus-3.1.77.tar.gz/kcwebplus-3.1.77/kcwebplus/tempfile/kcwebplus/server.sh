chmod -R 777 /kcwebplus
pkill kcwebplus
cd /kcwebplus
nohup kcwebplus --host 0.0.0.0 --port 39001 --processcount 4 --timeout 600 server -start > app/runtime/log/server.log 2>&1 &