document.addEventListener("DOMContentLoaded", function() {
    const selectAllCheckbox = document.getElementById("select-all");
    const isHomePage = document.body.classList.contains("home-page");
    const isTaskListPage = document.body.classList.contains("task-list-page");
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

    document.querySelectorAll('.task-checkbox').forEach(checkbox => {
        checkbox.addEventListener("change", function() {
            
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
                    alert("完了状態の保存に失敗しました：" + (data.error || ""));
                }
            })
            .catch(error => {
                console.error("完了状態の保存エラー:", error);
            });

            const row = this.closest("tr");
            if (isHomePage) {
            // 完了状態に基づいて行に線を引く/外す
                if (this.checked) {
                    row.classList.add("completed"); // チェックされたら線を引く
                } else {
                    row.classList.remove("completed"); // チェックが外れたら線を外す
               }
            }

            updateSelectedTasks(); // タスク選択状態を更新
        });
    });
    
    document.querySelectorAll('.show-on-home-checkbox').forEach(checkbox => {
        checkbox.addEventListener('change', function() {
            const taskId = this.value;
    
            // `is_completed` を変更しないように、show_on_home のみを変更
            fetch('/tasks/toggle_show_on_home/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'X-CSRFToken': getCsrfToken()
                },
                body: `task_id=${taskId}&show_on_home=${this.checked}`
            })
            .then(response => response.json())
            .then(data => {
                if (!data.success) {
                    alert('ホーム画面表示設定の保存に失敗しました: ' + (data.error || ''));
                }
            })
            .catch(error => {
                console.error('エラー:', error);
                alert('通信エラーが発生しました');
            });
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

    
    document.querySelectorAll('.assign-member').forEach(select => {
        select.addEventListener('change', function () {
            const taskId = this.dataset.taskId;
            const userId = this.value;
    
            fetch('/tasks/assign_task_member/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCsrfToken()
                },
                body: JSON.stringify({ task_id: taskId, user_id: userId })
            })
    
            .then(response => response.json())
            .then(data => {
                if (!data.success) {
                    alert("担当者の更新に失敗しました: " + (data.error || ""));
                }
            })
            .catch(error => {
                console.error("エラー:", error);
                alert("通信エラーが発生しました");
            });
        });
    });
});