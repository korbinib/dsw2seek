let institutions = []; // store all institutions globally
let timeout = null;

const institutionId    = document.querySelector('#institutionId');
const selected         = document.querySelector('.selected');
const optionsContainer = document.querySelector('.options-container');
const searchBox        = document.querySelector('.search-box input');
const spinner          = document.querySelector('.spinner');
const optionsList      = document.querySelectorAll('.option');

/**
 * Open the select box whenever the user clicks on it.
 */
selected.addEventListener('click', () => {
    optionsContainer.classList.toggle('active');

    searchBox.value = '';

    if (optionsContainer.classList.contains('active')) {
        searchBox.focus();
    }
});

/**
 * Only fetch institutions after the user has stopped typing.
 */
searchBox.addEventListener('keyup', async event => {
    optionsContainer.innerHTML = ''; // delete all existing children
    institutions = [];
    spinner.style.display = 'inline-block';
    clearTimeout(timeout);

    timeout = setTimeout(() => {
        fetchInstitutions(event);
    }, 1000)
});

/**
 * Fetch all institutions by calling the /typeahead endpoint of this application,
 * which in turn calls the actual /typeahead endpoint of SEEK.
 * 
 * The returned institutions are used to create options for the institution selector.
 */
const fetchInstitutions = async event => {
    const query = event.target.value.toLowerCase();
    const res = await fetch(`${TYPEAHEAD_URL}?query=${query}`);
    let data = await res.json();
    spinner.style.display = 'none';

    if ('results' in data) // in production, the returned institutions are wrapped in 'results' for some reason.
        data = data['results'];

    for (let institution of data)
        createOption(institution);
}

/**
 * Use the given institution to create an option for the institution selector.
 */
const createOption = institution => {
    const id = institution['id'];
    const name = institution['name'] ?? institution['text']; // Different Seek instances use either 'name' or 'text'.

    institutions.push({id, name});

    const option = document.createElement('div');
    option.classList.add('option');
    option.innerHTML = `
        <input type="radio" class="radio" id="${name}" />
        <label for="${name}">${name}</label>
    `;
    option.addEventListener('click', () => {
        selected.innerHTML = name;
        institutionId.value = id;
        optionsContainer.classList.remove('active');
    });
    optionsContainer.appendChild(option);
}
