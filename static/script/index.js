window.onload = function(){
    $("#clear-prompt").click();
}
const openModalButton = document.getElementById('openModalButton');
const closeModalButton = document.getElementById('closeModalButton');
const modal = document.getElementById('myModal');

openModalButton.addEventListener('click', () => {
  modal.classList.remove('hidden');
});

closeModalButton.addEventListener('click', () => {
  modal.classList.add('hidden');
});

// text area functions
$("#clear-prompt").click(function(){
$("#prompt").val("");
})
$("#request-query").click(function(){
    $(".successtext").addClass('hidden');
    if($("#prompt").val().trim()==''){
        $(".warningtext").removeClass('hidden');
        $(".warningcheckbox").addClass('hidden');
    }
    else if(document.querySelectorAll('.checkbox:checked').length==0){
        $(".warningtext").addClass('hidden');
        $(".warningcheckbox").removeClass('hidden');
    }
    else{
        $(".warningtext").addClass('hidden');
        $(".warningcheckbox").addClass('hidden');
        $('#modalContainer').removeClass('hidden');
        // $('#modalContainer').style.display = 'block';
        let combinedData = "";
        $(".checkbox:checked").each(function() {
            const row = $(this).closest("tr");
            const column1 = row.find("td:nth-child(1)").text();
            const column2 = row.find("td:nth-child(2)").text();
            const column3 = row.find("td:nth-child(3)").text();
            const column4 = row.find("td:nth-child(4)").text();
            let columns = column3.split(",")
            let dtypes = column4.split(",")
            coltype=''
            for(let i=0;i<columns.length;i++){
                // coltype+=`(${columns[i]},${dtypes[i]}),`
                coltype+=` ${columns[i]} [ ${dtypes[i]}] `
            }
            combinedData += `schema: ${column2}, table: ${column1}, columns: ${coltype}\n`;
        });
        $(".functionclass").addClass('disabled');
        $("#dropdownDefaultButton").addClass('disabled');
        $.ajax({
            url: "/process_textarea",
            type: "POST",
            contentType: "application/json",
            data: JSON.stringify({'query':$("#prompt").val(),'schema':combinedData}),
            success: function(response) {
                $(".functionclass").removeClass('disabled');
                $("#dropdownDefaultButton").removeClass('disabled');
                $("#prompt").val(response['query'].trim());
                $("#time-taken").text(response['time']);
                $("#request-query").addClass('hidden');
                $("#execute-query").removeClass('hidden');
                $("#clear-prompt").addClass('hidden');
                $("#reset-prompt").removeClass('hidden');
                $('#modalContainer').addClass('hidden');
                $(".warningtext").addClass('hidden');
                $(".warningcheckbox").addClass('hidden');
                $(".successtext").removeClass('hidden');
            }
        });
    }
});
$("#execute-query").click(function(){
$.ajax({
    url: "/clean_query",
    type: "POST",
    contentType: "application/json",
    data: JSON.stringify({'query':$("#prompt").val()}),
    success: function(response) {
        window.location.href = `/output_page`;
    }
});
})
$("#reset-prompt").click(function(){
    $("#prompt").val('');
    $(".warningtext").addClass('hidden');
    $(".warningcheckbox").addClass('hidden');
    $(".successtext").addClass('hidden');
    $("#request-query").removeClass('hidden');
    $("#execute-query").addClass('hidden');
    $("#clear-prompt").removeClass('hidden');
    $("#reset-prompt").addClass('hidden');
}) 

const masterCheckbox = document.getElementById('masterCheckbox');
const checkboxes = document.querySelectorAll('.checkbox');
const rows1 = tableBody.getElementsByTagName('tr');
masterCheckbox.addEventListener('change', () => {
    for (let i = 0; i < checkboxes.length; i++) {
        if (rows1[i].style.display !== 'none') {
            checkboxes[i].checked = masterCheckbox.checked;
        }
    }
});

const ulElement = document.getElementById("dropdown-group");
const liElements = ulElement.getElementsByTagName("li");

for (let i = 0; i < liElements.length; i++) {
  liElements[i].addEventListener("click", function() {
    let selection = liElements[i].textContent.trim();
    $.ajax({
        url: "/change_db",
        type: "POST",
        contentType: "application/json",
        data: JSON.stringify({'database':selection}),
        success: function(response) {
            if(response['status']==200){
                window.location.href = '/';
            }
            else if(response['status']==300){
                $("#samedb").removeClass('hidden');
            }
            else{
                alert(response['msg']);
            }
        }
    });
  });
}
$("#dropdownDefaultButton").click(function(){
    $("#samedb").addClass('hidden');
})
