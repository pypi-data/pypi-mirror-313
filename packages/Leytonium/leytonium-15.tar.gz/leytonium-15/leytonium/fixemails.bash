username="$(git config user.name)"
useremail="$(git config user.email)"

function summary {
    git log --pretty="%an %ae%n%cn %ce" | sort -u
}

summary

git filter-branch --env-filter '

if [ "$GIT_AUTHOR_NAME" = "'"$username"'" ]; then
    GIT_AUTHOR_EMAIL='"$useremail"'
fi

if [ "$GIT_COMMITTER_NAME" = "'"$username"'" ]; then
    GIT_COMMITTER_EMAIL='"$useremail"'
fi

' -- --all

summary
