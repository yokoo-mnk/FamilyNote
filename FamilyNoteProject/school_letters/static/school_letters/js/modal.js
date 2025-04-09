document.addEventListener("DOMContentLoaded", function() {
    const selectAllCheckbox = document.getElementById("select-all");
    const checkboxes = document.querySelectorAll(".letter-checkbox");
    const deleteBtn = document.getElementById("delete-btn");
    const modal = document.getElementById("delete-modal");
    const selectedList = document.getElementById("selected-letters-list");
    const confirmDelete = document.getElementById("confirm-delete");
    const closeModal = document.getElementById("close-modal");

    let selectedLetters = [];

    selectAllCheckbox.addEventListener("change", function() {
        checkboxes.forEach(checkbox => {
            checkbox.checked = selectAllCheckbox.checked;
        });

        updateSelectedLetters();
    });

    checkboxes.forEach(checkbox => {
        checkbox.addEventListener("change", function() {
            if (!this.checked) {
                selectAllCheckbox.checked = false; // 1つでも外れたら全選択をオフ
            } else if (Array.from(checkboxes).every(c => c.checked)) {
                selectAllCheckbox.checked = true; // 全部チェックされたら全選択をオン
            }

            updateSelectedLetters(); // 状態を更新
        });
    });

    function updateSelectedLetters() {
        const selectedLetters = Array.from(checkboxes)
            .filter(c => c.checked)
            .map(c => ({ id: c.value, title: c.dataset.title }));

        const deleteBtn = document.getElementById("delete-btn");
        deleteBtn.disabled = selectedLetters.length === 0;
    };

    deleteBtn.addEventListener("click", function() {
        selectedLetters = Array.from(document.querySelectorAll(".letter-checkbox:checked"))
        .map(c => ({
            id: c.value,
            title: c.dataset.title,
            child: c.dataset.child
        }));

        console.log(selectedLetters);

        selectedList.innerHTML = "";
        selectedLetters.forEach(letter => {
            const li = document.createElement("li");
            li.textContent = `${letter.title} / ${letter.child}`;
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
        selectedLetters.forEach(letter => {
            formData.append("delete_letter", letter.id);
        });

        console.log("CSRF Token:", getCsrfToken());

        fetch("/school_letters/delete_letter/", {
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
                window.location.href = "/school_letters/letter_list/";
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
        return document.querySelector('meta[name="csrf-token"]').getAttribute('content');
    }
});