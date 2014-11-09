function limitText(limitField, limitCount, limitNum) {
    if (limitField.value.length > limitNum) {
		limitField.value = limitField.value.substring(0, limitNum);
    } else {
		limitCount.value = limitNum - limitField.value.length;
    }
}


$("a[data-permalink]").click(function(e) {  // when a like/unlike button is clicked for a post
	permalink = $(this).attr("data-permalink")  // get the permalink for the post liked/unliked
		
    if ($(this).html() == "Like") {  // if "like" button was clicked
		$(this).html('Unlike');  // change button from "like" to "unlike"
		$.post('/like_post', {permalink: permalink}, function(data) {  	// send a post request to /like_post with permalink
			if (data == 'success') {  // if like was successfully saved to the database

			} else {   // if like was not successfully saved to the database
				alert('Uh oh. Try again later, maybe?');
			}
		});    
    }
    
    else {  // if "unlike" button was clicked
        $(this).html('Like');  // change button from "unlike" to "like"
        $.post('/unlike_post', {permalink: permalink}, function(data) {  // send a post request to /unlike_post with permalink
        	if (data == 'success') {  // if unlike was successfully saved to the database

        	} else {  // if unlike was not successfully saved to the database
        		alert("Uh oh. Try again later, maybe?");
        	}
        });
    }
    
    return false;
});