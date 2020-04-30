const { ipcRenderer, clipboard } = require("electron");
const keyInput = document.getElementById("keyInput");
const loading = document.getElementById("loading");

keyInput.addEventListener("change", function (e) {
  if (e.target.value != "") {
    ipcRenderer.send("CHECK_KEY", e.target.value);
    keyInput.setAttribute("disabled", true);
    loading.innerHTML =
      '<img width="60px" src="https://thumbs.gfycat.com/EnchantingInbornDogwoodtwigborer-max-1mb.gif">';
  }
});

ipcRenderer.on("CALLBACK_CHECK_KEY", function (event, data) {
  if (data.trim() != "success") {
    keyInput.removeAttribute("disabled");
    alert("Key hết hạn hoặc không có kết nối mạng.\nVui lòng thử lại sau !");
    loading.innerHTML = "";
  }
});
