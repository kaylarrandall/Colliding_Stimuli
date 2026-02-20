to kill hung process on ubuntu, run:
ps aux | grep -i ipykernel | grep -v grep | awk '{print $2}' | xargs -r kill -9