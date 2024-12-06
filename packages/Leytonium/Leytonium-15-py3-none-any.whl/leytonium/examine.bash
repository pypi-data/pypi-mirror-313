set -ex

unset context delimage

function cleanup {

    [[ -z "$context" ]] || rm -rfv $context

    [[ -z "$delimage" ]] || docker image rm $delimage

}

trap cleanup EXIT

image=$@

shells=($(docker run --rm --entrypoint ls $image /bin/bash /bin/sh || :))

if [[ 0 -lt ${#shells[@]} ]]; then

    runimage=$image

    shell=${shells[0]}

else

    context=$(mktemp -d)

    echo "FROM python
WORKDIR /image
COPY --from=$image / ." >$context/Dockerfile

    delimage=$(docker build --platform linux/amd64 -q $context)

    runimage=$delimage

    shell=bash

fi

docker run -ti --rm --entrypoint $shell -u 0 $runimage
