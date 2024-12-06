function touchmsg {
    echo "touch $(thisbranch)"
}

function showmenu {
    local n=1
    echo void
    $1 | while read id rest; do
        [[ "$id" ]] || continue # Possible if stream is empty.
        echo $id
        echo "$(printf '%3d' $n) $id $rest" >&2
        ((n+=1))
    done
}

function menu {
    local n ids=($(showmenu "$1"))
    shift
    read -p "$*? " n
    echo ${ids[$n]}
    MENU_NUMBER=$n
}

function cdtoproject {
    while [[ ! -d .git ]]; do cd ..; done
}

function thisbranch {
    git rev-parse --abbrev-ref HEAD
}

function allbranches {
    git branch | cut -c 3-
}
