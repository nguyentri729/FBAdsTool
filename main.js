const { app, BrowserWindow, ipcMain, shell } = require("electron");
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
  createWindow();
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

ipcMain.on("CALL_ACTION", async (event, arg) => {
  const account = JSON.parse(arg);
  console.log(`python ${__dirname}/\\test.py ${account.data}`)
  const callPythonFile = function () {
    return exec(`python ${__dirname}/\\test.py ${account.data}`);
  };

  const proc = callPythonFile();
  proc.stdout.on("data", function (data) {
    console.log("data ne", data, account.index);
    //callback intro index.js
    event.reply(
      "CALLBACK_ACTION",
      JSON.stringify({
        index: account.index,
        data,
      })
    );
  });

  proc.on("error", function (err) {
    event.reply(
      "CALLBACK_ACTION",
      JSON.stringify({
        index: account.index,
        data: err,
      })
    );
  });
});
