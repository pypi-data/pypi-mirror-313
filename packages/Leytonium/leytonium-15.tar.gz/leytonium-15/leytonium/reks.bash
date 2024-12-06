set -e

. "$(git-functions-path)"

b=$(thisbranch)
ks=kitchen-sink
co $ks
stopmsg="$(touchmsg)" # FIXME: This is wrong, there may be a manual commit.
co $b

ids=($(git cherry $ks | tac | while read _ id; do
    msg="$(git log -n 1 --format=%s $id)"
    [[ "$stopmsg" = "$msg" ]] && break
    echo $id
done | tac))

drop -f
co $ks
git branch $b # TODO: Configure parent.
co $b
git cherry-pick ${ids[@]}
