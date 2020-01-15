# Development

`$` `git clone https://github.com/wenoptics/First-FbApp.git`

## Linux

### 1. Preparing

1. Install NodeJS 

    (_Currently, the LTS version is `12.14.1`_)

    e.g. `$` `curl -sL https://rpm.nodesource.com/setup_12.x | bash -`

    or `$` `curl -sL https://rpm.nodesource.com/setup_12.x | sudo bash -`

    For more dist, see [nodesource/distributions](https://github.com/nodesource/distributions/blob/master/README.md).

2. Install Yarn

3. Install Quasar CLI

    (`Quasar`: `v1.7.3`, `Quasar CLI`: `1.5.1`)

    See 

    e.g. `$` `yarn global add @quasar/cli`
    
    `$` `export PATH="$(yarn global bin):$PATH"`

4. Initilize the Project
   
   In the application folder:

    `$` `cd app`

    `$` `yarn install` 

### 2. 🎉Run Dev!

#### 1. Clean Cache

Considering to clean cache if there's any build-time error:

`$` `./exec/clean-cache.ps1`

(Then rebuild:)

`$` `npm install && ./node_modules/.bin/electron-rebuild`

#### 2. Install new dependencies:

Run `$` `./node_modules/.bin/electron-rebuild` after module installed.

#### 3. Start dev run

`$` `quasar dev -m electron`

(Or on Linux, if encourtering chrome-sandbox issue, we can disable Electron sandbox by:
`$` `quasar dev -m electron -- --no-sandbox --disable-setuid-sandbox`)

### 3. 🎉Build

`$` `quasar build -m electron`

If you built an AppImage (`/app/dist/electron/Packaged/<some_name>.AppImage`), if have trouble with chrome-sandbox, you can disable sandbox with `--no-sandbox` flag. (So far, the app is being developing without the presence of the sandbox)

 - About a this [fix](https://github.com/electron-userland/electron-builder/issues/4278)
 - More about [the SUID sandbox issue](https://github.com/electron/electron/issues/17972)
 - [Chromium sandbox](https://chromium.googlesource.com/chromium/src/+/master/docs/design/sandbox_faq.md)

### Troubleshots

  #### 1. Complaining about node-gyp on build-time

  - `node-gyp` (`node-gyp-bin`)

  - `The imported project "D:\Microsoft.Cpp.Default.props" was not found.`

  **Things to check**

  This might only affect build time, so even you get `quasar dev -m electron` works, still might run into this issue (it occurs at the packaging stage)

  - Check [this Quasar article](https://quasar.dev/quasar-cli/developing-electron-apps/preparation#A-note-for-Windows-Users) about build on windows

  - Check [this Electron article](https://electronjs.org/docs/tutorial/using-native-node-modules#installing-modules-and-rebuilding-for-electron) about rebuilding module for Electron

  - Install `visual-cpp-build-tools` (VS2015) and [more disscussions](https://github.com/nodejs/node-gyp/issues/671) on this.
