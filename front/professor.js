

const API_URL =
    window.location.hostname === "localhost" ||
    window.location.hostname === "127.0.0.1"
        ? "http://127.0.0.1:8000"
        : "";

let currentProfessor = null;


// ============================
// ورود استاد
// ============================

document
    .getElementById("professorLoginForm")
    .addEventListener("submit", async function (event) {

        event.preventDefault();

        const personalCode =
            document.getElementById("professorCode").value.trim();

        const message =
            document.getElementById("professorMessage");

        message.textContent = "";

        try {

            const response = await fetch(
                `${API_URL}/professors/`
            );

            if (!response.ok) {
                throw new Error("خطا در دریافت اطلاعات استادها");
            }

            const professors = await response.json();

            const professor = professors.find(
                p => String(p.personal_code) === personalCode
            );

            if (!professor) {

                message.textContent =
                    "استادی با این کد پرسنلی پیدا نشد.";

                return;
            }

            currentProfessor = professor;


            // مخفی کردن صفحه ورود
            document.getElementById(
                "professorLoginPage"
            ).style.display = "none";


            // نمایش پنل استاد
            document.getElementById(
                "professorDashboard"
            ).style.display = "block";


            // اطلاعات استاد
            document.getElementById(
                "professorName"
            ).textContent = professor["full name"];


            document.getElementById(
                "professorCodeInfo"
            ).textContent = professor.personal_code;


            document.getElementById(
                "professorDepartment"
            ).textContent = professor.department;


            // دریافت درس‌ها
            await loadAvailableProfessorCourses();

            loadProfessorCourses(professor);

        } catch (error) {

            console.error("ERROR:", error);

            message.textContent =
                "ارتباط با سرور برقرار نشد.";
        }

    });


// ============================
// نمایش تمام درس‌ها
// ============================

async function loadAvailableProfessorCourses() {

    const container =
        document.getElementById(
            "availableProfessorCourses"
        );

    try {

        const response = await fetch(
            `${API_URL}/courses/`
        );

        if (!response.ok) {
            throw new Error("خطا در دریافت درس‌ها");
        }

        const courses = await response.json();

        container.innerHTML = "";


        if (courses.length === 0) {

            container.innerHTML = `
                <div class="empty-courses">
                    درسی برای انتخاب وجود ندارد.
                </div>
            `;

            return;
        }


        courses.forEach(course => {

            const card =
                document.createElement("div");

            card.className = "course-card";


            let professorName =
                "استاد تعیین نشده";


            if (course.professor) {

                professorName =
                    `${course.professor.first_name} ${course.professor.last_name}`;

            }


            card.innerHTML = `

                <div class="course-content">

                    <h3>
                        ${course.title}
                    </h3>

                    <div class="course-details">

                        <span>
                            کد درس: ${course.code}
                        </span>

                        <span>
                            ${course.units} واحد
                        </span>

                        <span>
                            استاد: ${professorName}
                        </span>

                    </div>

                    <button
                        class="assign-course-button"
                        onclick="assignCourse(${course.id})"
                        ${course.professor ? "disabled" : ""}>

                        ${
                            course.professor
                                ? "درس دارای استاد است"
                                : "اختصاص به من"
                        }

                    </button>

                </div>

            `;

            container.appendChild(card);

        });


    } catch (error) {

        console.error(
            "خطا در دریافت درس‌ها:",
            error
        );

        container.innerHTML = `
            <div class="empty-courses">
                دریافت درس‌ها با خطا مواجه شد.
            </div>
        `;

    }

}


// ============================
// نمایش درس‌های استاد
// ============================

