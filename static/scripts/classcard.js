function addCard(assignment){
    const box = document.getElementById('deadlines');


    const newcard = document.createElement('div');
    newcard.className = 'classcard text-white bg-dark m-2 h-100 rounded';
    newcard.style = 'max-width:300px';
    newcard.setAttribute('id', assignment.name);

    const newcardheader = document.createElement('div');
    newcardheader.className = 'text-center';
    newcardheader.textContent = assignment.name;

    const newcardbody = document.createElement('div');
    newcardbody.className = 'classcard-body';

    const newassignmentDesc = document.createElement('p');
    newassignmentDesc.className = "classcard-text scroll";
    newassignmentDesc.textContent = assignment.description;

    const newcardfooter = document.createElement('div');
    newcardfooter.className = 'classcard-footer text-center';


    const newassignmentLink = document.createElement('a');
    newassignmentLink.className = "btn btn-primary";
    newassignmentLink.href = assignment.course_url;
    newassignmentLink.target = "_blank"
    newassignmentLink.textContent = "Go to class";

    box.appendChild(newcard);

    newcard.appendChild(newcardheader);
    newcard.appendChild(newcardbody);
    newcard.appendChild(newcardfooter);

    newcardbody.appendChild(newassignmentDesc);
    newcardfooter.appendChild(newassignmentLink);
}

function ownerGreeting(n){
    const box = document.getElementById('owner');
    var greetingsArray = ["Here are your classes,"];
    var greeting = greetingsArray[Math.floor(Math.random()*greetingsArray.length)];
    box.textContent = greeting;
}

(() => {
    fetch('/api/uvle/classes')
    .then(response => response.json())
    .then((json) => {
        ownerGreeting("Bill");
        console.log(json);

        for(const course of json.courses) {
            addCard(course);
        }
    });
    fetch('/api/gclass/classes', {mode: 'no-cors'})
    .then(response => response.json())
    .then((json) => {
        ownerGreeting("Bill");
        console.log(json);

        for(const course of json.courses) {
            addCard(course);
        }
    });
}
)();


