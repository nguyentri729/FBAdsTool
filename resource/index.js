const { ipcRenderer, clipboard } = require("electron");
const {getCurrentWindow, globalShortcut, dialog} = require('electron').remote;

var reload = ()=>{
  getCurrentWindow().reload()
}

globalShortcut.register('F5', reload);
globalShortcut.register('CommandOrControl+R', reload);
// here is the fix bug #3778, if you know alternative ways, please write them
window.addEventListener('beforeunload', ()=>{
  globalShortcut.unregister('F5', reload);
  globalShortcut.unregister('CommandOrControl+R', reload);
})
$('#reset').click(function() {
  reload()
})

var dem = 0;
var isCredit = false; //using add credit
var list_credit;
var listProxy;
const getProxy = function () {
  //console.log( get proxy )
  try {
    return listProxy[Math.floor(Math.random() * listProxy.length)];
  } catch (error) {
    return "";
  }
};
//Options change
$("#addCredit:first").change(function () {
  if (!$(this)[0].checked) {
    isCredit = false;
    list_credit = null;
    $("#paste_credit").hide();
  } else {
    $("#paste_credit").show();
  }
});

$("#sayTestChangeIP").click(function () {
  switch ($("#change_ip_select")[0].value) {
    case "proxy":
      ipcRenderer.send("TEST_CHANGE_IP_PROXY", getProxy());
      break;
    case "dcom":
      ipcRenderer.send("CHANGE_IP_DCOM", "test");
      break;
    default:
      break;
  }
});

ipcRenderer.on("CALL_BACK_CHANGE_DCOM", function (event, arg) {
  try {
    arg = JSON.parse(arg);
    const regex = /[error]/;
    if (arg.err || regex.test(arg.stdout)) {
      $("#changeIPStatus").html(
        `<span style="color: red;">Reset IP lỗi</span>`
      );
    } else {
      $("#changeIPStatus").html(
        '<span style="color: green">Reset IP success !</span>'
      );
    }
  } catch (error) {
    console.log(error);
    $("#changeIPStatus").html('<span style="color: red">unknown error</span>');
  }
});
$("#proxy_list").change(function (e) {
  listProxy = e.target.value.split("\n");
  console.log(listProxy);
});
//option change
$("#change_ip_select").change(function (e) {
  const value = e.target.value;

  if (value == "proxy") {
    $("#proxy_list").show();
  } else {
    $("#proxy_list").hide();
  }
});

$("#copy_selected").click(function () {
  let checkedInput = $('#lists_account input[type="checkbox"]:checked:enabled');
  let data = "";
  for (let index = 0; index < checkedInput.length; index++) {
    const input = checkedInput[index];
    const id = $(input).attr("tr-id");
    data +=
      $("#tr_" + id + " textarea")[0].value +
      "|" +
      $("#tr_" + id + " textarea")[1].value +
      "|" +
      $("#tr_" + id + " textarea")[2].value +
      "|" +
      $("#tr_" + id + " textarea")[3].value +
      "\n";
  }
  clipboard.writeText(data);
  alert("Copy thành công");
});
$("#delete_selected").click(function () {
  let checkedInput = $('#lists_account input[type="checkbox"]:checked:enabled');
  for (let index = 0; index < checkedInput.length; index++) {
    const input = checkedInput[index];
    const id = $(input).attr("tr-id");
    $("#tr_" + id + "").remove();
  }
});
$("#createAccountAds:first").change(function () {
  if (!$(this)[0].checked) {
    addAdsAccount = false;
    $("#createAccountAdsOptions").hide();
  } else {
    ipcRenderer.send("GET_CONTRIES_OPTIONS", "");
    ipcRenderer.send("GET_MONEYTYPE_OPTIONS", "");
    ipcRenderer.send("GET_TIMEZONES_OPTIONS", "");
    addAdsAccount = true;
    $("#createAccountAdsOptions").show();
  }
});

