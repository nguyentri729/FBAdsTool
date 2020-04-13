const { app, BrowserWindow, ipcMain, shell} = require("electron");
require("electron-reload")(__dirname);
const { exec } = require("child_process");

function createWindow() {
  const win = new BrowserWindow({
    width: 1000,
    height: 800,
    webPreferences: {
      nodeIntegration: true,
    },
  });

  // and load the index.html of the app.
  win.loadFile("./resource/index.html");
  // win.loadURL("http://http://localhost:3000/")
  
  // Open the DevTools.
  win.webContents.openDevTools();
}
app.allowRendererProcessReuse = true;

app.whenReady().then(() => {

  createWindow()
});
app.on("window-all-closed", () => {
  if (process.platform !== "darwin") {
    app.quit();
  }
});
app.on("activate", () => {
  if (BrowserWindow.getAllWindows().length === 0) {
    createWindow();
  }
});

//handle event
ipcMain.on("senter", (event, arg) => {
  console.log("hello viet nam");
  shell.beep();
  exec(`python D:/\\Projects/\\autoFB/\\test.py`, (err, stdout, stderr) => {
    console.log(err, stdout, stderr);
  });
});

ipcMain.on('addCredit', async (event, arg) => {
 // console.log(`python D:/\\Projects/\\autoFB/\\test.py ${arg}`)
  const callPythonFile = function() {
    return exec(`python D:/\\Projects/\\autoFB/\\test.py ${arg}`)
  }
  var proc = callPythonFile()
  proc.stdout.on('data', function (data) {
    console.log('data ne', data)
  });
  proc.on('error', function (err) {
    console.log('err ne', err)
  });
 
})