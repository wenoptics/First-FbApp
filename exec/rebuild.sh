BASEDIR=$(dirname $0)

$BASEDIR/clean-cache.sh
pushd ./app
npm install
./node_modules/.bin/electron-rebuild
popd
popd

# ../exec/clean-cache.sh && npm install && ./node_modules/.bin/electron-rebuild
# quasar clean && quasar dev -m electron
