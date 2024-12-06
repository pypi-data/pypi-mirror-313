set -e

[[ $(basename "$0") = drclean.py ]] && armed=armed

function logged {
    [[ "$armed" ]] || return 0
    echo "$@" >&2
    "$@"
}

docker ps -a

ids=$(docker ps -aq)

[[ "$ids" ]] && {
    logged docker stop $ids
    logged docker rm $ids
}

docker images

ids=$(docker images | tail -n +2 | ag -v '^(?:rabbitmq|python|redis|postgres|adminer|minio|confluentinc|maven|busybox|localstack|jenkins|openjdk|ubuntu|oraclelinux|container-registry.oracle.com|fat|.+[.]amazonaws[.]com|combatopera)[ /]' | awk '{ print $3 }')

[[ "$ids" ]] && {
    logged docker rmi -f $ids # Need -f to remove images with multiple tags.
}

docker volume ls

ids=$(docker volume ls --format '{{.Name}}' | grep -v '^mirror$') || true

[[ "$ids" ]] && {
    logged docker volume rm $ids
}

docker network ls

logged docker network prune -f

logged docker builder prune -f
