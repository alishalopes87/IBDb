function showResults(results){
   if(Array.isArray(results)){
        for(let i in results){
        console.log(results)
        let book= results[i]
        let ulHtml = $('<ul>')
        
        // listTitle.text(book.title) 
        // $('#book-results').append('Title',listTitle)

        let newLi = $('<li>')
        let bookUrl = $('<a>')
        newLi.append(bookUrl)
        bookUrl.text(book.title)
        bookUrl.attr("href", book.book_url)
        $('#book-results').append(newLi)
        let author_url = $('<a>')
        let authorLi = $('<li>')
        authorLi.append(author_url)
        author_url.text(book.name)
        author_url.attr("href", author_url.author_url)
        $('#book-results').append(authorLi)
        let count = book.count
        let countLi = $('<p>')
        countLi.text(count) 
        $('#count-result').text("Results:")
         $('#count-result').append(countLi)

    }
    }else{
        let book = results 
        let newLi = $('<li>')
        let bookUrl = $('<a>')
        newLi.append(bookUrl)
        bookUrl.text(book.title)
        bookUrl.attr("href", book.book_url)
        $('#book-results').append(newLi) 
        newLi.append(bookUrl)
        bookUrl.text(book.name)
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

// function showAuthorResults(results){ 
//     if(Array.isArray(results)){
//         for(let i in results){
//         console.log(results)
//         let author= results[i]
//         console.log(author)
//         let newLi = $('<li>')
//         let bookUrl = $('<a>')
//         newLi.append(bookUrl)
//         bookUrl.text(author.name)
//         bookUrl.attr("href", author.author_url)
//         $('#book-results').append(newLi)
//         }
//     } else{
//         let author = results
//         console.log(author)
//         let newLi = $('<li>')
//         let bookUrl = $('<a>')
//         newLi.append(bookUrl)
//         bookUrl.text(author.name)
//         bookUrl.attr("href", author.author_url)
//         $('#book-results').append(newLi)
//     }
// };    

// $('#getCount').on('submit', evt => {
//     evt.preventDefault();

//     $.get("/search-books.json", searchData, showCount)
// });

