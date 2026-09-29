console.log("JavaScript connected successfully!");


// ===============================
// SHOW SECTION
// ===============================

function showSection(sectionId) {

    const sections =
        document.querySelectorAll(".content-section");

    sections.forEach(function(section) {
        section.style.display = "none";
    });


    const selectedSection =
        document.getElementById(sectionId);

    if (selectedSection) {
        selectedSection.style.display = "block";
    }


    // Active dashboard button

    const buttons =
        document.querySelectorAll(
            ".dashboard-actions button"
        );

    buttons.forEach(function(button) {
        button.classList.remove("active");
    });


    const clickedButton =
        document.querySelector(
            `.dashboard-actions button[onclick="showSection('${sectionId}')"]`
        );

    if (clickedButton) {
        clickedButton.classList.add("active");
    }


    // Load latest students when View opens

    if (sectionId === "view-section") {
        loadStudents();
    }
}


// ===============================
// LOAD STUDENTS FROM MYSQL
// ===============================

async function loadStudents() {

    try {

        const response =
            await fetch("/api/students");


        const students =
            await response.json();


        if (!response.ok) {

            console.error(
                students.message ||
                "Failed to load students."
            );

            return;
        }


        displayStudents(students);

        updateDashboard(students);

    }

    catch (error) {

        console.error(
            "Error loading students:",
            error
        );

    }
}


// ===============================
// UPDATE DASHBOARD
// ===============================

function updateDashboard(students) {

    document.getElementById(
        "total-students"
    ).textContent = students.length;


    const maleCount =
        students.filter(function(student) {

            return String(student.gender)
                .trim()
                .toLowerCase() === "male";

        }).length;


    const femaleCount =
        students.filter(function(student) {

            return String(student.gender)
                .trim()
                .toLowerCase() === "female";

        }).length;


    document.getElementById(
        "male-students"
    ).textContent = maleCount;


    document.getElementById(
        "female-students"
    ).textContent = femaleCount;
}


// ===============================
// DISPLAY STUDENTS
// ===============================

function displayStudents(students) {

    const tableBody =
        document.getElementById(
            "student-table-body"
        );


    tableBody.innerHTML = "";


    if (students.length === 0) {

        tableBody.innerHTML = `

            <tr>

                <td colspan="6">
                    No students available.
                </td>

            </tr>

        `;

        return;
    }


    students.forEach(function(student) {

        const row =
            document.createElement("tr");


        row.innerHTML = `

            <td>${student.student_id}</td>

            <td>${student.name}</td>

            <td>${student.age}</td>

            <td>${student.gender}</td>

            <td>${student.city}</td>

            <td>${student.department}</td>

        `;


        tableBody.appendChild(row);

    });
}


// ===============================
// ADD STUDENT
// ===============================

const studentForm =
    document.getElementById(
        "student-form"
    );


if (studentForm) {

    studentForm.addEventListener(
        "submit",
        async function(event) {

            event.preventDefault();


            const name =
                document.getElementById(
                    "student-name"
                ).value.trim();


            const age =
                document.getElementById(
                    "student-age"
                ).value;


            const gender =
                document.getElementById(
                    "student-gender"
                ).value;


            const city =
                document.getElementById(
                    "student-city"
                ).value.trim();


            const department =
                document.getElementById(
                    "student-department"
                ).value.trim();


            if (
                name === "" ||
                age === "" ||
                gender === "" ||
                city === "" ||
                department === ""
            ) {

                alert(
                    "Please fill all fields."
                );

                return;
            }


            const studentAge =
                Number(age);


            if (
                studentAge < 5 ||
                studentAge > 100
            ) {

                alert(
                    "Age must be between 5 and 100."
                );

                return;
            }


            if (
                !/^[A-Za-z ]+$/.test(name)
            ) {

                alert(
                    "Name must contain letters and spaces only."
                );

                return;
            }


            if (
                !/^[A-Za-z ]+$/.test(city)
            ) {

                alert(
                    "City must contain letters and spaces only."
                );

                return;
            }


            if (
                !/^[A-Za-z ]+$/.test(department)
            ) {

                alert(
                    "Department must contain letters and spaces only."
                );

                return;
            }


            try {

                const response =
                    await fetch(
                        "/api/students",
                        {

                            method: "POST",

                            headers: {
                                "Content-Type":
                                    "application/json"
                            },

                            body: JSON.stringify({

                                name: name,

                                age: studentAge,

                                gender: gender,

                                city: city,

                                department:
                                    department

                            })

                        }
                    );


                const result =
                    await response.json();


                if (!response.ok) {

                    alert(
                        result.message ||
                        "Failed to add student."
                    );

                    return;
                }


                document.getElementById(
                    "success-message"
                ).textContent =
                    result.message;


                studentForm.reset();


                loadStudents();

            }

            catch (error) {

                console.error(error);

                alert(
                    "Unable to connect to Flask server."
                );

            }

        }
    );
}


// ===============================
// SEARCH BY NAME
// ===============================

const searchButton =
    document.getElementById(
        "search-btn"
    );


