$( document ).ready(() =>{

    $(".photos-thumbnail-grid div div").on('click', (event) =>{
        const target = $( event.target );
        window.open('/gallery/view/' + target.closest("div").parent("div").find("#name").html() + '/0', '_parent');
    });

});