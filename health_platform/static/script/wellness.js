function loadArticle(topic) {
    fetch(`/article/${topic}`)
    .then(response => response.json())
    .then(data => {
        document.getElementById("articleTitle").innerText = data.title;
        document.getElementById("articleContent").innerText = data.content;
        document.getElementById("articleModal").style.display = "block";
    })
    .catch(() => {
        alert("Failed to load article.");
    });
}

function closeModal() {
    document.getElementById("articleModal").style.display = "none";
} 