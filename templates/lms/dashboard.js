function addCard1(){
    const box = document.getElementById('deadlines');

    const newcard = document.createElement('div');
    newcard.className = 'p-2 bg-white shadow-sm d-flex align-items-center rounded border border-dark border-3';
    newcard.setAttribute('id', 'CS192.1');

    const newp = document.createElement('p');
    newp.className = 'fs-2 m-2'
    newp.textContent = 'CS 192';

    const newi = document.createElement('i');
    newi.className = 'fas fa-briefcase fs-1 primary-text m-2'
    newi.setAttribute('id', 'briefCaseLogo');

    const newassignment = document.createElement('bold');
    newassignment.className = "fs-4 m-2";
    newassignment.textContent = "Sprint Plan 5"

    box.appendChild(newcard);
    newcard.appendChild(newp);
    newcard.appendChild(newi);
    newcard.appendChild(newassignment);
}

function addCard2(){
    const box = document.getElementById('deadlines');

    const newcard = document.createElement('div');
    newcard.className = 'p-2 bg-white shadow-sm d-flex align-items-center rounded border border-dark border-3';
    newcard.setAttribute('id', 'CS145.1');

    const newp = document.createElement('p');
    newp.className = 'fs-2 m-2'
    newp.textContent = 'CS 145';

    const newi = document.createElement('i');
    newi.className = 'fas fa-briefcase fs-1 primary-text m-2'
    newi.setAttribute('id', 'briefCaseLogo');

    const newassignment = document.createElement('bold');
    newassignment.className = "fs-4 m-2";
    newassignment.textContent = "Lab Exercise 10"

    box.appendChild(newcard);
    newcard.appendChild(newp);
    newcard.appendChild(newi);
    newcard.appendChild(newassignment);
}

function addCard3(){
    const box = document.getElementById('deadlines');

    const newcard = document.createElement('div');
    newcard.className = 'p-2 bg-white shadow-sm d-flex align-items-center rounded border border-dark border-3';
    newcard.setAttribute('id', 'CS180.1');

    const newp = document.createElement('p');
    newp.className = 'fs-2 m-2'
    newp.textContent = 'CS 180';

    const newi = document.createElement('i');
    newi.className = 'fas fa-briefcase fs-1 primary-text m-2'
    newi.setAttribute('id', 'briefCaseLogo');

    const newassignment = document.createElement('bold');
    newassignment.className = "fs-4 m-2";
    newassignment.textContent = "Spam Classifier"

    box.appendChild(newcard);
    newcard.appendChild(newp);
    newcard.appendChild(newi);
    newcard.appendChild(newassignment);
}
addCard1();
addCard2();
addCard3();