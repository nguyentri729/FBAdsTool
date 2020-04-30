const { app, BrowserWindow, ipcMain, shell } = require("electron");
const { exec } = require("child_process");

// require("electron-reload")(__dirname);

const fs = require("fs");
var win;
var activeWindow;
var keyActive;
async function createWindow() {
  keyActive = fs.readFileSync('key.txt', 'utf8')

  if (keyActive != '') {
    showWindow()
  
    //win.webContents.openDevTools();
  }else{
    activeWindow = new BrowserWindow({
      webPreferences: {
        nodeIntegration: true,
      },
      frame: false,
      width: 450,
      height: 250,
      resizable: false,
      icon: __dirname + "/icon.ico",
      parent: win,
    });
    activeWindow.loadFile("./resource/active.html");
    //activeWindow.webContents.openDevTools();
  }
  
}
const showWindow = function() {
  win = new BrowserWindow({
    webPreferences: {
      nodeIntegration: true,
    },
    icon: __dirname + "/icon.ico",
  });
  win.maximize();
  win.setMenuBarVisibility(false);
  win.loadFile("./resource/index.html");
  //win.webContents.openDevTools();
}
app.allowRendererProcessReuse = true;
app.whenReady().then(() => {
  //console.log('deptrai khoai to :)) ')
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
  let data = fs.readFileSync("countriesOptions.txt", "utf8");
  //console.log()
  event.reply("GET_CONTRIES_OPTIONS", data);
});

ipcMain.on("GET_MONEYTYPE_OPTIONS", (event, arg) => {
  let data = fs.readFileSync("moneyTypeOpions.txt", "utf8");
  //console.log()
  event.reply("GET_MONEYTYPE_OPTIONS", data);
});

ipcMain.on("GET_TIMEZONES_OPTIONS", (event, arg) => {
  let data = fs.readFileSync("timeZoneOptions.txt", "utf8");
  //console.log()
  event.reply("GET_TIMEZONES_OPTIONS", data);
});

ipcMain.on("TEST_CHANGE_IP_PROXY", (event, arg) => {
  exec(
    `${__dirname}/\\buildAction.exe${
      arg.length > 0 ? " -proxy " + arg + "" : " "
    } -test`
  );
});

ipcMain.on("CHANGE_IP_DCOM", async (event, arg) => {
  exec(`${__dirname}/\\resetDcom.bat`, function (err, stdout, stderr) {
    event.reply(
      "CALL_BACK_CHANGE_DCOM",
      JSON.stringify({
        err,
        stdout,
        stderr,
      })
    );
  });
});

ipcMain.on("CALL_ACTION", async (event, arg) => {
  const account = JSON.parse(arg);
  if (account.data.includes('-typeAcc main')){
    const name = "runMainAccount.bat"
    fs.writeFileSync('./'+name, `buildAction.exe ${account.data} -keyActive ${keyActive}`)
    
    event.reply('OPEN_FILE', name)
    return true
  }else{
    console.log(`python buildAction.py ${account.data} -keyActive ${keyActive}`)
    var callPythonFile = function () {
      // return exec(`buildAction.exe ${account.data} -keyActive ${keyActive}`);
      return exec(`buildAction.exe ${account.data} -keyActive ${keyActive}`);
    };
  }

  const proc = callPythonFile();
  



  proc.stdout.on("data", function (data) {
    try {

      fs.writeFile(
        "./logs/" + new Date().getTime().toString() + "_logs.txt",
        `python buildAction.py ${account.data} \n ${data}`,
        function (err) {
          console.log(err);
        }
      );
      
      data = JSON.parse(data);

    } catch (error) {
      data = {
        msg: "unknown",
        type: "fail",
      };
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
          type: "error",
          msg: 'can"t connect chrome!',
        },
      })
    );
  });
});

//check active keys
ipcMain.on("CHECK_KEY", function (event, key) {
 // console.log('key ne', key);
 
  if (key) {
    //console.log(`python ${__dirname}\\buildAction.py -keyActive ${key} -checkKey`)
    const callPythonFile = function () {
      return exec(`${__dirname}\\buildAction.exe -keyActive ${key} -checkKey`);
    };
    const proc = callPythonFile()
    proc.stdout.on("data", function (data) {
        event.reply('CALLBACK_CHECK_KEY', data)
        if (data.trim() == 'success') {
          showWindow()
          activeWindow.hide()
          fs.writeFile('key.txt', key.trim(), function(err) {
            console.log('error')
          })
        }

    });


  }
});