function loadProfessorCourses(professor) {

    const container =
        document.getElementById(
            "professorCourses"
        );

    container.innerHTML = "";


    if (
        !professor.courses ||
        professor.courses.length === 0
    ) {

        container.innerHTML = `
            <div class="empty-courses">
                هنوز درسی به شما اختصاص داده نشده است.
            </div>
        `;

        return;
    }


    professor.courses.forEach(course => {

        const card =
            document.createElement("div");

        card.className = "course-card";


        card.innerHTML = `

            <div class="course-content">

                <h3>
                    ${course.title}
                </h3>

                <div class="course-details">

                    <span>
                        کد درس: ${course.code}
                    </span>

                    <span>
                        ${course.units} واحد
                    </span>

                </div>

                <button
                    class="view-students-button"
                    onclick="viewCourseStudents(${course.id})">

                    مشاهده دانشجویان
                </button>

            </div>

        `;

        container.appendChild(card);

    });

}


// ============================
// اختصاص درس به استاد
// ============================

async function assignCourse(courseId) {

    if (!currentProfessor) {
        return;
    }


    try {

        const response = await fetch(
            `${API_URL}/courses/${courseId}/professors/${currentProfessor.id}`,
            {
                method: "POST"
            }
        );


        const result = await response.json();


        if (!response.ok) {

            alert(
                result.message ||
                result.Message ||
                "اختصاص درس انجام نشد."
            );

            return;
        }


        alert(
            result.message ||
            result.Message ||
            "درس با موفقیت به شما اختصاص داده شد."
        );


        // دریافت اطلاعات جدید استاد
        const professorsResponse =
            await fetch(
                `${API_URL}/professors/`
            );


        const professors =
            await professorsResponse.json();


        currentProfessor =
            professors.find(
                professor =>
                    professor.id === currentProfessor.id
            );


        // بروزرسانی درس‌های استاد
        loadProfessorCourses(
            currentProfessor
        );


        // بروزرسانی لیست درس‌ها
        loadAvailableProfessorCourses();

    } catch (error) {

        console.error(
            "ERROR:",
            error
        );

        alert(
            "ارتباط با سرور برقرار نشد."
        );

    }

}


async function viewCourseStudents(courseId) {

    const section =
        document.getElementById(
            "courseStudentsSection"
        );

    const container =
        document.getElementById(
            "courseStudents"
        );

    const title =
        document.getElementById(
            "selectedCourseTitle"
        );


    section.style.display = "block";

    container.innerHTML = `
        <div class="empty-courses">
            در حال بارگذاری دانشجویان...
        </div>
    `;


    try {

        const response = await fetch(
            `${API_URL}/courses/${courseId}`
        );


        if (!response.ok) {

            throw new Error(
                "خطا در دریافت اطلاعات درس"
            );

        }


        const course =
            await response.json();


        title.textContent =
            `${course.title} | ${course.code}`;


        container.innerHTML = "";


        if (
            !course.students ||
            course.students.length === 0
        ) {

            container.innerHTML = `
                <div class="empty-courses">
                    هنوز دانشجویی این درس را انتخاب نکرده است.
                </div>
            `;

            return;
        }


        course.students.forEach(student => {

            const card =
                document.createElement("div");


            card.className =
                "course-card";


            card.innerHTML = `

                <div class="course-content">

                    <h3>
                        ${student.first_name}
                        ${student.last_name}
                    </h3>

                    <div class="course-details">

                        <span>
                            شماره دانشجویی:
                            ${student.student_number}
                        </span>

                    </div>

                </div>

            `;


            container.appendChild(card);

        });


    } catch (error) {

        console.error(
            "ERROR:",
            error
        );


        container.innerHTML = `
            <div class="empty-courses">
                دریافت لیست دانشجویان با خطا مواجه شد.
            </div>
        `;

    }

}


// ============================
// خروج استاد
// ============================

function professorLogout() {

    currentProfessor = null;


    document.getElementById(
        "professorDashboard"
    ).style.display = "none";


    document.getElementById(
        "professorLoginPage"
    ).style.display = "block";


    document.getElementById(
        "professorCode"
    ).value = "";


    document.getElementById(
        "professorMessage"
    ).textContent = "";


    // Redirect to landing page
    window.location.href = "landing.html";

}
