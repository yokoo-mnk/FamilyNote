document.addEventListener("DOMContentLoaded", function () {
    function getCsrfToken() {
        const tokenElement = document.querySelector("[name=csrfmiddlewaretoken]");
        return tokenElement ? tokenElement.value : "";
    }


    const openModal = document.getElementById("open-modal");
    const modal = document.getElementById("child-modal");
    const closeModal = document.getElementById("close-modal");
    const childForm = document.querySelector("#child-modal-form");

    if (!openModal || !modal || !closeModal || !childForm) {
        console.error("モーダルの要素が見つかりません！");
        return;
    }

    // モーダルを開く
    openModal.addEventListener("click", function (event) {
        event.preventDefault();  // リンクのデフォルト動作を防ぐ
        console.log("モーダルを開きます");
        modal.style.display = "flex"; // モーダルを表示
    });

    // モーダルを閉じる
    closeModal.addEventListener("click", function () {
        modal.style.display = "none";
    });

    // モーダル外をクリックしたら閉じる
    window.addEventListener("click", function (event) {
        if (event.target === modal) {
            modal.style.display = "none";
        }
    });
    
    // フォームの送信処理
    const form = document.getElementById("child-modal-form"); // フォームのIDを指定
    if (form) {
        form.addEventListener('submit', function (event) {
            event.preventDefault();

            // DjangoのURLパターンに合わせたURLを指定
            fetch("/accounts/add_child/", {  // ✅ 直接パスを指定
                method: "POST",
                headers: {
                    "X-CSRFToken": getCsrfToken(), // ✅ CSRFトークンを取得する関数を作る
                },
                body: new URLSearchParams(new FormData(document.getElementById("child-modal-form"))),
            })
            
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    console.log("子ども情報が登録されました");
                    modal.style.display = "none";
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