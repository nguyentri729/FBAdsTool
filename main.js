const { app, BrowserWindow, ipcMain, shell } = require("electron");
require("electron-reload")(__dirname);
const { exec } = require("child_process");
const fs = require('fs')
const axios = require('axios')
async function createWindow() {
  const win = new BrowserWindow({
    webPreferences: {
      nodeIntegration: true,
    },
    icon: __dirname + '/icon.png'
  });
  win.maximize();
  win.setMenuBarVisibility(false)
 
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
ipcMain.on("GET_CONTRIES_OPTIONS", (event, arg) => {
    let data = fs.readFileSync('countriesOptions.txt', "utf8")
    //console.log()
    event.reply('GET_CONTRIES_OPTIONS', data)
});


ipcMain.on("GET_MONEYTYPE_OPTIONS", (event, arg) => {
  let data = fs.readFileSync('moneyTypeOpions.txt', "utf8")
  //console.log()
  event.reply('GET_MONEYTYPE_OPTIONS', data)
});


ipcMain.on("GET_TIMEZONES_OPTIONS", (event, arg) => {
  let data = fs.readFileSync('timeZoneOptions.txt', "utf8")
  //console.log()
  event.reply('GET_TIMEZONES_OPTIONS', data)
});


ipcMain.on("TEST_CHANGE_IP_PROXY", (event, arg)=> {
  exec(`${__dirname}/\\buildAction.py${(arg.length > 0) ? ' -proxy ' +arg+'' : ' '} -test`);  
})


ipcMain.on("CHANGE_IP_DCOM", async (event, arg)=> {
  exec(`${__dirname}/\\resetDcom.bat`, function(err, stdout, stderr) {
    event.reply('CALL_BACK_CHANGE_DCOM', JSON.stringify({
      err,
      stdout,
      stderr
    }))
  })
})


ipcMain.on("CALL_ACTION", async (event, arg) => {
  const account = JSON.parse(arg);
  console.log(`python ${__dirname}/\\buildAction.py ${account.data}`)
  
  const callPythonFile = function () {
    return exec(`python ${__dirname}/\\buildAction.py ${account.data}`);
  };


  const proc = callPythonFile();
  proc.stdout.on("data", function (data) {
    try {
      data = JSON.parse(data)
    } catch (error) {
      data = {
        msg: 'unknown',
        type: 'fail'
      }
    }
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
        data: {
          type: 'error',
          msg: 'can"t connect chrome!'
        },
      })
    );
  });
});
