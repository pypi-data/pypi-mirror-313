set -e

base=$(pb)

ids=($(git cherry $base | tac | while read _ id; do echo $id; done))

function commitmessage {
    git log -n 1 --pretty=format:%B "$@"
}

function stripwip {
    echo "${1#WIP }"
}

function jirarefs {
    echo WIP
    local ref refs=$(expr $(thisbranch) : '\(\([a-z]\+[0-9]\+_\)\+\)')
    IFS=_ refs=($refs)
    for ref in ${refs[@]}; do
        ref=${ref^^}
        echo $(expr $ref : '\([A-Z]\+\)')-$(expr $ref : '[A-Z]\+\([0-9]\+\)')
    done
}

function jiraref {
    menu jirarefs 'JIRA reference for this commit'
}

function cherry {
    local id
    for id in ${ids[@]}; do
        echo $id "$(commitmessage $id | head -1)"
    done
}

. "$(git-functions-path)"

menu cherry Which commit should absorb all newer commits

index=$((MENU_NUMBER-1))

id=${ids[$index]}

git reset --hard $id

git cherry-pick $(for i in $(seq $((index-1)) -1 0); do echo ${ids[$i]}; done)

git reset --soft $id~1

message="$(jiraref) ...

$(for i in $(seq $((index)) -1 0); do echo "$((index-i+1)). $(stripwip "$(commitmessage ${ids[$i]})")"; done)"

git commit -em "$message"
