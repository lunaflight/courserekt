const loadingSpinner = document.getElementById('loading-spinner');

/**
 * Show the loading spinner element.
 * @async
 * @function
 */
async function showLoadingSpinner() {
  loadingSpinner.classList.remove('hidden');
}

/**
 * Hide the loading spinner element.
 * @async
 * @function
 */
async function hideLoadingSpinner() {
  loadingSpinner.classList.add('hidden');
}

/**
 * Toggle the visibility of course title column in the table based on the checkbox state.
 * @async
 * @function
 */
async function toggleCourseNamesByCheckbox() {
  const checkbox = document.getElementById('toggle-course-names-checkbox');
  const isVisible = checkbox.checked;

  const table = document.getElementById("table-data");
  const courseTitleIndex = 1;

  // Toggle the visibility of the column in the table body
  const tbodyCells = table.getElementsByTagName("tbody")[0].getElementsByTagName("td");
  for (let i = courseTitleIndex; i < tbodyCells.length; i += table.rows[0].cells.length) {
    tbodyCells[i].classList.toggle("hidden", !isVisible);
  }

  // Toggle the visibility of the column in the table headers
  const theadCells = table.getElementsByTagName("thead")[0].getElementsByTagName("th");
  theadCells[courseTitleIndex].classList.toggle("hidden", !isVisible);
}

/**
 * Toggle the visibility of preliminary vacancies in the table based on the checkbox state.
 * @async
 * @function
 */
async function toggleForecastByCheckbox() {
  const checkbox = document.getElementById('toggle-forecast-checkbox');
  const isVisible = checkbox.checked;

  const vacancyDataSpans = document.querySelectorAll(".vacancy-data");

  vacancyDataSpans.forEach(span => span.classList.toggle("hidden", !isVisible));
}

/**
 * Filter the courses in the table based on the input search text.
 * Courses are shown if and only if they contain at least one of the search patterns
 * as a substring in their course code.
 *
 * The search input can accept multiple search patterns delimited by spaces.
 * For example, if the input is "CS3 GEC", the table will show all courses
 * that have "CS3" or "GEC" in their course code.
 *
 * @async
 * @function
 */
async function filterCourses() {
  const searchInput = document.getElementById('search-input');
  localStorage.setItem('searchValue', searchInput.value);

  const formattedInput = searchInput.value.toUpperCase();
  const tableRows = document.getElementsByTagName('tr');
  const filters = formattedInput.split(' ').filter(Boolean);

  const courseCodeIndex = 0;

  for (let i = 1; i < tableRows.length; i++) {
    const courseCode = tableRows[i]
      .getElementsByTagName('td')[courseCodeIndex]
      .textContent
      .toUpperCase();

    const isMatch = filters.some(filter => courseCode.indexOf(filter) > -1);

    if (filters.length == 0 || isMatch) {
      tableRows[i].classList.remove('hidden');
    } else {
      tableRows[i].classList.add('hidden');
    }
  }
}

/**
 * This code block sets up event listeners and initial state when the DOM content is loaded.
 *
 * @event
 */
document.addEventListener('DOMContentLoaded', () => {
  // The checkbox determines if the course title is shown.
  const checkbox = document.getElementById('toggle-course-names-checkbox');
  checkbox.addEventListener('change', toggleCourseNamesByCheckbox);
  toggleCourseNamesByCheckbox();

  // The checkbox determines if the preliminary vacancies are shown.
  const forecastCheckbox = document.getElementById('toggle-forecast-checkbox');
  forecastCheckbox.addEventListener('change', toggleForecastByCheckbox);
  toggleForecastByCheckbox();

  // The search bar should constantly filter courses as new input is received.
  const searchInput = document.getElementById('search-input');
  searchInput.value = localStorage.getItem('searchValue') || '';
  searchInput.addEventListener('input', filterCourses);
  filterCourses();

  // The data should immediately update when new data is requested by a button press.
  const courseForm = document.getElementById('course-form');
  courseForm.addEventListener('change', () => {
    courseForm.submit();
    showLoadingSpinner();
  });
  courseForm.addEventListener('submit', event => event.preventDefault());
});
