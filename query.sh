#!/bin/bash
set +x
exit_on_error() {
    exit_code=$1
    last_command=${@:2}
    if [ $exit_code -ne 0 ]; then
        >&2 echo "\"${last_command}\" command failed with exit code ${exit_code}."
        exit $exit_code
    fi
}

if [ -z "$1" ]; then
    echo "You must specify a target respository to stargaze."
    exit 1
fi

echo "Querying Stargazer data..."
steampipe query "with data as (
 SELECT date_trunc('hour', starred_at) AS day_hour, COUNT(1) FROM github.github_stargazer
 WHERE repository_full_name = '${1}'
 GROUP BY 1
)

SELECT day_hour, SUM(COUNT) over (order by day_hour asc rows between unbounded preceding and current row)
from data" --output csv > data.csv
tail -n +2 data.csv > data.csv.tmp && mv data.csv.tmp data.csv

echo "Running dockerized selenium"
docker run --rm -d -p 4444:4444 --name chrome-selenium selenium/standalone-chrome  &> /dev/null || exit_on_error $? docker run
echo "Generating image..."
python3 minimal.py &
sleep 2
python3 curler.py || exit_on_error $? python3 curler.py
sleep 2
echo "Copying image to local..."
docker cp chrome-selenium:/tmp/download.png ./stargazers.png || exit_on_error $? docker cp
echo "Done! Cleaning up..."
docker rm -f chrome-selenium &> /dev/null || exit_on_error $? docker rm