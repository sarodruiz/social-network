document.addEventListener('DOMContentLoaded', () => {
    document.querySelector('#new-post-form').addEventListener('submit', new_post)
});

function new_post(event) {
    const content = document.querySelector('#new-post-content').value;
    fetch('', {
        method: 'POST',
        body: JSON.stringify({
            content: content
        })
    })
    .then(response => response.json)
    .then(result => window.location.reload())
    .catch(error => console.log('Error', error));
}