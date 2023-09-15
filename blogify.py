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
<link rel="stylesheet" href="style.css">
<script src="script.js"></script>
                                                  
""")
            f.write(html)
            f.writelines("""
<script>
    init()
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