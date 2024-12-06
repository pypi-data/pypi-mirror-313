set -ex

vol="$1"

docker run --rm -v "$vol:/vol/$vol" -v "$PWD:/host" python cp -av "/vol/$vol" /host
