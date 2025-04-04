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
    

    // 家族モーダルの要素が正しく取得できているか確認
    if (!openFamilyModal) console.error("openFamilyModalが見つかりません！");
    if (!familyModal) console.error("familyModalが見つかりません！");
    if (!closeFamilyModal) console.error("closeFamilyModalが見つかりません！");
    if (!familyForm) console.error("createFamilyFormが見つかりません！");

    // 子どもモーダルの要素が正しく取得できているか確認
    if (!openChildModal) console.error("openChildModalが見つかりません！");
    if (!childModal) console.error("childModalが見つかりません！");
    if (!closeChildModal) console.error("closeChildModalが見つかりません！");
    if (!childForm) console.error("childFormが見つかりません！");

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
                console.log(data);

                if (data.success) {
                    console.log("家族情報が登録されました");
                    
                    const familyModal = document.getElementById('family-modal');
                    if (familyModal) {
                        familyModal.style.display = "none"; // モーダルを非表示にする
                    }
                     // 家族状態を更新
                    document.querySelector("#family-status").innerHTML = "現在、家族に所属しています。";
                    
                    const openFamilyModalLink = document.getElementById("open-family-modal");
                    if (openFamilyModalLink) {
                        openFamilyModalLink.style.display = "none"; // リンクを非表示
                    }

                    const leaveFamilyButton = document.querySelector("#leave-family-button");
                    if (leaveFamilyButton) {
                        leaveFamilyButton.style.display = "block"; // ボタンを表示
                    }
                    

                    // // もし家族が作成されていれば、もう一度家族リンクの表示状態を確認
                    // const familyDiv = document.querySelector('.family-status');  // 家族の状態を表示している要素を指定（仮にfamily-statusとしています）
                    // if (familyDiv) {
                    //     familyDiv.style.display = 'none'; // 例えば、ユーザーが家族に所属している場合はその情報を非表示にするなど
                    // }

                    const familyName = data.family.family_name;  // サーバーから返される家族の名前
                    document.querySelector(".family-box h3").innerHTML = familyName + " 家族情報";
                    
                    const familyInviteLink = document.querySelector("#family-invite-link");
                    if (familyInviteLink) {
                        familyInviteLink.style.display = "inline";
                    }
                    // const familyStatusElement = document.querySelector("#family-status");
                    // if (familyStatusElement) {
                    //     familyStatusElement.innerHTML = "現在、家族に所属しています。";
                    // } else {
                    //     console.error("#family-status 要素が見つかりません。");
                    // }

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
    
    // 家族を抜けるボタンが押されたときに「家族を作成する」リンクを再表示する処理
    const leaveFamilyButton = document.querySelector('.getout form');
    if (leaveFamilyButton) {
        leaveFamilyButton.addEventListener('submit', function (event) {
            event.preventDefault();

            // 「家族を作成する」リンクを再表示
            const openFamilyModalLink = document.getElementById("open-family-modal");
            if (openFamilyModalLink) {
                openFamilyModalLink.style.display = "block"; // リンクを再表示
            }

            // 「家族を抜ける」ボタンを非表示
            leaveFamilyButton.style.display = "none"; // ボタンを非表示

            // 家族を抜ける処理を行う（フォーム送信など）
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
                    location.reload(); // 必要ならページをリロード
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
    }
});