. "$(~/.local/bin/git-functions-path)"

function _allbranches {
    local branches="$(git branch | cut -c 3-)"
    COMPREPLY=($(compgen -W "$branches" $2))
}

function _otherbranches {
    local branches="$(git branch | grep -v '^[*]' | cut -c 3-)"
    COMPREPLY=($(compgen -W "$branches" $2))
}

function _branchnames {
    local names="$(allbranches | grep -v '^master$' | sed 's/^[^-]*-//')" # FIXME: Not just master.
    COMPREPLY=($(compgen -W "$names" $2))
}

function _demonames {
    local names="$(
        cdtoproject
        cd samples
        for d in *; do [[ -e $d/build.gradle ]] && echo $d; done
    )"
    COMPREPLY=($(compgen -W "$names" $2))
}

function _commonmessages {
    COMPREPLY=($(compgen -W 'conciser refactor refactoring undup redundant mv ren inline formatting unused idiomaticer consistency obsolete comment documentation efficienter experimentally convention simplify retire sensibler extract invalid generaler logging correcter quieter specificer reliabler eleganter temporarily minimaler determinism tastefuler preciser' $2))
}

function _unconflictedpaths {
    local paths="$(git diff --name-only --diff-filter=U | while read path; do
        grep '^=======$' "$path" &>/dev/null || echo "$path"
    done | python3 -c 'from pathlib import Path
import sys
top, = map(Path, sys.argv[1:])
for p in sys.stdin:
    # FIXME: Support paths between top and cwd.
    print((top / p).relative_to(Path.cwd()))' "$(git rev-parse --show-toplevel)")"
    COMPREPLY=($(compgen -W "$paths" $2))
}

function _loggroups {
    [[ "$_loggroups_names" ]] || _loggroups_names="$(aws logs describe-log-groups | python3 -c 'import json, sys
for group in json.load(sys.stdin)["logGroups"]:
    print(group["logGroupName"])')"
    COMPREPLY=($(compgen -W "$_loggroups_names" $2))
}

function _dockervolumes {
    local names="$(docker volume ls --format '{{.Name}}')"
    COMPREPLY=($(compgen -W "$names" $2))
}

complete -F _allbranches ren
complete -F _otherbranches co
complete -F _otherbranches eb
complete -F _otherbranches setparent
complete -F _branchnames br
complete -F _demonames demo
complete -F _commonmessages ci
complete -F _unconflictedpaths rd
complete -F _unconflictedpaths rdx
complete -F _loggroups awslogs
complete -F _dockervolumes vunzip
