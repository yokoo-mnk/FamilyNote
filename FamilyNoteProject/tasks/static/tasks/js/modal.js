document.addEventListener("DOMContentLoaded", function() {
    const selectAllCheckbox = document.getElementById("select-all");
    const isHomePage = document.body.classList.contains("home-page");
    const checkboxes = document.querySelectorAll(".task-checkbox");
    const deleteBtn = document.getElementById("delete-btn");
    const modal = document.getElementById("delete-modal");
    const selectedList = document.getElementById("selected-tasks-list");
    const confirmDelete = document.getElementById("confirm-delete");
    const closeModal = document.getElementById("close-modal");
    const taskDeleteEndpoint = document.getElementById("task-delete-endpoint");
    const homeTaskRemoveEndpoint = document.getElementById("home-task-remove-endpoint");

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
            
            const row = this.closest("tr");
            if (isHomePage) {
                // ホーム画面の場合、チェックボックスの状態に基づいて行に線を引く
                if (this.checked) {
                    row.classList.add("completed"); // チェックされたら線を引く
                } else {
                    row.classList.remove("completed"); // チェックが外れたら線を外す
                }
            }

            fetch("/tasks/toggle_completion/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/x-www-form-urlencoded",
                    "X-CSRFToken": getCsrfToken()
                },
                body: `task_id=${this.value}&is_completed=${this.checked}`
            })
            .then(response => response.json())
            .then(data => {
                if (!data.success) {
                    alert("チェック状態の保存に失敗しました：" + (data.error || ""));
                }
            })
            .catch(error => {
                console.error("チェック状態の保存エラー:", error);
            });
        
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
        let endpoint = null;

        if (taskDeleteEndpoint) {
            endpoint = taskDeleteEndpoint.value;
        } else if (homeTaskRemoveEndpoint) {
            endpoint = homeTaskRemoveEndpoint.value;
        } else {
            console.error("エンドポイントが見つかりません");
            return;
        }
        
        // 削除処理を行う
        console.log("エンドポイント:", endpoint);

        const formData = new FormData();
        selectedTasks.forEach(task => {
            formData.append("tasks", task.id);
        });

        fetch(endpoint, {
            method: "POST",
            body: formData,
            headers: {
                "X-CSRFToken": getCsrfToken()
            }
        })
        .then(response => {
            console.log("Raw Response:", response);

            if (response.redirected) {
                window.location.href = response.url;
                return;
            }

            return response.json();
        })
        .then(data => {
            if (data.success) {
                if (endpoint.includes("home_task_remove")) {
                    window.location.href = "/tasks/home/?sort_order=" + getSortOrder();
                } else {
                    window.location.href = "/tasks/task_list/?sort_order=" + getSortOrder();
                }
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

    function getSortOrder() {
        const sortOrderSelect = document.querySelector("[name=sort_order]");
        return sortOrderSelect ? sortOrderSelect.value : "newest";  // デフォルトは新しい順
    }
});