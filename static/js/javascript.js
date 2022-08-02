"use strict"

const checkImage = (evt) => {
    let title = $("#title").val();
    let author = $("#author").val();
    let series = $("#series").val();
    let isValid = true;

    let allowedExtensions = /(\.jpg|\.jpeg|\.png|\.gif|\.jfif)$/i;
    const imageSize = Math.round($('#item_picture')[0].files[0].size /1024);

    if (imageSize > 1000 || !allowedExtensions.exec($("#item_picture").val())) {
        isValid = false;
        $("#item_picture").next().next().text("* Image larger than 1MB, or of wrong type");
    }
    else {
        $("#item_picture").next().next().text("");
    }

    if ( title === "" ) {
        isValid = false;
        $("#title").next().next().text("* Title field is required");
    }
    else {
        $("#title").next().next().text("");
    }

    if ( author === "" ) {
        isValid = false;
        $("#author").next().next().text("* Author field is required");
    }
    else {
        $("#author").next().next().text("");
    }
    if ( series === "" ) {
        isValid = false;
        $("#series").next().next().text("* Series field is required");
    }
    else {
        $("#series").next().next().text("");
    }

    if ( isValid === false ) {
			evt.preventDefault();
		}
}

$(document).ready( () => {
    $("#addItemSubmit").click( (evt) => {
        checkImage(evt);
    });
});