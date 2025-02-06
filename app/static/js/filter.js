document.getElementById('tag-filter').addEventListener('change', function() {
    const tagId = this.value;
    fetch(`/filter_records?tag_id=${tagId}`)
        .then(response => response.json())
        .then(data => {
            const recordsContainer = document.querySelector('.records ul');
            recordsContainer.innerHTML = '';
            const recordCountElement = document.querySelector('.record-count');
            const totalRecords = data.total_records;
            if (data.records.length === 0) {
                recordsContainer.innerHTML = '<p style="margin: 10px 0;">まだ記録がありません。</p>';
                recordCountElement.textContent = '';
            } else {
                recordCountElement.textContent = `${totalRecords} 件中 ${data.records.length} 件を表示`;
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