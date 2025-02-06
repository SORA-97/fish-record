document.getElementById('tag-filter').addEventListener('change', function() {
    const tagId = this.value;
    fetch(`/filter_records?tag_id=${tagId}`)
        .then(response => response.json())
        .then(data => {
            const recordsContainer = document.querySelector('.records ul');
            recordsContainer.innerHTML = '';
            if (data.records.length === 0) {
                recordsContainer.innerHTML = '<p style="margin: 10px 0;">まだ記録がありません。</p>';
            } else {
                data.records.forEach(record => {
                    const recordElement = document.createElement('li');
                    recordElement.className = 'card';
                    recordElement.innerHTML = `
                        <a href="/record/${record.record_id}">
                            ${record.photo_path !== 'default.jpg' ? `<img src="/static/uploads/${record.photo_path}" class="card-photo"><div class="card-photo-gradient"></div>` : ''}
                            <div class="card-title">${record.fish_name}</div>
                            <p class="small">作成日: ${record.created_at}</p>
                        </a>
                    `;
                    recordsContainer.appendChild(recordElement);
                });
            }
        });
});