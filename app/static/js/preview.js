function previewImage(event) {
    var reader = new FileReader();
    var file = event.target.files[0];

    if (!file) {
        clearPreviewImage();
        return;
    }

    reader.onload = function(){
        var output = document.getElementById('photo-preview');
        output.src = reader.result;
        output.style.display = 'block';
    };
    reader.readAsDataURL(file);

    input.value = '';
}

function clearPreviewImage() {
    var output = document.getElementById('photo-preview');
    output.src = '#';
    document.getElementById('photo').value = '';
    output.style.display = 'none';
}

function previewTags(event) {
    const memo = document.getElementById('memo').value;
    const tagContainer = document.getElementById('tag-container');
    const tagPattern = /(?<!\S)#([^\s#]+)(?=\s|$)/g;
    let match;
    const tags = new Set();
    tagContainer.innerHTML = '';

    while ((match = tagPattern.exec(memo)) !== null) {
        tags.add(match[1]);
    }

    tags.forEach(tagText => {
        const tag = document.createElement('div');
        tag.className = 'tag';
        tag.textContent = tagText;
        tagContainer.appendChild(tag);
    });
}

document.getElementById('memo').addEventListener('input', previewTags);
window.addEventListener('load', previewTags);