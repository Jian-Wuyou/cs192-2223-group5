function addCard(assignment){
    const box = document.getElementById('deadlines');


    const newcard = document.createElement('div');
    newcard.className = 'classcard bg-light m-2 h-100 rounded';
    newcard.style = 'max-width:300px';
    newcard.setAttribute('id', assignment.course_name);

    const newcardheader = document.createElement('div');
    newcardheader.className = 'classcard-header text-center';
    newcardheader.textContent = assignment.course_name;

    const newcardbody = document.createElement('div');
    newcardbody.className = 'classcard-body';

    const newassignmentTitle = document.createElement('h5');
    newassignmentTitle.className = "classcard-title";
    newassignmentTitle.textContent = assignment.name;

    const newassignmentDesc = document.createElement('p');
    newassignmentDesc.className = "classcard-text scroll";
    newassignmentDesc.textContent = assignment.description;

    const newcardfooter = document.createElement('div');
    newcardfooter.className = 'classcard-footer text-center bg-light';


    const newassignmentLink = document.createElement('a');
    newassignmentLink.className = "btn btn-primary";
    newassignmentLink.href = assignment.course_url;
    newassignmentLink.target = "_blank"
    newassignmentLink.textContent = "Go to page";

    box.appendChild(newcard);

    newcard.appendChild(newcardheader);
    newcard.appendChild(newcardbody);
    newcard.appendChild(newcardfooter);
    newcardbody.appendChild(newassignmentTitle);
    newcardbody.appendChild(newassignmentDesc);
    newcardfooter.appendChild(newassignmentLink);
}

function numberOfAssignments(n){
    const box = document.getElementById('assignmentNumber');
    const text1 = document.createElement('span');
    text1.style = "color:#fff";
    text1.textContent = "You Have ";
    box.appendChild(text1)
    const text2 = document.createElement('span');
    text2.style = "color:#ff0000";
    text2.className = "redtext";
    text2.textContent = n;
    box.appendChild(text2)
    const text3 = document.createElement('span');
    text3.style = "color:#fff";
    text3.textContent = " Assigments Due!";
    box.appendChild(text3)
}

function ownerGreeting(){
    const box = document.getElementById('owner');
    var greetingsArray = ["Welcome back,", "Let's get you back from where you left off,", "Good day,", "Back to work,"];
    var greeting = greetingsArray[Math.floor(Math.random()*greetingsArray.length)];
    box.textContent = greeting;
}

fetch('/api/uvle/deadlines')
    .then(response => response.json())
    .then((json) => {
        ownerGreeting();
        numberOfAssignments(json.deadlines.length);
        for (var i = 0; i < json.deadlines.length; i++){
            console.log(json.deadlines[i]);
            addCard(json.deadlines[i]);
        }
    });
    fetch('/api/gclass/deadlines')
    .then(response => response.json())
    .then((json) => {
        ownerGreeting();
        console.log(json.deadlines);
        numberOfAssignments(json.deadlines.length);
        for (var i = 0; i < json.deadlines.length; i++){
            addCard(json.deadlines[i]);
        }
    });


