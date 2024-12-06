set -e

path=$(gmktemp --suffix .html 2>/dev/null || mktemp)

function cleanup {
    rm -fv $path
}

trap cleanup EXIT

pandoc -T "$(basename "${@: -1}")" --toc "$@" >$path

$(if [[ -d /proc ]]; then echo firefox; else echo open; fi) $path

while true; do sleep 1; done
