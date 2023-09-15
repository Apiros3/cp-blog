
function render_blog(path) {
    // console.log(path)
    document.getElementById("content").innerHTML = `
        <iframe src="blog-html/${path}.html" title="${path}" frameBorder="0"></iframe>
    `
}

function sortFunction(a, b) {
    if (a[0] === b[0]) {
        return 0;
    }
    else if (a[0] == "Other:") return 1;
    else if (b[0] == "Other:") return -1;
    else {
        return (a[0] < b[0]) ? -1 : 1;
    }
}

function initial_blog_load() {

    var a = new Array(genre.length);
    for(let i = 0; i < genre.length; i++) {
        a[i] = [genre[i], lst[i], update[i]];
    }

    a.sort(sortFunction);

    var return_string = "<table><tr class='blog-sidebar'><td class='sidebar-title'>Title:</td><td class='sidebar-date'>Last Update:</td></tr>";

    last_genre = "";
    for(let i = 0; i < genre.length; i++) {
        if (last_genre != a[i][0]) {
            return_string += `
                <tr class="genre" style="border-bottom:1px solid #89929b">
                    <td colspan="2">
                        ${a[i][0]}
                    </td>
                </tr>
            `
            last_genre = a[i][0];
        }
    
        return_string += `
            <tr id="blog-${a[i][1]}">
                <td class="article-title" onclick="render_blog('${a[i][1]}')">
                    ${a[i][1]}
                </td> 
                <td class="article-date">
                    ${a[i][2]}
                </td>
            </tr>
        `
    }
    return_string += "</table>"
    document.getElementById("list").innerHTML = return_string;

    const searchParams = new URLSearchParams(window.location.search);
    if (searchParams.has('blog')) {
        render_blog(searchParams.get('blog'));
    }
    else {
        render_blog('default');
    }

}