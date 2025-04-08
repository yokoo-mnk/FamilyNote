document.addEventListener("DOMContentLoaded", function () {
    function getCsrfToken() {
        const tokenElement = document.querySelector("[name=csrfmiddlewaretoken]");
        console.log(tokenElement ? tokenElement.value : "CSRFトークンが見つかりません");
        return tokenElement ? tokenElement.value : "";
    }

    const openFamilyModal = document.getElementById('open-family-modal');
    const familyModal = document.getElementById('family-modal');
    const closeFamilyModal = document.getElementById('close-family-modal');
    
    const openChildModal = document.getElementById('open-child-modal');
    const childModal = document.getElementById('child-modal');
    const closeChildModal = document.getElementById('close-child-modal');
    const editChildModal = document.getElementById('edit-child-modal');
    const closeEditChildModal = document.getElementById('close-edit-child-modal');
    const editChildModalForm = document.getElementById("edit-child-modal-form");
    

    // モーダルを開く
    if (openFamilyModal && familyModal) {
        openFamilyModal.addEventListener("click", function (event) {
            event.preventDefault();
            console.log("家族モーダルを開きます");
            familyModal.style.display = "flex";
        });
    }
    
    if (openChildModal) {
        openChildModal.addEventListener("click", function (event) {
            event.preventDefault();
            if (childModal) {
                childModal.style.display = "flex";
            }
        });
    }
      
    if (closeChildModal) {
        closeChildModal.addEventListener("click", function () {
            if (childModal) {
                childModal.style.display = "none";
            }
        });
    }

    // モーダルを閉じる
    closeFamilyModal.addEventListener("click", function () {
        familyModal.style.display = "none";
    });
    closeChildModal.addEventListener("click", function () {
        childModal.style.display = "none";
    });

    // モーダル外をクリックしたら閉じる
    window.addEventListener("click", function (event) {
        if (event.target === familyModal) {
            familyModal.style.display = "none";
        }
        if (event.target === childModal) {
            childModal.style.display = "none";
        }
    });
    
    // 家族作成処理
    const createFamilyForm = document.getElementById("create-family-form");
    if (createFamilyForm) {
        createFamilyForm.addEventListener('submit', function (event) {
            event.preventDefault();

            const formData = new FormData(createFamilyForm);
            fetch("/families/create_family/", {
                method: "POST",
                headers: {
                    "X-CSRFToken": getCsrfToken(),
                },
                body: formData,
            })
            
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    console.log("家族情報が登録されました");
                    location.reload();

                    const leaveFamilyButton = document.getElementById("leave-family-button");
                    if (leaveFamilyButton) {
                        leaveFamilyButton.disabled = false;
                        leaveFamilyButton.classList.remove("disabled");
                    }
                   
                    const familyInviteLink = document.getElementById("family-invite-link");
                    if (familyInviteLink) {
                        familyInviteLink.classList.remove("disabled-link");
                        familyInviteLink.onclick = null;
                    }
                    location.reload();
                    
                } else {
                    console.log("エラー:", data.errors);
                }
            })
            .catch(error => {
                console.error("エラー:", error);
                alert("通信エラーが発生しました。");
            });
        });
    }

    // 家族を抜ける処理
    const leaveFamilyButton = document.querySelector('.getout form');
    if (leaveFamilyButton) {
        leaveFamilyButton.addEventListener('submit', function (event) {
            event.preventDefault();

            const formData = new FormData(leaveFamilyButton);
            fetch(leaveFamilyButton.action, {
                method: "POST",
                headers: {
                    "X-CSRFToken": getCsrfToken(),
                },
                body: formData,
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    console.log("家族から抜けました");
                }
            })
            .catch(error => {
                console.error("エラー:", error);
                alert("通信エラーが発生しました。");
            });
        });
    }
    // 子供情報登録する処理
    const childModalForm = document.getElementById("child-modal-form");
    if (childModalForm) {
        childModalForm.addEventListener('submit', function (event) {
            event.preventDefault();

            const formData = new FormData(childModalForm);
            fetch("/accounts/add_child/", {
                method: "POST",
                headers: {
                    "X-CSRFToken": getCsrfToken(),
                },
                body: formData,
            })
            
            .then(response => {
                if (!response.ok) {
                    throw new Error('ネットワークエラー');
                }
                return response.json();
            })
            .then(data => {
                if (data.success) {
                    console.log("子ども情報が登録されました");
                    childModal.style.display = "none";
                    location.reload();
                } else {
                    console.log("エラー:", data.errors);
                }
            })
            .catch(error => {
                console.error("エラー:", error);
                alert("通信エラーが発生しました。");
            });
        });
    }
    
    // 子供情報編集処理
    const editChildLinks = document.querySelectorAll('.edit-child');

    editChildLinks.forEach(link => {
        link.addEventListener('click', function (event) {
            event.preventDefault();

            const childId = this.getAttribute('data-id');
            
            fetch(`/accounts/get_child_data/${childId}/`)
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        editChildModal.style.display = "flex";

                        document.getElementById('edit_child_id').value = data.child.id;
                        document.getElementById('edit_child_name').value = data.child.child_name;
                        document.getElementById('edit_birth_date').value = data.child.birth_date;
                    } else {
                        alert("データの取得に失敗しました");
                    }
                })
                .catch(error => {
                    console.error("エラー:", error);
                    alert("通信エラーが発生しました。");
                });
            });
        });
        
        closeEditChildModal.addEventListener("click", function () {
            editChildModal.style.display = "none";
        });

        window.addEventListener("click", function (event) {
            if (event.target === editChildModal) {
                editChildModal.style.display = "none";
            }
        });

        if (editChildModalForm) {
            editChildModalForm.addEventListener('submit', function (event) {
                event.preventDefault();
        
                const formData = new FormData(editChildModalForm);

                fetch(`/accounts/edit_child/${childId}/`, {
                    method: "POST",
                    headers: {
                        "X-CSRFToken": getCsrfToken(),
                    },
                    body: formData,
                })

                .then(response => {
                    if (!response.ok) {
                        throw new Error('ネットワークエラー');
                    }
                    return response.json();
                })
                .then(data => {
                    if (data.success) {
                        console.log("子ども情報が更新されました");
                        editChildModal.style.display = "none";
                        location.reload();
                    } else {
                        console.log("エラー:", data.errors);
                    }
                })
                .catch(error => {
                    console.error("エラー:", error);
                    alert("通信エラーが発生しました。");
                });
            });
        }
    let selectedChildId = null;

    document.querySelectorAll('.delete-child').forEach(function (button) {
        button.addEventListener('click', function (event) {
            event.preventDefault();
            selectedChildId = this.getAttribute('data-id');
            document.getElementById('delete-child-modal').style.display = 'flex';
        });
    });
    
    document.getElementById('confirm-delete-button').addEventListener('click', function () {
        if (selectedChildId) {
            fetch(`/accounts/delete_child/${selectedChildId}/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCsrfToken(),
                }
            })

            .then(response => response.json())
            .then(data => {
                if (data.status === 'deleted') {
                    alert("削除しました！");
                    location.reload();  // ページを更新して削除反映
                } else {
                    alert("削除に失敗しました。");
                }
            })
            .catch(error => {
                console.error("エラー:", error);
                alert("通信エラーが発生しました。");
            });
        }
        document.getElementById('delete-child-modal').style.display = 'none';
    });
    document.getElementById('cancel-delete-button').addEventListener('click', function () {
        document.getElementById('delete-child-modal').style.display = 'none';
    });
    
    document.getElementById('close-delete-modal').addEventListener('click', function () {
        document.getElementById('delete-child-modal').style.display = 'none';
    });   
});