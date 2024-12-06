set -e

if [[ "$@" ]]; then
    args=("$@")
else
    args=($(pb))
    read -p "Press enter to rebase on: $args"
fi

git rebase "${args[@]}"
