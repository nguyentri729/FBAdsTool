const { ipcRenderer, clipboard } = require("electron");
sayBtn = document.getElementById("sayHello");

var dem = 0;
var isCredit = false; //using add credit
var list_credit;


//Options change 
$('#addCredit:first').change(function() {
  
  
  if (!$(this)[0].checked) {
    isCredit = false;
    list_credit = null;
    $('#paste_credit').hide()
  }else{
    $('#paste_credit').show()
  }
  
})

$('#paste_credit').click(function() {
  list_credit = clipboard.readText().split("\n");
  $(this).html(`Thêm credit (${list_credit.length})`)
  isCredit = true

  $('#headerTable').html(`
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

  `)
})

$('#paste_account').click(function () {
  let list_account = clipboard.readText().split("\n");
  $(this).html(`Dán account (${list_account.length})`)
  //check credit first
  if(!list_credit && $('#addCredit')[0].checked) {
    alert("Thêm credit trước !");
    return true
  }
  
  
  //handle credit && creat options
  if (isCredit) {
    var optionsHTML = '<option value="random">Random</option>' + list_credit.map((credit, index) => {
        return `<option value="${credit}">${credit}</option>`
    })
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
          </td>`
    }else{
      var moreOptions = ''
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
          <textarea style="width: 100%;">${account[3]}</textarea>
        </td>
        ${moreOptions}
        <td class="jsgrid-cell jsgrid-align-center" style="width: 60px;">
            <b id="status_${vtri}" class="text-normal">Ready !!</b><br>
            
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
  
  //Max of thread 
  const numberThread = parseInt($("#thread_number")[0].value);
 
  let listInputChecked = $('#lists_account input[type="checkbox"]:checked');


  //set waiting
  for (let j = 0; j < listInputChecked.length; j++) {
      const input = listInputChecked[j];
      const tr_id = $(input).attr("tr-id");
      $("#tr_"+tr_id).attr('class', '')
      $("#status_" + tr_id)
      .html("Đang chờ...")
      .attr("class", "text-primary");
  }

  var checkThread = 0;
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
    let moreString = ''
    if($('#addCredit')[0].checked) {
        const selectOption = $(`#tr_${tr_id} select`)[0].value
        if (selectOption == 'random') {
            var splitOptions = list_credit[Math.round(Math.random()*list_credit.length)].split('|')
        }else{
            var splitOptions = selectOption.split('|')
        }
        const cardInfo = {
          cardName: splitOptions[0],
          cardNumber: splitOptions[1],
          cardExperied: splitOptions[2],
          ccv: splitOptions[3]
        }
        moreString = '-credit ' + btoa(JSON.stringify(cardInfo))
    }
    //send request for main
    ipcRenderer.send(
      "CALL_ACTION",
      JSON.stringify({
        index: tr_id,
        data: `-acc ${btoa(JSON.stringify(account))} ${moreString}`,
      })
    );

    //set status 
    $("#status_" + tr_id)
      .html("Đang chạy...")
      .attr("class", "text-normal");

    $("#tr_"+tr_id).attr('class', '')
    //when max thread
    checkThread++;
    


    
    if (checkThread >= numberThread) {
      await new Promise(function (resolve, reject) {
        var count = 0;
        //wait callback_action
        ipcRenderer.on("CALLBACK_ACTION", function (event, arg) {
          arg = JSON.parse(arg);
          if (arg.index) {
            //set status
            arg.data.trim() == "success"
              ? $("#status_" + arg.index)
                  .attr("class", "text-success")
                  .html("Thành công")
              : $("#status_" + arg.index)
                  .attr("class", "text-danger")
                  .html("Thất bại");
    
            $("#tr_"+arg.index).attr('class', 'jsgrid-row')
    
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
        }, 100000);
      });
      console.log('max thread roi ne')
      checkThread = 0;
    }
    

    
  }
});
