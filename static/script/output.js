$(document).ready(function() {
    var table = $('#example').DataTable({
        "autoWidth": false, // Disable auto width
        "scrollX": true,    // Enable horizontal scrolling
        "columnDefs": [
                { "width": "100px", "targets": "_all" } // Set maximum width for columns
            ]
        })
        columns.adjust()
        .responsive.recalc();
});
function openNewTab(htmlContent) {
    const newTab = window.open('', '_blank');
    newTab.document.open();
    newTab.document.write(htmlContent);
    newTab.document.close();
    }
const openModalButton = document.getElementById('chartbutton');

openModalButton.addEventListener('click', async () => {
      try {
            const response = await fetch('/render_dashboard');
            const htmlString = await response.text();
            openNewTab(htmlString);
        } catch (error) {
            console.error('Error fetching HTML:', error);
        }
});
$(".navbar").removeClass('sticky');