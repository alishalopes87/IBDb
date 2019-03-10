function showResults(response){
    //FIXME: Remove the old results if necessary before
    //adding new ones
   const results = response.results
   const count = response.count

    //TODO: Display this count somewhere on the page
    //(ps don't forget to to remove the old count)
   console.log(count)

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

        //FIXME: This can probably be deleted now :)
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
}

