import os, glob
import markdown
import datetime 

path = 'blog-html'
files = glob.glob(os.path.join(path, '*.html'))
for filename in files:
    os.remove(filename)

path = 'blog-md'
with open("listify.js", 'w') as g:
    g.writelines(
"""
var lst = [];
var update = [];
var genre = [];

function listify() {
"""        
    )
    files = glob.glob(os.path.join(path, '*.md'))
    files.sort(key=os.path.getmtime, reverse=True)
    
    for filename in files:
        with open(filename,  encoding="utf-8", mode = 'r') as f: # open in readonly mode
            # do your stuff
            print(str(filename))
            text = f.read()
            html = markdown.markdown(text)
            html = "".join([["\)","\("][i&1 if i else 1]+l for i, l in enumerate(html.split('$'))])[2:]
            html = html.replace("<code>","<pre><code>").replace("</code>","</code></pre>")
            # print(str(html))
        genre = "Other:"
        filepath = str(filename[8:-3])
        for i in range(len(str(filename[8:-3]))) :
            if (filename[8+i] == '_') :
                genre = filename[8:8+i] + ":"
                filepath = filename[(9+i):-3]
                break 

        with open(f"blog-html/{filepath}.html", 'w') as f:
            f.writelines("""
<!DOCTYPE html>
<head>
    <meta charset="UTF-8">
    <link rel="stylesheet" href="style.css">
    <script src="script.js"></script>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.11.1/dist/katex.min.css" integrity="sha384-zB1R0rpPzHqg7Kpt0Aljp8JPLqbXI3bhnPWROx27a9N0Ll6ZP/+DiW/UqRcLbRjq" crossorigin="anonymous">
    <script defer src="https://cdn.jsdelivr.net/npm/katex@0.11.1/dist/katex.min.js" integrity="sha384-y23I5Q6l+B6vatafAwxRu/0oK/79VlbSz7Q9aiSZUvyWYIYsd+qj+o24G5ZU2zJz" crossorigin="anonymous"></script>
    <script defer src="https://cdn.jsdelivr.net/npm/katex@0.11.1/dist/contrib/auto-render.min.js" integrity="sha384-kWPLUVMOks5AQFrykwIup5lo0m3iMkkHrD0uJ4H5cjeGihAutqP0yW0J6dpFiVkI" crossorigin="anonymous" onload="renderMathInElement(document.body);"></script>
    <link rel="stylesheet" href="highlight/styles/github-dark-dimmed.min.css">
    <script src="highlight/highlight.min.js"></script>
</head>                           
""")
            f.write(html)
            f.writelines("""
<script>
    init();
    hljs.highlightAll();
</script>
""")
        if (str(filename)[8:-3] == "default"):
            continue
        #append to listify() command
        g.writelines(
f"""
    lst.push("{filepath}");
    update.push("{datetime.datetime.fromtimestamp(os.path.getctime(filename)).strftime('%Y-%m-%d')}")
    genre.push("{genre}")
"""
        )
    g.writelines("""}""")