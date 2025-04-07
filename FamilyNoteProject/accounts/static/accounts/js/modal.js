document.addEventListener("DOMContentLoaded", function () {
    function getCsrfToken() {
        const tokenElement = document.querySelector("[name=csrfmiddlewaretoken]");
        return tokenElement ? tokenElement.value : "";
    }

    const openFamilyModal = document.getElementById('open-family-modal');
    const familyModal = document.getElementById('family-modal');
    const closeFamilyModal = document.getElementById('close-family-modal');
    const familyForm = document.querySelector("#create-family-form");
    
    const openChildModal = document.getElementById('open-child-modal');
    const childModal = document.getElementById('child-modal');
    const closeChildModal = document.getElementById('close-child-modal');
    const childForm = document.querySelector("#child-modal-form");
    

    // // 家族モーダルの要素が正しく取得できているか確認
    // if (!openFamilyModal) console.error("openFamilyModalが見つかりません！");
    // if (!familyModal) console.error("familyModalが見つかりません！");
    // if (!closeFamilyModal) console.error("closeFamilyModalが見つかりません！");
    // if (!familyForm) console.error("createFamilyFormが見つかりません！");

    // // 子どもモーダルの要素が正しく取得できているか確認
    // if (!openChildModal) console.error("openChildModalが見つかりません！");
    // if (!childModal) console.error("childModalが見つかりません！");
    // if (!closeChildModal) console.error("closeChildModalが見つかりません！");
    // if (!childForm) console.error("childFormが見つかりません！");

    // モーダルを開く
    openFamilyModal.addEventListener("click", function (event) {
        event.preventDefault();  // リンクのデフォルト動作を防ぐ
        console.log("家族モーダルを開きます");
        familyModal.style.display = "flex"; // モーダルを表示
    });
    openChildModal.addEventListener("click", function (event) {
        event.preventDefault();  // リンクのデフォルト動作を防ぐ
        console.log("こどもモーダルを開きます");
        childModal.style.display = "flex"; // モーダルを表示
    });

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
    
    // フォームの送信処理
    const createFamilyForm = document.getElementById("create-family-form"); // フォームのIDを指定
    if (createFamilyForm) {
        createFamilyForm.addEventListener('submit', function (event) {
            event.preventDefault();

            const formData = new FormData(createFamilyForm);
            // DjangoのURLパターンに合わせたURLを指定
            fetch("/families/create_family/", {  // ✅ 直接パスを指定
                method: "POST",
                headers: {
                    "X-CSRFToken": getCsrfToken(), // ✅ CSRFトークンを取得する関数を作る
                },
                body: formData,
            })
            
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    console.log("家族情報が登録されました");
                    location.reload();

                    // ✅ 表示を切り替える
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

    // 家族を抜ける処理を行う（フォーム送信など）
    const leaveFamilyButton = document.querySelector('.getout form');
    if (leaveFamilyButton) {
        leaveFamilyButton.addEventListener('submit', function (event) {
            event.preventDefault(); // フォーム送信のデフォルト動作を防ぐ

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
    
    const childModalForm = document.getElementById("child-modal-form"); // フォームのIDを指定
    if (childModalForm) {
        childModalForm.addEventListener('submit', function (event) {
            event.preventDefault();

            const formData = new FormData(childModalForm);
            // DjangoのURLパターンに合わせたURLを指定
            fetch("/accounts/add_child/", {  // ✅ 直接パスを指定
                method: "POST",
                headers: {
                    "X-CSRFToken": getCsrfToken(), // ✅ CSRFトークンを取得する関数を作る
                },
                body: formData,
            })
            
            .then(response => response.json())
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
    }})