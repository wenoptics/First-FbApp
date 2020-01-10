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

    (`Quasar`: `v1.6.1`, `Quasar CLI`: `1.0.5`)

    See 

    e.g. `$` `yarn global add @quasar/cli`
    f
    `$` `export PATH="$(yarn global bin):$PATH"`

4. Initilize the Project
   
   In the application folder:

    `$` `cd app`

    `$` `yarn install` 

### 2. 🎉Run Dev!

`$` `quasar dev -m electron`

(Or on Linux, if encourtering chrome-sandbox issue, we can disable Electron sandbox by:
`$` `quasar dev -m electron -- --no-sandbox --disable-setuid-sandbox`)

### 3. 🎉Build

`$` `quasar build -m electron`

If you build an AppImage (`/app/dist/electron/Packaged/<some_name>.AppImage`), if have trouble with chrome-sandbox, you can disable sandbox with `--no-sandbox` flag. (So far, the app is being developing without the presence of the sandbox)

 - About a this [fix](https://github.com/electron-userland/electron-builder/issues/4278)
 - More about [the SUID sandbox issue](https://github.com/electron/electron/issues/17972)
 - [Chromium sandbox](https://chromium.googlesource.com/chromium/src/+/master/docs/design/sandbox_faq.md)

