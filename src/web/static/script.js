const loadingSpinner = document.getElementById('loading-spinner'); // Get the loading spinner element

async function showLoadingSpinner() {
  loadingSpinner.classList.remove('hidden');
}

async function hideLoadingSpinner() {
  loadingSpinner.classList.add('hidden');
}

async function toggleColumnByCheckbox() {
  const checkbox = document.getElementById('toggle-column-checkbox');
  const isVisible = checkbox.checked;

  const table = document.getElementById("table-data");
  const columnIndex = 1;

  // Toggle the visibility of the column in the tbody
  const tbodyCells = table.getElementsByTagName("tbody")[0].getElementsByTagName("td");
  for (let i = columnIndex; i < tbodyCells.length; i += table.rows[0].cells.length) {
    tbodyCells[i].classList.toggle("hidden", !isVisible);
  }

  // Toggle the visibility of the column in the thead
  const theadCells = table.getElementsByTagName("thead")[0].getElementsByTagName("th");
  theadCells[columnIndex].classList.toggle("hidden", !isVisible);
}

async function filterCourses() {
  const searchInput = document.getElementById('search-input');
  const filter = searchInput.value.toUpperCase();
  const tableRows = document.getElementsByTagName('tr');

  const filters = filter.split(' ').filter(Boolean);

  for (let i = 1; i < tableRows.length; i++) {
    const courseCode = tableRows[i].getElementsByTagName('td')[0].textContent.toUpperCase();

    const isMatch = filters.some(filter => courseCode.indexOf(filter) > -1);

    if (filters.length == 0 || isMatch) {
      tableRows[i].classList.remove('hidden');
    } else {
      tableRows[i].classList.add('hidden');
    }
  }
}

document.addEventListener('DOMContentLoaded', function() {
  const checkbox = document.getElementById('toggle-column-checkbox');

  checkbox.addEventListener('change', () => toggleColumnByCheckbox());
  toggleColumnByCheckbox();

  const searchInput = document.getElementById('search-input');
  searchInput.addEventListener('input', filterCourses);
  filterCourses();

  const courseForm = document.getElementById('course-form');
  courseForm.addEventListener('change', () => {
    courseForm.submit();
    showLoadingSpinner();
  });
  courseForm.addEventListener('submit', event => event.preventDefault());
});
