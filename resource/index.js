const { ipcRenderer, clipboard } = require("electron");
sayBtn = document.getElementById("sayHello");

var dem = 0;
document.getElementById("paste_account").addEventListener("click", function () {
  
    let list_account= clipboard.readText().split('\n')
    for (let index = 0; index < list_account.length; index++) {
        const account = list_account[index].split('|');
        const vtri = ++dem
        if(account[1] == undefined && account[2] == undefined && account[3] == undefined) {
            alert('Copy đúng định dạng \n User|Pass|2Fa|Cookie')
            break;
        }
        $("#lists_account").append(`<tr class="jsgrid-row" id="tr_${vtri}">
        <td class="jsgrid-cell" style="width: 30px;">
          ${vtri}
        </td>
        <td class="jsgrid-cell" style="width: 50px; text-align: center;">
          <input type="checkbox" tr-id="${vtri}" /> 
        </td>
        <td class="jsgrid-cell jsgrid-align-center" style="width: 100px;">
          <textarea style="width: 100%;">${account[0]}</textarea>
        </td>
        <td class="jsgrid-cell jsgrid-align-center" style="width: 100px;">
          <textarea style="width: 100%;">${account[1]}</textarea>
        </td>
        <td class="jsgrid-cell jsgrid-align-center" style="width: 100px;">
          <textarea style="width: 100%;">${account[2]}</textarea>
        </td>
        <td class="jsgrid-cell jsgrid-align-center" style="width: 100px;">
          <textarea style="width: 100%;">${account[3]}</textarea>
        </td>
        <td class="jsgrid-cell jsgrid-align-center" style="width: 60px;">
            <b id="status_${vtri}" class="text-normal">Ready !!</b><br>
            
        </td>
        </tr>`);
        
    }
  
});


$('#checkAll').change(function() {
   
    $('#lists_account input').attr("checked", $(this)[0].checked);
    if(!$(this)[0].checked) {
        let checkedInput = $('#lists_account input[type="checkbox"]:checked:enabled')
        for (let index = 0; index < checkedInput.length; index++) {
            const input = checkedInput[index];
            $(input).attr("checked", false)
        }
    }
})


$('#checkAll').on('click',function(){
    if(this.checked){
        $('#lists_account input[type="checkbox"]').each(function(){
            this.checked = true;
        });
    }else{
         $('#lists_account input[type="checkbox"]').each(function(){
            this.checked = false;
        });
    }
});

$('#lists_account input[type="checkbox"]').on('click',function(){
    if($('#lists_account input[type="checkbox"]:checked').length == $('#lists_account input[type="checkbox"]').length){
        $('#checkAll').prop('checked',true);
    }else{
        $('#checkAll').prop('checked',false);
    }
});




$('#start').click(function() {
    let listInputChecked = $('#lists_account input[type="checkbox"]:checked')
    for (let index = 0; index < listInputChecked.length; index++) {
        const input = listInputChecked[index];
        const tr_id = $(input).attr('tr-id')
        const accountTextarea = $('#tr_'+tr_id+' textarea')
        const account = {
            'username': accountTextarea[0].value,
            'password':  accountTextarea[1].value,
            'secret':  accountTextarea[2].value,
            'cookie':  accountTextarea[3].value,
        }

        let returnData = ipcRenderer.send('addCredit', `-acc ${btoa(JSON.stringify(account))}`)
        console.log(returnData)
        
    }
})