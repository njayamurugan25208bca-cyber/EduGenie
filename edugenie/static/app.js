const task =
    document.getElementById("task");

const levelWrap =
    document.getElementById("level-wrap");

const level =
    document.getElementById("level");

const inputText =
    document.getElementById("inputText");

const submitBtn =
    document.getElementById("submitBtn");

const clearBtn =
    document.getElementById("clearBtn");

const result =
    document.getElementById("result");

const statusEl =
    document.getElementById("status");

const hint =
    document.getElementById("hint");


const hints = {

    qa:
        "Example: Which is the largest ocean?",

    explain:
        "Example: Explain Pythagoras theorem",

    quiz:
        "Paste a passage to generate MCQs.",

    summarize:
        "Paste an educational passage.",

    learn:
        "Example: Learn SQL"
};


function updateForm() {

    const showLevel =
        task.value === "explain" ||
        task.value === "learn";

    levelWrap.classList.toggle(
        "hidden",
        !showLevel
    );

    hint.textContent =
        hints[task.value];
}


task.addEventListener(
    "change",
    updateForm
);


clearBtn.addEventListener(
    "click",
    () => {

        inputText.value = "";

        result.className =
            "result empty";

        result.innerHTML =
            `
            <div class="empty-icon">
                ✦
            </div>

            <p>
                Your result will appear here.
            </p>
            `;

        statusEl.textContent =
            "Ready";
    }
);


function escapeHtml(value) {

    return value.replace(
        /[&<>"']/g,
        character => ({

            "&": "&amp;",

            "<": "&lt;",

            ">": "&gt;",

            '"': "&quot;",

            "'": "&#039;"

        }[character])
    );
}


async function runTask() {

    const text =
        inputText.value.trim();

    if (!text) {

        alert(
            "Please enter your input."
        );

        return;
    }


    submitBtn.disabled =
        true;

    statusEl.textContent =
        "Working...";


    result.className =
        "result";

    result.innerHTML =
        `
        <p>
            EduGenie is preparing
            your response...
        </p>
        `;


    let endpoint;

    let payload;


    if (task.value === "qa") {

        endpoint = "/qa";

        payload = {
            question: text
        };

    }

    else if (
        task.value === "explain"
    ) {

        endpoint = "/explain";

        payload = {

            topic: text,

            level:
                level.value
        };

    }

    else if (
        task.value === "quiz"
    ) {

        endpoint = "/quiz";

        payload = {

            text: text,

            count: 3
        };

    }

    else if (
        task.value === "summarize"
    ) {

        endpoint = "/summarize";

        payload = {

            text: text
        };

    }

    else {

        endpoint =
            "/learn/recommendations";

        payload = {

            topic: text,

            level:
                level.value
        };
    }


    try {

        const response =
            await fetch(
                endpoint,
                {

                    method:
                        "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body:
                        JSON.stringify(
                            payload
                        )
                }
            );


        const data =
            await response.json();


        if (!response.ok) {

            throw new Error(
                data.detail ||
                "Request failed."
            );
        }


        if (
            task.value === "quiz"
        ) {

            renderQuiz(
                data.questions
            );

        }

        else {

            let key;


            if (
                task.value === "qa"
            ) {

                key = "answer";

            }

            else if (
                task.value === "explain"
            ) {

                key = "explanation";

            }

            else if (
                task.value === "summarize"
            ) {

                key = "summary";

            }

            else {

                key = "learning_path";
            }


            result.innerHTML =
                `
                <div class="answer">
                    ${escapeHtml(
                        data[key]
                    )}
                </div>
                `;
        }


        statusEl.textContent =
            "Complete";

    }

    catch (error) {

        result.innerHTML =
            `
            <div class="answer">

                <strong>
                    Something went wrong.
                </strong>

                <br><br>

                ${escapeHtml(
                    error.message
                )}

            </div>
            `;

        statusEl.textContent =
            "Error";

    }

    finally {

        submitBtn.disabled =
            false;
    }
}


function renderQuiz(
    questions
) {

    result.innerHTML =
        `
        <div
            class="quiz-score"
            id="score"
        >
            Score: 0 /
            ${questions.length}
        </div>

        ${
            questions.map(
                (question, index) => `

                <article
                    class="quiz-question"
                >

                    <h3>
                        ${index + 1}.
                        ${escapeHtml(
                            question.question
                        )}
                    </h3>

                    ${
                        question.options.map(
                            option => `

                            <label
                                class="option"
                            >

                                <input
                                    type="radio"
                                    name="q${index}"
                                    value="${escapeHtml(option)}"
                                >

                                ${escapeHtml(
                                    option
                                )}

                            </label>

                            `
                        ).join("")
                    }

                    <button
                        class="secondary check-answer"
                        type="button"
                    >
                        Check Answer
                    </button>

                    <div
                        class="feedback"
                        hidden
                    ></div>

                </article>
                `
            ).join("")
        }
        `;


    let score = 0;

    const answered =
        new Set();


    result
        .querySelectorAll(
            ".quiz-question"
        )
        .forEach(
            (card, index) => {

                card
                    .querySelector(
                        ".check-answer"
                    )
                    .addEventListener(
                        "click",
                        () => {

                            if (
                                answered.has(
                                    index
                                )
                            ) {

                                return;
                            }


                            const selected =
                                card.querySelector(
                                    `input[name="q${index}"]:checked`
                                );


                            const feedback =
                                card.querySelector(
                                    ".feedback"
                                );


                            if (!selected) {

                                feedback.hidden =
                                    false;

                                feedback.className =
                                    "feedback wrong";

                                feedback.textContent =
                                    "Choose an option first.";

                                return;
                            }


                            answered.add(
                                index
                            );


                            const correct =
                                questions[index]
                                    .correct_answer;


                            const isCorrect =
                                selected.value ===
                                correct;


                            if (isCorrect) {

                                score++;

                                feedback.className =
                                    "feedback correct";

                                feedback.textContent =
                                    "Correct! " +
                                    questions[index]
                                        .explanation;

                            }

                            else {

                                feedback.className =
                                    "feedback wrong";

                                feedback.textContent =
                                    "Correct answer: " +
                                    correct +
                                    ". " +
                                    questions[index]
                                        .explanation;
                            }


                            feedback.hidden =
                                false;


                            card
                                .querySelectorAll(
                                    "input"
                                )
                                .forEach(
                                    input =>
                                        input.disabled =
                                            true
                                );


                            card
                                .querySelector(
                                    ".check-answer"
                                )
                                .disabled =
                                    true;


                            document
                                .getElementById(
                                    "score"
                                )
                                .textContent =
                                    `Score: ${score} / ${questions.length}`;
                        }
                    );
            }
        );
}


submitBtn.addEventListener(
    "click",
    runTask
);


inputText.addEventListener(
    "keydown",
    event => {

        if (
            (event.ctrlKey ||
             event.metaKey) &&
            event.key === "Enter"
        ) {

            runTask();
        }
    }
);


updateForm();