function filterCourses() {
  let searchInput = document.getElementById('search-input');
  let filter = searchInput.value.toUpperCase();
  let tableRows = document.getElementsByTagName('tr');

  let filters = filter.split(' ').filter(Boolean);

  for (let i = 1; i < tableRows.length; i++) {
    let courseCode = tableRows[i].getElementsByTagName('td')[0].textContent.toUpperCase();

    let isMatch = filters.some(filter => courseCode.indexOf(filter) > -1);

    if (filters.length == 0 || isMatch) {
      tableRows[i].classList.remove('hidden');
    } else {
      tableRows[i].classList.add('hidden');
    }
  }
}

document.addEventListener('DOMContentLoaded', function() {
  let searchInput = document.getElementById('search-input');
  searchInput.addEventListener('input', filterCourses);
  filterCourses();

  let courseForm = document.getElementById('course-form');
  courseForm.addEventListener('change', () => courseForm.submit());
  courseForm.addEventListener('submit', event => event.preventDefault());
});