if (searchButton) {

    searchButton.addEventListener(
        "click",
        async function() {

            const searchValue =
                document.getElementById(
                    "search-input"
                ).value.trim();


            const result =
                document.getElementById(
                    "search-result"
                );


            if (searchValue === "") {

                result.innerHTML =
                    "<p>Please enter a student name.</p>";

                return;
            }


            try {

                const response =
                    await fetch(
                        `/api/students/search?name=${encodeURIComponent(searchValue)}`
                    );


                const students =
                    await response.json();


                if (!response.ok) {

                    result.innerHTML =
                        `<p>${students.message}</p>`;

                    return;
                }


                if (students.length === 0) {

                    result.innerHTML =
                        "<p>Student not found.</p>";

                    return;
                }


                result.innerHTML = "";


                students.forEach(
                    function(student) {

                        result.innerHTML += `

                            <div class="card">

                                <h3>
                                    ${student.name}
                                </h3>

                                <p>
                                    ID:
                                    ${student.student_id}
                                </p>

                                <p>
                                    Age:
                                    ${student.age}
                                </p>

                                <p>
                                    Gender:
                                    ${student.gender}
                                </p>

                                <p>
                                    City:
                                    ${student.city}
                                </p>

                                <p>
                                    Department:
                                    ${student.department}
                                </p>

                            </div>

                        `;

                    }
                );

            }

            catch (error) {

                console.error(error);

                result.innerHTML =
                    "<p>Unable to connect to server.</p>";

            }

        }
    );
}


// ===============================
// SEARCH BY ID
// ===============================

const searchIdButton =
    document.getElementById(
        "search-id-btn"
    );


if (searchIdButton) {

    searchIdButton.addEventListener(
        "click",
        async function() {

            const id =
                Number(
                    document.getElementById(
                        "search-id"
                    ).value
                );


            const result =
                document.getElementById(
                    "search-result"
                );


            if (!id || id <= 0) {

                result.innerHTML =
                    "<p>Please enter a valid student ID.</p>";

                return;
            }


            try {

                const response =
                    await fetch(
                        `/api/students/${id}`
                    );


                const student =
                    await response.json();


                if (!response.ok) {

                    result.innerHTML =
                        `<p>${student.message}</p>`;

                    return;
                }


                result.innerHTML = `

                    <div class="card">

                        <h3>
                            ${student.name}
                        </h3>

                        <p>
                            ID:
                            ${student.student_id}
                        </p>

                        <p>
                            Age:
                            ${student.age}
                        </p>

                        <p>
                            Gender:
                            ${student.gender}
                        </p>

                        <p>
                            City:
                            ${student.city}
                        </p>

                        <p>
                            Department:
                            ${student.department}
                        </p>

                    </div>

                `;

            }

            catch (error) {

                console.error(error);

                result.innerHTML =
                    "<p>Unable to connect to server.</p>";

            }

        }
    );
}


// ===============================
// UPDATE STUDENT
// ===============================

const updateButton =
    document.getElementById(
        "update-btn"
    );


if (updateButton) {

    updateButton.addEventListener(
        "click",
        async function() {

            const id =
                Number(
                    document.getElementById(
                        "update-id"
                    ).value
                );


            const name =
                document.getElementById(
                    "update-name"
                ).value.trim();


            const age =
                Number(
                    document.getElementById(
                        "update-age"
                    ).value
                );


            const gender =
                document.getElementById(
                    "update-gender"
                ).value;


            const city =
                document.getElementById(
                    "update-city"
                ).value.trim();


            const department =
                document.getElementById(
                    "update-department"
                ).value.trim();


            const message =
                document.getElementById(
                    "update-message"
                );


            if (!id || id <= 0) {

                message.textContent =
                    "Please enter a valid student ID.";

                return;
            }


            if (
                name === "" ||
                !age ||
                gender === "" ||
                city === "" ||
                department === ""
            ) {

                message.textContent =
                    "Please fill all fields.";

                return;
            }


            if (
                age < 5 ||
                age > 100
            ) {

                message.textContent =
                    "Age must be between 5 and 100.";

                return;
            }


            try {

                const response =
                    await fetch(
                        `/api/students/${id}`,
                        {

                            method: "PUT",

                            headers: {
                                "Content-Type":
                                    "application/json"
                            },

                            body: JSON.stringify({

                                name: name,

                                age: age,

                                gender: gender,

                                city: city,

                                department:
                                    department

                            })

                        }
                    );


                const result =
                    await response.json();


                if (!response.ok) {

                    message.textContent =
                        result.message;

                    return;
                }


                message.textContent =
                    result.message;


                document.getElementById(
                    "update-id"
                ).value = "";


                document.getElementById(
                    "update-name"
                ).value = "";


                document.getElementById(
                    "update-age"
                ).value = "";


                document.getElementById(
                    "update-gender"
                ).value = "";


                document.getElementById(
                    "update-city"
                ).value = "";


                document.getElementById(
                    "update-department"
                ).value = "";


                loadStudents();

            }

            catch (error) {

                console.error(error);

                message.textContent =
                    "Unable to connect to server.";

            }

        }
    );
}


// ===============================
// DELETE STUDENT
// ===============================

const deleteButton =
    document.getElementById(
        "delete-btn"
    );


if (deleteButton) {

    deleteButton.addEventListener(
        "click",
        async function() {

            const id =
                Number(
                    document.getElementById(
                        "delete-id"
                    ).value
                );


            const message =
                document.getElementById(
                    "delete-message"
                );


            if (!id || id <= 0) {

                message.textContent =
                    "Please enter a valid student ID.";

                return;
            }


            const confirmation =
                confirm(
                    "Are you sure you want to delete this student?"
                );


            if (!confirmation) {
                return;
            }


            try {

                const response =
                    await fetch(
                        `/api/students/${id}`,
                        {
                            method: "DELETE"
                        }
                    );


                const result =
                    await response.json();


                if (!response.ok) {

                    message.textContent =
                        result.message;

                    return;
                }


                message.textContent =
                    result.message;


                document.getElementById(
                    "delete-id"
                ).value = "";


                loadStudents();

            }

            catch (error) {

                console.error(error);

                message.textContent =
                    "Unable to connect to server.";

            }

        }
    );
}


// ===============================
// INITIAL LOAD
// ===============================

loadStudents();