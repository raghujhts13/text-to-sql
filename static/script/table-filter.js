const filterInput = document.getElementById('filterInput');
const tableBody = document.getElementById('tableBody');
const rows = tableBody.getElementsByTagName('tr');

filterInput.addEventListener('input', function() {
  const filterValue = filterInput.value.toLowerCase();
  
  for (let i = 0; i < rows.length; i++) {
    const tablecell = rows[i].getElementsByTagName('td')[0];
    const schemacell = rows[i].getElementsByTagName('td')[1];
    if ((tablecell) || (schemacell)) {
      const nameValue = tablecell.textContent || tablecell.innerText;
      const schemavalue = schemacell.textContent || schemacell.innerText;
      if ((nameValue.toLowerCase().indexOf(filterValue) > -1)||(schemavalue.toLowerCase().indexOf(filterValue) > -1)) {
        rows[i].style.display = '';
      } else {
        rows[i].style.display = 'none';
      }
    }
  }
});
