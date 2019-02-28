function showResults(results){
   if(Array.isArray(results)){
        for(let i in results){
        let book= results[i]
        console.log(typeof(book))
        let ulHtml = $('<ul>')
        // let listTitle = $('<li>')
        // listTitle.text(book.title) 
        // $('#book-results').append('Title',listTitle)
        
        // listAuthor.text(book.author)
        // $('#book-results').append('Author',listAuthor)
        let newLi = $('<li>')
        let bookUrl = $('<a>')
        newLi.append(bookUrl)
        bookUrl.text(book.title)
        bookUrl.attr("href", book.book_url)
        $('#book-results').append(newLi)
    }
    }else{
        let book = results 
        let newLi = $('<li>')
        let bookUrl = $('<a>')
        newLi.append(bookUrl)
        bookUrl.text(book.title)
        bookUrl.attr("href", book.book_url)
        $('#book-results').append(newLi) 
        
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
    if(Array.isArray(results)){
        for(let i in results){
        console.log(results)
        let author= results[i]
        console.log(author)
        let newLi = $('<li>')
        let bookUrl = $('<a>')
        newLi.append(bookUrl)
        bookUrl.text(author.name)
        bookUrl.attr("href", author.author_url)
        $('#book-results').append(newLi)
        }
    } else{
        let author = results
        console.log(author)
        let newLi = $('<li>')
        let bookUrl = $('<a>')
        newLi.append(bookUrl)
        bookUrl.text(author.name)
        bookUrl.attr("href", author.author_url)
        $('#book-results').append(newLi)
    }
};    

$('#getAuthor').on('submit', evt => {
    evt.preventDefault();
    const searchData = {
        author: $('#author').val()
    };

    $.get("/search-books.json", searchData, showAuthorResults)
});

