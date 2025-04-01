document.addEventListener("DOMContentLoaded", function () {
    const openModal = document.getElementById("open-modal");
    const modal = document.getElementById("child-modal");
    const closeModal = document.getElementById("close-modal");
   
    if (!openModal || !modal || !closeModal) {
        console.error("モーダルの要素が見つかりません！");
        return;
    }

    // モーダルを開く
    openModal.addEventListener("click", function (event) {
        event.preventDefault();  // リンクのデフォルト動作を防ぐ
        console.log("モーダルを開きます");
        modal.style.display = "block"; // モーダルを表示
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
    const form = document.getElementById("child-form"); // フォームのIDを指定
        form.addEventListener("submit", function (e) {
            e.preventDefault(); // デフォルトのフォーム送信をキャンセル

            const formData = new FormData(form);
            const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

            // DjangoのURLパターンに合わせたURLを指定
            fetch("{% url 'accounts:add_child' %}", {  // ここでURLを指定
                method: 'POST',
                body: formData,
                headers: {
                    'X-CSRFToken': csrfToken  // CSRFトークンを送信
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    console.log("子ども情報が登録されました");
                    modal.style.display = "none";
                } else {
                    console.log("エラー:", data.errors);
                }
            })
            .catch(error => {
                console.error("エラー:", error);
            });
        });
    });