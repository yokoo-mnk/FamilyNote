document.addEventListener("DOMContentLoaded", function() {
    const selectAllCheckbox = document.getElementById("select-all");
    const checkboxes = document.querySelectorAll(".task-checkbox");
    const deleteBtn = document.getElementById("delete-btn");
    const modal = document.getElementById("delete-modal");
    const selectedList = document.getElementById("selected-tasks-list");
    const confirmDelete = document.getElementById("confirm-delete");
    const closeModal = document.getElementById("close-modal");

    let selectedTasks = [];

    selectAllCheckbox.addEventListener("change", function() {
        checkboxes.forEach(checkbox => {
            checkbox.checked = selectAllCheckbox.checked;
        });

        updateSelectedTasks();
    });

    checkboxes.forEach(checkbox => {
        checkbox.addEventListener("change", function() {
            if (!this.checked) {
                selectAllCheckbox.checked = false; // 1つでも外れたら全選択をオフ
            } else if (Array.from(checkboxes).every(c => c.checked)) {
                selectAllCheckbox.checked = true; // 全部チェックされたら全選択をオン
            }

            updateSelectedTasks(); // 状態を更新
        });
    });

    function updateSelectedTasks() {
        const selectedTasks = Array.from(checkboxes)
            .filter(c => c.checked)
            .map(c => ({ id: c.value, title: c.dataset.title }));

        const deleteBtn = document.getElementById("delete-btn");
        deleteBtn.disabled = selectedTasks.length === 0;
    };

    deleteBtn.addEventListener("click", function() {
        selectedTasks = Array.from(document.querySelectorAll(".task-checkbox:checked"))
        .map(c => ({ id: c.value, title: c.dataset.title }));

        console.log(selectedTasks);

        selectedList.innerHTML = "";
        selectedTasks.forEach(task => {
            const li = document.createElement("li");
            li.textContent = task.title;
            selectedList.appendChild(li);
        });
        modal.style.display = "flex";
    });

    closeModal.addEventListener("click", function() {
        modal.style.display = "none";
    });
    
    window.addEventListener("click", function (event) {
        if (event.target === modal) {
            modal.style.display = "none";
        }
    });

    confirmDelete.addEventListener("click", function() {
        const formData = new FormData();
        selectedTasks.forEach(letter => {
            formData.append("delete_task", letter.id);
        });

        fetch("/tasks/task_delete/", {
            method: "POST",
            body: formData,
            headers: {
                "X-CSRFToken": getCsrfToken()
            }
        })
        .then(response => {
            console.log("Raw Response:", response); // レスポンスをデバッグ

            // リダイレクトされている場合、ログインページへ移動
            if (response.redirected) {
                window.location.href = response.url;
                return;
            }

            return response.json();  // JSONに変換
        })
        .then(data => {
            if (data.success) {
                window.location.href = "/tasks/task_list/";
            } else {
                alert("削除に失敗しました：" + (data.error || "不明なエラー"));
            }
        })
        .catch(error => {
            console.error("削除エラー:", error);
            alert("通信エラーが発生しました。");
        });
    });

    function getCsrfToken() {
        return document.querySelector("[name=csrfmiddlewaretoken]").value;
    }
});





// document.getElementById("selectAll").addEventListener("change", function() {
//     let checkboxes = document.querySelectorAll(".taskCheckbox");
//     checkboxes.forEach(cb => cb.checked = this.checked);
//     toggleDeleteButton();
// });

// document.querySelectorAll(".taskCheckbox").forEach(cb => {
//     cb.addEventListener("change", toggleDeleteButton);
// });

// function toggleDeleteButton() {
//     let checked = document.querySelectorAll(".taskCheckbox:checked").length > 0;
//     document.getElementById("deleteButton").disabled = !checked;
// }

// function openModal() {
//     let selectedTasks = document.querySelectorAll(".taskCheckbox:checked");
//     let taskList = document.getElementById("tasks:taskList");
//     taskList.innerHTML = "";

//     selectedTasks.forEach(task => {
//         let title = task.closest("tr").querySelector("td:nth-child(2)").textContent;
//         let li = document.createElement("li");
//         li.textContent = title;
//         taskList.appendChild(li);
//     });

//     document.getElementById("deleteModal").style.display = "flex";
// }

// function closeModal() {
//     document.getElementById("deleteModal").style.display = "none";
// }