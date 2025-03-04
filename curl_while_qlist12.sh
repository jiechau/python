#!/bin/bash

# Configuration parameters
API_URL=http://172.18.5.39:8080/api/getwlist
JSON_PAYLOAD=getwlist.json
TIME_THRESHOLD=1.0
#TIME_THRESHOLD=0.5
#TIME_THRESHOLD=0.01

while true; do
    # Execute curl and capture the output
    result=$(curl -X POST -H "Content-Type: application/json" \
        ${API_URL} \
        -d @${JSON_PAYLOAD} -so /dev/null \
        -w "%{http_code}, time:%{time_total}, size:%{size_download}")

    # Extract the time value using awk
    time=$(echo "$result" | awk -F'time:' '{print $2}' | awk -F',' '{print $1}')

    # Compare time with threshold using bc for floating-point comparison
    if [ "$(echo "$time > ${TIME_THRESHOLD}" | bc)" -eq 1 ]; then
        datetime=$(date '+%Y-%m-%d %H:%M:%S')
        echo "$datetime - $result"
        #echo "$result"
    fi

    # Optional: Add a small sleep to prevent overwhelming the server
    sleep 1
done
