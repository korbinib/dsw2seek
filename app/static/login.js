const nextButton = document.querySelector('#next-button');
const prevButton = document.querySelector('#prev-button');
const loginError = document.querySelector('#login-error');
const tabs       = document.querySelectorAll('.tab');

/**
 * Go to the next tab when the user presses the enter key on the first tab.
 */
document.querySelectorAll('#username, #password')
    .forEach(element => element.addEventListener('keyup', event => {
        if(event.key !== 'Enter') return;
        nextButton.click();
        event.preventDefault();
    })
);

/**
 * Go to the next tab when the user clicks on the "next" button.
 * Also show an error message if the request failed.
 */
nextButton.addEventListener('click', async () => {
    nextButton.innerHTML = '<span class="button-spinner"></span>';
    const res = await login();

    if (res.status !== 200) {
        loginError.style.visibility = 'visible';
    }
    else {
        loginError.style.visibility = 'hidden';
        nextTab();
    }

    nextButton.innerHTML = 'Log in';
});

prevButton.addEventListener('click', () => {
    prevTab();
});

/**
 * Send the username and password to the backend.
 * The credentials are required when searching for institutions in the next step.
 */
const login = async () => {
    const username = document.querySelector('#username').value;
    const password = document.querySelector('#password').value;
    const data = {username, password}

    return await fetch('http://localhost:8080/login', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(data)
        });
}

const nextTab = () => {
    for (const [index, tab] of tabs.entries()) {
        if (tab.classList.contains('active') && index < tabs.length - 1) {
            tab.classList.remove('active');
            tabs[index + 1].classList.add('active');
        }
    }
}

const prevTab = () => {
    for (const [index, tab] of tabs.entries()) {
        if (tab.classList.contains('active') && index > 0) {
            tab.classList.remove('active');
            tabs[index - 1].classList.add('active');
        }
    }
}