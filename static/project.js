function showResults(results){
    console.log(results)
    console.log(results.title)
    let ulHtml = $('<ul>')
    for(let i in results){
        let book= results[i]
        console.log(typeof(book))
        let ulHtml = $('<ul>')
        // let listTitle = $('<li>')
        // listTitle.text(book.title) 
        // $('#book-results').append('Title',listTitle)
        
        // listAuthor.text(book.author)
        // $('#book-results').append('Author',listAuthor)
        let bookUrl = $('<a>')
        bookUrl.text(book.title)
        bookUrl.attr("href", book.book_url)
        $('#book-results').append(bookUrl)
        
  }
};  

$('#getInfo').on('submit', evt => {
    evt.preventDefault();
    const searchData = {
        book: $('#book').val()
    };

    $.get("/search-books.json", searchData, showResults)
});

function showAuthorResults(results){
    console.log(results)
    console.log(results.title)
    let ulHtml = $('<ul>')
    for(let i in results){
        let book= results[i]
        console.log(typeof(book))
        let ulHtml = $('<ul>')
        let bookUrl = $('<a>')
        bookUrl.text(book.title)
        bookUrl.attr("href", book.book_url)
        $('#book-results').append(bookUrl)
        
  }
};    

$('#getAuthor').on('submit', evt => {
    evt.preventDefault();
    const searchData = {
        book: $('#author').val()
    };

    $.get("/search-books.json", searchData, showAuthorResults)
});

