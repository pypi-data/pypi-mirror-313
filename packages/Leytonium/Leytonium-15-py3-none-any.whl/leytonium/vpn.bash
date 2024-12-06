set -e

eval "$(arid-config ~/.settings.arid vpn)"

if sudo killall openvpn; then sleep 1; fi

routes="$(sudo route)"

echo "$routes"

path=$(tempfile)

echo "$authuser" >$path

sudo openvpn --config "$configpath" --daemon --auth-user-pass $path

rm $path

while true; do

    sleep .1

    [[ "$(sudo route)" = "$routes" ]] || break

done

sleep .1

sudo route