$("#copy_success").click(function () {
  const statusLists = $(".status");
  let data = "";

  for (let index = 0; index < statusLists.length; index++) {
    const status = statusLists[index];

    if ($(status).text().trim() == "Thành công") {
      const tr_id = $(status).attr("tr-id");
      data +=
        $("#tr_" + tr_id + " textarea")[0].value +
        "|" +
        $("#tr_" + tr_id + " textarea")[1].value +
        "|" +
        $("#tr_" + tr_id + " textarea")[2].value +
        "|" +
        $("#tr_" + tr_id + " textarea")[3].value +
        "\n";
    }
  }
  clipboard.writeText(data);
  alert("Copy thành công !");
});

$("#paste_credit").click(function () {
  list_credit = clipboard.readText().split("\n");
  $(this).html(`Thêm credit (${list_credit.length})`);
  isCredit = true;

  $("#headerTable").html(`
  <tr class="jsgrid-header-row">
    <th class="jsgrid-header-cell jsgrid-align-center"
      style="width: 10px;">
      STT
    </th>
    <th class="jsgrid-header-cell jsgrid-align-center jsgrid-header-sortable" style="width: 20px;">
        <input type="checkbox"   id="checkAll" /> 
    </th>
    <th class="jsgrid-header-cell jsgrid-align-center jsgrid-header-sortable" style="width: 50px;">
      Email
    </th>
    <th class="jsgrid-header-cell jsgrid-header-sortable" style="width: 50px;">
      Password
    </th>
    <th class="jsgrid-header-cell jsgrid-align-center jsgrid-header-sortable" style="width: 50px;">
      2FA
    </th>
    <th class="jsgrid-header-cell jsgrid-align-center jsgrid-header-sortable" style="width: 50px;">
      Cookie
    </th>
    <th class="jsgrid-header-cell jsgrid-align-center jsgrid-header-sortable" style="width: 50px;">
        Credit
      </th>
    <th class="jsgrid-header-cell jsgrid-align-center jsgrid-header-sortable" style="width: 60px;">
      Trạng thái
    </th>
  </tr>

  `);
});

$("#paste_account").click(function () {
  let list_account = clipboard.readText().split("\n");
  $(this).html(`Dán account (${list_account.length})`);
  //check credit first
  if (!list_credit && $("#addCredit")[0].checked) {
    alert("Thêm credit trước !");
    return true;
  }

  //handle credit && creat options
  if (isCredit) {
    var optionsHTML =
      '<option value="random">Random</option>' +
      list_credit.map((credit, index) => {
        return `<option value="${credit}">${credit}</option>`;
      });
  }
  for (let index = 0; index < list_account.length; index++) {
    const account = list_account[index].split("|");
    const vtri = ++dem;
    if (
      account[1] == undefined &&
      account[2] == undefined &&
      account[3] == undefined
    ) {
      alert("Copy đúng định dạng \n User|Pass|2Fa|Cookie");
      break;
    }

    //check creadit
    if (isCredit) {
      var moreOptions = `
          <td class="jsgrid-cell jsgrid-align-center" style="width: 50px;">
              <select style="width: 100px;" id="card_${vtri}">
                  ${optionsHTML}
              </select>
          </td>`;
    } else {
      var moreOptions = "";
    }

    //show list account
    $("#lists_account").append(`<tr class="jsgrid-row" id="tr_${vtri}">
        <td class="jsgrid-cell" style="width: 10px;">
          ${vtri}
        </td>
        <td class="jsgrid-cell jsgrid-align-center" style="width: 20px; text-align: center;">
          <input type="checkbox" tr-id="${vtri}" /> 
        </td>
        <td class="jsgrid-cell jsgrid-align-center" style="width: 50px;">
          <textarea style="width: 100%;">${account[0]}</textarea>
        </td>
        <td class="jsgrid-cell jsgrid-align-center" style="width: 50px;">
          <textarea style="width: 100%;">${account[1]}</textarea>
        </td>
        <td class="jsgrid-cell jsgrid-align-center" style="width: 50px;">
          <textarea style="width: 100%;">${account[2]}</textarea>
        </td>
        <td class="jsgrid-cell jsgrid-align-center" style="width: 50px;">
          <textarea style="width: 100%;" id="cookie_input_${vtri}">${account[3]}</textarea>
        </td>
        ${moreOptions}
        <td class="jsgrid-cell jsgrid-align-center status" tr-id="${vtri}" style="width: 60px;">
            <b id="status_${vtri}" class="text-normal">Ready</b><br>
        </td>
        </tr>`);
  }
});

