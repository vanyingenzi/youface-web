$( document ).ready( function(){

    /**
     * Contains all the JQuery code.
     *
     */
    const openSideMenuButton = $("#menuOpenButton");
    const closeSideMenuButton = $("#menuCloseButton");
    const sideNavMenu = $(".sideMenuContainer");

    /* Manually hides the menu on mobile screen */
    if ( parseInt($(window).width()) <= 600){
        sideNavMenu.hide();
        openSideMenuButton.show();
        closeSideMenuButton.hide();
    }

    openSideMenuButton.click(() => {
        openSideMenuButton.hide();
        sideNavMenu.show();
        closeSideMenuButton.show();
    });

    closeSideMenuButton.click(() => {
        closeSideMenuButton.hide();
        sideNavMenu.hide();
        openSideMenuButton.show();
    });
});
