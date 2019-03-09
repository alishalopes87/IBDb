const dataFetcher = (request, response) => {
  $.get('/search-subjects.json?subject=' + request.term, (results) => {
      console.log(request.term)
      console.log("results", results)
      response([results])
  });
}


$( document ).ready(function() {
    $( "#myInput" ).autocomplete({
        appendTo: "#someElem"
    });

    $('#myInput').autocomplete({ source: dataFetcher })
    console.log("hello")
});




