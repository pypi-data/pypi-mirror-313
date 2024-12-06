set -ex

. "$(git-functions-path)"

cdtoproject

git diff --name-status | sed 's/.*\t//' | while read path; do

    git diff "$path" | ag '^[+-][^+-]' | ag -v ^.import >/dev/null || git add "$path"

done

st
