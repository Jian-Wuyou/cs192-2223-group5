function addCard(assignment) {
    const box = document.getElementById("deadlines");

    const newcard = document.createElement("div");
    newcard.className = "classcard bg-light m-2 h-100 rounded";
    newcard.style = "max-width:300px";
    newcard.setAttribute("id", assignment.course_name);

    const newcardheader = document.createElement("div");
    newcardheader.className = "classcard-header text-center";
    newcardheader.textContent = assignment.course_name;

    const newcardbody = document.createElement("div");
    newcardbody.className = "classcard-body";

    const newassignmentTitle = document.createElement("h5");
    newassignmentTitle.className = "classcard-title";
    newassignmentTitle.textContent = assignment.name;

    const newassignmentDesc = document.createElement("p");
    newassignmentDesc.className = "classcard-text scroll";
    newassignmentDesc.textContent = `Due on ${assignment.date}`;

    const newcardfooter = document.createElement("div");
    newcardfooter.className = "classcard-footer text-center bg-light";

    const newassignmentLink = document.createElement("a");
    newassignmentLink.className = "btn btn-primary";
    newassignmentLink.href = assignment.url;
    newassignmentLink.target = "_blank";
    newassignmentLink.textContent = "Go to page";

    box.appendChild(newcard);

    newcard.appendChild(newcardheader);
    newcard.appendChild(newcardbody);
    newcard.appendChild(newcardfooter);
    newcardbody.appendChild(newassignmentTitle);
    newcardbody.appendChild(newassignmentDesc);
    newcardfooter.appendChild(newassignmentLink);
}

function numberOfAssignmentsUvle(n) {
    const box = document.getElementById("assignmentNumberUvle");
    const text1 = document.createElement("span");
    text1.style = "color:#fff";
    text1.textContent = "You Have ";
    box.appendChild(text1);
    const text2 = document.createElement("span");
    text2.style = "color:#ff0000";
    text2.className = "redtext";
    text2.textContent = n;
    box.appendChild(text2);
    const text3 = document.createElement("span");
    text3.style = "color:#fff";
    text3.textContent = " Assigments Due on UVLê!";
    box.appendChild(text3);
}

function numberOfAssignmentsGclass(n) {
    const box = document.getElementById("assignmentNumberGclass");
    const text1 = document.createElement("span");
    text1.style = "color:#fff";
    text1.textContent = "You Have ";
    box.appendChild(text1);
    const text2 = document.createElement("span");
    text2.style = "color:#ff0000";
    text2.className = "redtext";
    text2.textContent = n;
    box.appendChild(text2);
    const text3 = document.createElement("span");
    text3.style = "color:#fff";
    text3.textContent = " Assigments Due on Google Classroom!";
    box.appendChild(text3);
}

function ownerGreeting() {
    const box = document.getElementById("owner");
    var greetingsArray = [
        "Welcome back,",
        "Let's get you back from where you left off,",
        "Good day,",
        "Back to work,",
    ];
    var greeting =
        greetingsArray[Math.floor(Math.random() * greetingsArray.length)];
    box.textContent = greeting;
}

fetch("/api/uvle/deadlines", {
    method: "POST",
    headers: {
        "Content-Type": "application/json",
    },
    body: JSON.stringify({ description: false }),
})
    .then((response) => response.json())
    .then((json) => {
        ownerGreeting();
        console.log(json.deadlines);
        numberOfAssignmentsUvle(json.deadlines.length);
        for (const deadline of json.deadlines) {
            addCard(deadline);
        }
    });
fetch("/api/gclass/deadlines", {
    method: "POST",
    headers: {
        "Content-Type": "application/json",
    },
    body: JSON.stringify({ description: false }),
})
    .then((response) => response.json())
    .then((json) => {
        ownerGreeting();
        console.log(json.deadlines);
        numberOfAssignmentsGclass(json.deadlines.length);
        for (const deadline of json.deadlines) {
            addCard(deadline);
        }
    });