$("#checkAll").change(function () {
  $("#lists_account input").attr("checked", $(this)[0].checked);
  if (!$(this)[0].checked) {
    let checkedInput = $(
      '#lists_account input[type="checkbox"]:checked:enabled'
    );
    for (let index = 0; index < checkedInput.length; index++) {
      const input = checkedInput[index];
      $(input).attr("checked", false);
    }
  }
});

$("#checkAll").on("click", function () {
  if (this.checked) {
    $('#lists_account input[type="checkbox"]').each(function () {
      this.checked = true;
    });
  } else {
    $('#lists_account input[type="checkbox"]').each(function () {
      this.checked = false;
    });
  }
});

$('#lists_account input[type="checkbox"]').on("click", function () {
  if (
    $('#lists_account input[type="checkbox"]:checked').length ==
    $('#lists_account input[type="checkbox"]').length
  ) {
    $("#checkAll").prop("checked", true);
  } else {
    $("#checkAll").prop("checked", false);
  }
});

$("#start").click(async function (e) {
  try {
    //Max of thread
    const numberThread = parseInt($("#thread_number")[0].value);
    const numberChangeIP = parseInt($("#changeIpAfter")[0].value);
    let listInputChecked = $('#lists_account input[type="checkbox"]:checked');

    //set waiting
    for (let j = 0; j < listInputChecked.length; j++) {
      const input = listInputChecked[j];
      const tr_id = $(input).attr("tr-id");
      $("#tr_" + tr_id).attr("class", "");
      $("#status_" + tr_id)
        .html("Đang chờ...")
        .attr("class", "text-primary");
    }

    var checkThread = 0;
    var checkChangeIP = 0;
    $("#total").html(listInputChecked.length);
    var proxyIP = getProxy();
    for (let index = 0; index < listInputChecked.length; index++) {
      const input = listInputChecked[index];
      const tr_id = $(input).attr("tr-id");
      const accountTextarea = $("#tr_" + tr_id + " textarea");
      const account = {
        username: accountTextarea[0].value,
        password: accountTextarea[1].value,
        secret: accountTextarea[2].value,
        cookie: accountTextarea[3].value,
      };
      let moreString = "-updateCookie";
      if ($("#addCredit")[0].checked) {
        const selectOption = $(`#tr_${tr_id} select`)[0].value;
        if (selectOption == "random") {
          var splitOptions = list_credit[
            Math.floor(Math.random() * list_credit.length)
          ].split("|");
        } else {
          var splitOptions = selectOption.split("|");
        }
        const cardInfo = {
          cardName: splitOptions[0],
          cardNumber: splitOptions[1],
          cardExperied: splitOptions[2],
          ccv: splitOptions[3],
        };
        moreString = "-credit " + btoa(JSON.stringify(cardInfo));
      }

      if ($("#createAccountAds")[0].checked) {
        moreString = `-createAdsAccount -moneyIndex ${
          $("#moneyTypeOptions")[0].value
        } -timeIndex ${$("#timeZoneOptions")[0].value} -countryIndex ${
          $("#contryOptions")[0].value
        } `;
      }

      //set status
      $("#status_" + tr_id)
        .html("Đang chạy...")
        .attr("class", "text-normal");

      $("#tr_" + tr_id).attr("class", "");
      //when max thread
      checkThread++;
      checkChangeIP++;
      //check change IP
      if (checkChangeIP >= numberChangeIP) {
        //change IP with dcom
        switch ($("#change_ip_select")[0].value) {
          case "dcom":
            $("#changeIPStatus").html("Đang reset Dcom");
            ipcRenderer.send("CHANGE_IP_DCOM", "");
            await new Promise(function (resolve, reject) {
              //wait callback_action
              ipcRenderer.on("CALL_BACK_CHANGE_DCOM", function (event, arg) {
                console.log("data change dcom", arg);
                resolve("");
              });
              setTimeout(() => {
                reject("fail");
              }, 300000);
            });
            break;
          case "proxy":
            $("#changeIPStatus").html("Proxy : " + proxyIP);
            moreString += " -proxy " + proxyIP;
            proxyIP = getProxy();
            break;
          default:
            break;
        }
        checkChangeIP = 0;
      }

      //send request for main
      ipcRenderer.send(
        "CALL_ACTION",
        JSON.stringify({
          index: tr_id,
          data: `-acc ${btoa(JSON.stringify(account))} ${moreString}`,
        })
      );

      //check thread
      if (checkThread >= numberThread) {
        await new Promise(function (resolve, reject) {
          var count = 0;
          //wait callback_action
          ipcRenderer.on("CALLBACK_ACTION", function (event, arg) {
            arg = JSON.parse(arg);
            console.log("data ne", arg.data);

            if (arg.index) {
              try {
                if (arg.data.status == "success") {
                  $("#count_success").html(
                    parseInt($("#count_success").html()) + 1
                  );
                  $("#status_" + arg.index)
                    .attr("class", "text-success")
                    .html("Thành công");
                } else {
                  $("#count_fail").html(parseInt($("#count_fail").html()) + 1);
                  $("#status_" + arg.index)
                    .attr("class", "text-danger")
                    .html("Thất bại <br><small>" + arg.data.msg + "</small>");
                }
                if (arg.data.cookie) {
                  $("#cookie_input_" + arg.index + "")[0].value =
                    arg.data.cookie;
                }
              } catch (error) {
                console.log(error);
                $("#status_" + arg.index)
                  .attr("class", "text-danger")
                  .html("Thất bại <br><small>unknown</small>");
              }

              $("#tr_" + arg.index).attr("class", "jsgrid-row");

              console.log("index xong : ", arg.index);
              count++;
              if (count >= numberThread) {
                count = 0;
                resolve();
              }
            }
          });
          setTimeout(() => {
            reject("fail");
          }, 300000);
        });
        checkThread = 0;
      }
    }
  } catch (error) {
    console.log(error);
  }
});

ipcRenderer.on("GET_CONTRIES_OPTIONS", function (e, arg) {
  const contries = arg.split("\n");
  $("#contryOptions").html("");
  for (let index = 0; index < contries.length; index++) {
    $("#contryOptions").append(`
      <option value="${index + 1}" ${1 + index == 235 ? 'selected=""' : ""}>${
      contries[index]
    }</options>
    `);
  }
});

ipcRenderer.on("GET_TIMEZONES_OPTIONS", function (e, arg) {
  const timeZone = arg.split("\n");
  $("#timeZoneOptions").html("");
  for (let index = 0; index < timeZone.length; index++) {
    $("#timeZoneOptions").append(`
      <option value="${54 + index}" ${54 + index == 436 ? 'selected=""' : ""}>${
      timeZone[index]
    }</options>
    `);
  }
});

ipcRenderer.on("GET_MONEYTYPE_OPTIONS", function (e, arg) {
  const moneyType = arg.split("\n");
  $("#moneyTypeOptions").html("");
  for (let index = 0; index < moneyType.length; index++) {
    $("#moneyTypeOptions").append(`
      <option value="${index}" ${index == 16 ? 'selected=""' : ""}>${
      moneyType[index]
    }</options>
    `);
  }
});
