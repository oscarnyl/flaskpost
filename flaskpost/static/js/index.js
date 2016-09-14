document.querySelector("#load_more").addEventListener("click", function() {
    var count = document.getElementsByClassName("blogpost").length;
    console.log("DEBUG: count: " + count);
    var request = new XMLHttpRequest();
    request.open('POST', '/api/more_posts');
    request.setRequestHeader("Content-Type", "application/json");

    request.onload = function() {
        if (this.status >= 200 & this.status < 400) {
            var data = JSON.parse(this.response);
            var additional = document.querySelector("#additional_posts");
            data.map( function (post) {
                var element = document.createElement("div");
                element.setAttribute("class", "blogpost");
                var title = document.createElement("h3");
                title.appendChild(document.createTextNode(post[1]));
                var post_body = document.createElement("p");
                post_body.appendChild(document.createTextNode(post[2]));
                var footer = document.createElement("h6");
                footer.appendChild(document.createTextNode("Post #" + post[0] + ". Posted " + post[3]));
                element.appendChild(title);
                element.appendChild(post_body);
                element.appendChild(footer);
                additional.appendChild(element);
            });
        }
    };

    request.send(JSON.stringify({current_limit: count}));

});
