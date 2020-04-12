const { app, BrowserWindow, ipcMain  } = require("electron");
require('electron-reload')(__dirname);

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
  win.removeMenu()
  // Open the DevTools.
 // win.webContents.openDevTools();
}
app.whenReady().then(createWindow);
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
ipcMain.on('sayHello', (event, arg) => {
  console.log(arg) // prints "ping"
})
