function showLanguageFilters(){
    // function to show or hide the category filters
    const languageButton = document.getElementById('language-dropdown')
    let showing = true;
    const languageFields = document.getElementById('language-group')
    languageButton.addEventListener('click', (evt)=>{
        console.log("clicked!")
        if (showing){
            languageFields.style.display="none";
            showing = false;
        }
        else{
            languageFields.style.display="block";
            showing=true
            }
        });
    }




fillSearchBar();
showLanguageFilters();