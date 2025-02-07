function validateForm() {
    const photo = document.getElementById('photo').files.length;
    const fishName = document.getElementById('fish_name').value.trim();

    if (photo === 0 && fishName === "") {
        alert("画像か名称のいずれかを入力してください。");
        return false;
    }
    return true;
}