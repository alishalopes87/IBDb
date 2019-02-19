function showResults(results){
    console.log(results)
    console.log(results.title
    $('#title').html(results.title);
    $('#author').html(results.author);
    $("#book_url").attr("href", results.book_url)
}

$('#getInfo').on('submit', evt => {
    evt.preventDefault();
    const searchData = {
        book: $('#book').val()
    };

    $.get("/search-books.json", searchData, showResults)
});

