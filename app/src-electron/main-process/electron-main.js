import { app, BrowserWindow, nativeTheme } from 'electron'
import path from 'path'

try {
  if (process.platform === 'win32' && nativeTheme.shouldUseDarkColors === true) {
    require('fs').unlinkSync(path.join(app.getPath('userData'), 'DevTools Extensions'))
  }
} catch (_) { }

/**
 * Set `__statics` path to static files in production;
 * The reason we are setting it here is that the path needs to be evaluated at runtime
 */
if (process.env.PROD) {
  global.__statics = path.join(__dirname, 'statics').replace(/\\/g, '\\\\')
}

function createBackendProc () {
  // TODO pass the name/path from .conf (https://quasar.dev/quasar-cli/cli-documentation/handling-process-env#Adding-to-process.env)
  let binPath = path.join(__statics, 'backend-bin', 'FBapp_backend', 'FBapp_backend' + '.exe')
  console.log('bin path is ', binPath)
  let port = 50051
  let pyProc
  let isProduction = true // process.env.PROD

  if (isProduction) {
    pyProc = require('child_process').execFile(binPath, [port])
  } else {
    pyProc = require('child_process').spawn('python', [binPath, port])
  }

  if (pyProc != null) {
    console.log(pyProc)
    console.log('Bin process success on port ' + port)
  }
}

let mainWindow

function createWindow () {
  /**
   * Initial window options
   */
  mainWindow = new BrowserWindow({
    width: 1000,
    height: 800,
    useContentSize: true,
    webPreferences: {
      // Change from /quasar.conf.js > electron > nodeIntegration;
      // More info: https://quasar.dev/quasar-cli/developing-electron-apps/node-integration
      nodeIntegration: QUASAR_NODE_INTEGRATION,
      preload: path.resolve(__dirname, 'electron-preload.js')
    },
    frame: false
    // titleBarStyle: 'hidden'
  })

  mainWindow.loadURL(process.env.APP_URL)

  mainWindow.on('closed', () => {
    mainWindow = null
  })
}

app.on('ready', () => {
  createWindow()
  createBackendProc()
})

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit()
  }
})

app.on('activate', () => {
  if (mainWindow === null) {
    createWindow()
  }
})
