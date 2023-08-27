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
if($("#prompt").val().trim()==''){
    $(".warningtext").removeClass('hidden');
}
else{
    $("#app").addClass('disabled');
$('#modalContainer').removeClass('hidden');
$('#modalContainer').style.display = 'block';
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
    coltype+=`(${columns[i]},${dtypes[i]}),`
}
combinedData += `table: ${column1}, schema: ${column2}, columns: ${coltype}\n`;
});
$.ajax({
    url: "/process_textarea",
    type: "POST",
    contentType: "application/json",
    data: JSON.stringify({'query':$("#prompt").val(),'schema':combinedData}),
    success: function(response) {
        $("#prompt").val(response.trim());
        $("#request-query").addClass('hidden');
        $("#execute-query").removeClass('hidden');
        $("#clear-prompt").addClass('hidden');
        $("#reset-prompt").removeClass('hidden');
        $('#modalContainer').addClass('hidden');
        $("#app").removeClass('disabled');
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

// ============open ai gpt slider for temperature========================
// const slider = document.querySelector('input[type="range"]');
// const sliderValue = document.getElementById('sliderValue');

// slider.addEventListener('input', (event) => {
//   const value = parseFloat(event.target.value).toFixed(1);
//   sliderValue.textContent = value;
// });
