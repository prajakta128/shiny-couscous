function filterSchemes() {
    let input = document.getElementById("searchBox").value.toLowerCase();
    let cards = document.getElementById("schemeCards").getElementsByClassName("card");
    for (let i = 0; i < cards.length; i++) {
        let title = cards[i].getElementsByTagName("h3")[0].innerText.toLowerCase();
        if (title.includes(input)) {
            cards[i].style.display = "block";
        } else {
            cards[i].style.display = "none";
        }
    }
}