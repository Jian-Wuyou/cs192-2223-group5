function addCard(assignment){
    const box = document.getElementById('deadlines');

    const newcard = document.createElement('div');
    newcard.className = 'p-2 bg-white shadow-sm d-flex align-items-center rounded border border-dark border-3';
    newcard.setAttribute('id', assignment.course_name);

    const newp = document.createElement('p');
    newp.className = 'fs-2 m-2'
    newp.textContent = assignment.course_name;

    const newi = document.createElement('i');
    newi.className = 'fas fa-briefcase fs-1 primary-text m-2'
    newi.setAttribute('id', 'briefCaseLogo');

    const newassignment = document.createElement('bold');
    newassignment.className = "fs-4 m-2";
    newassignment.textContent = assignment.name

    box.appendChild(newcard);
    newcard.appendChild(newp);
    newcard.appendChild(newi);
    newcard.appendChild(newassignment);
}

function numberOfAssignments(n){
    const box = document.getElementById('assignmentNumber');
    box.textContent = n + " Assignments Due!"
}

fetch('dashboard_script/deadlines.json')
    .then(response => response.json())
    .then((json) => {
        numberOfAssignments(json.deadlines.length)
        for (var i = 0; i < json.deadlines.length; i++){
            console.log(json.deadlines[i])
            addCard(json.deadlines[i])
        }
    });
