const API_URL =
    window.location.hostname === "localhost" ||
    window.location.hostname === "127.0.0.1"
        ? "http://127.0.0.1:8000"
        : "";

const loginForm = document.getElementById("loginForm");

const message = document.getElementById("message");

const loginPage = document.getElementById("loginPage");

const dashboardPage = document.getElementById("dashboardPage");


let currentStudent = null;



loginForm.addEventListener("submit", async function (event) {

    event.preventDefault();


    const studentNumber =
        document.getElementById("studentNumber").value.trim();


    if (!studentNumber) {

        message.textContent =
            "لطفاً شماره دانشجویی را وارد کنید.";

        message.style.color = "#f87171";

        return;
    }


    message.textContent =
        "در حال بررسی...";

    message.style.color = "#94a3b8";


    try {

       const response =
            await fetch(`${API_URL}/students/`);


        if (!response.ok) {

            throw new Error(
                `HTTP Error: ${response.status}`
            );

        }


        const students =
            await response.json();


        const student =
            students.find(
                student =>
                    student.student_number === studentNumber
            );


        if (!student) {

            message.textContent =
                "دانشجویی با این شماره دانشجویی پیدا نشد.";

            message.style.color = "#f87171";

            return;
        }


        currentStudent = student;


        showDashboard(student);


    } catch (error) {

        console.error(error);


        message.textContent =
            "خطا در ارتباط با سرور.";

        message.style.color = "#f87171";

    }

});



function showDashboard(student) {

    loginPage.style.display = "none";

    dashboardPage.style.display = "block";


    document.getElementById("studentName").textContent =
        student["full name"];


    document.getElementById("studentNumberInfo").textContent =
        student.student_number;


    document.getElementById("studentMajor").textContent =
        student.major;


    loadStudentCourses(student.id);
    loadAvailableCourses();

}



async function loadStudentCourses(studentId) {

    const coursesContainer =
        document.getElementById("selectedCourses");


    try {

        const response =
            await fetch(
                `${API_URL}/students/${studentId}/courses`
            );


        if (!response.ok) {

            throw new Error(
                `HTTP Error: ${response.status}`
            );

        }


        const courses =
            await response.json();


        if (courses.length === 0) {

            coursesContainer.innerHTML = `
                <div class="empty-courses">
                    هنوز درسی انتخاب نکرده‌اید.
                </div>
            `;

            return;
        }


            coursesContainer.innerHTML = "";


            courses.forEach(course => {

                const courseCard =
                    document.createElement("div");


                courseCard.className =
                    "course-card";


                courseCard.innerHTML = `
        <div>
            <div class="course-title">
                ${course.title}
            </div>

            <div class="course-details">
                <span>کد: ${course.code}</span>
                <span>${course.unit} واحد</span>
            </div>
        </div>

        <button
            class="remove-course-button"
            onclick="dropCourse(${course.id})">
            حذف درس
        </button>
    `;


            coursesContainer.appendChild(courseCard);

        });


    } catch (error) {

        console.error(
            "خطا در دریافت درس‌ها:",
            error
        );


        coursesContainer.innerHTML = `
            <div class="empty-courses">
                دریافت درس‌های دانشجو با خطا مواجه شد.
            </div>
        `;

    }

}



function logout() {

    currentStudent = null;


    dashboardPage.style.display = "none";

    loginPage.style.display = "block";


    document.getElementById("studentNumber").value = "";

    message.textContent = "";

}
async function loadAvailableCourses() {

    const coursesContainer =
        document.getElementById("availableCourses");

    try {

        const response = await fetch(
            `${API_URL}/courses/`
        );

        if (!response.ok) {
            throw new Error(
                `HTTP Error: ${response.status}`
            );
        }

        const courses = await response.json();

        coursesContainer.innerHTML = "";


        if (courses.length === 0) {

            coursesContainer.innerHTML = `
                <div class="empty-courses">
                    در حال حاضر هیچ درسی ارائه نشده است.
                </div>
            `;

            return;
        }


        courses.forEach((course, index) => {

            const courseCard =
                document.createElement("div");

            courseCard.className = "course-card";

            courseCard.style.animationDelay =
                `${index * 0.08}s`;


            courseCard.innerHTML = `

                <div>

                    <div class="course-title">
                        ${course.title}
                    </div>

                    <div class="course-details">

                        <span>
                            کد: ${course.code}
                        </span>

                        <span>
                            ${course.units} واحد
                        </span>

                        <span>
                            ظرفیت باقی‌مانده:
                            ${course.remaining_capacity}
                        </span>
                        <span>
                            استاد:
                            ${
                                 course.professor
                                    ? `${course.professor.first_name} ${course.professor.last_name}`
                                    : "استاد تعیین نشده"
                            }
                        </span>
                    </div>

                </div>

                <button
                    class="login-button"
                    onclick="selectCourse(${course.id})">

                    انتخاب درس

                </button>

            `;


            coursesContainer.appendChild(courseCard);

        });


    } catch (error) {

        console.error(
            "خطا در دریافت دروس:",
            error
        );

        coursesContainer.innerHTML = `
            <div class="empty-courses">
                دریافت لیست دروس با خطا مواجه شد.
            </div>
        `;
    }
}

async function selectCourse(courseId) {

    if (!currentStudent) {
        alert("اطلاعات دانشجو پیدا نشد.");
        return;
    }

    try {

        const response = await fetch(
            `${API_URL}/students/${currentStudent.id}/courses/${courseId}`,
            {
                method: "POST"
            }
        );

        const result = await response.json();


        // اگر Backend خطا برگرداند
        if (!response.ok) {

            const errorMessage =
                result.message ||
                result.Message ||
                "انتخاب درس انجام نشد.";

            alert(errorMessage);

            return;
        }


        // انتخاب موفق
        showToast(
    result.message ||
    "درس با موفقیت انتخاب شد."
    );


        // دوباره درس‌های انتخاب‌شده را دریافت کن
        await loadStudentCourses(currentStudent.id);


        // دوباره لیست دروس را دریافت کن
        await loadAvailableCourses();


    } catch (error) {

        console.error(
            "خطا در انتخاب درس:",
            error
        );

        alert(
            "ارتباط با سرور برقرار نشد."
        );
    }
}

async function dropCourse(courseId) {

    if (!currentStudent) {
        alert("اطلاعات دانشجو پیدا نشد.");
        return;
    }

    try {

        const response = await fetch(
            `${API_URL}/students/${currentStudent.id}/courses/${courseId}`,
            {
                method: "DELETE"
            }
        );

        const result = await response.json();

        if (!response.ok) {
            showToast(
                result.message ||
                result.Message ||
                "حذف درس انجام نشد."
            );
            return;
        }

        showToast(
            result.message ||
            result.Message ||
            "درس با موفقیت حذف شد."
        );

        await loadStudentCourses(currentStudent.id);
        await loadAvailableCourses();

    } catch (error) {

        console.error("خطا در حذف درس:", error);

        alert("ارتباط با سرور برقرار نشد.");
    }
}
document.getElementById("courseSearch").addEventListener("input", function () {

    const searchText = this.value.trim().toLowerCase();

    const courseCards = document.querySelectorAll(
        "#availableCourses .course-card"
    );

    courseCards.forEach(card => {

        const text = card.textContent.toLowerCase();

        if (text.includes(searchText)) {
            card.style.display = "";
        } else {
            card.style.display = "none";
        }

    });

});
function showToast(message) {

    const toast = document.getElementById("toast");

    toast.textContent = message;

    toast.classList.add("show");

    setTimeout(() => {
        toast.classList.remove("show");
    }, 2500);
}
