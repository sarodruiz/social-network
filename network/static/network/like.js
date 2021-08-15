document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.like-btn').forEach(btn => {
        btn.onclick = function (event) {
            on_like(this.dataset.id);
        }
    });
});

function on_like(post_id) {
    fetch('/like', {
        method: 'POST',
        body: JSON.stringify({
            id: post_id
        })
    })
    .then(response => response.json())
    .then(data => {
            document.querySelector(`#likes${post_id}`).innerHTML = `Likes: ${data.likes}`;
            document.querySelector(`#like-btn${post_id}`).innerHTML = `${data.text}`;
    });
}