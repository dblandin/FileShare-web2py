# coding: utf8
import sha, random, base64, os
import applications.BlandinDevon_Assignment01.modules.bitly as bitly
code_exts = {'.py': 'python', '.c': 'c', '.cpp': 'cpp', '.web2py': 'web2py', '.html': 'html'}
image_exts = ['.jpg', '.jpeg', '.gif', '.png']

@auth.requires_login()
def index():
        # hide id and access_token from grid
        db.file.id.readable = False
        db.file.access_token.readable = False
        db.file.file.readable = False

        # define the query object. Here we are pulling all files belonging to the currently signed in user
        query = (db.file.posted_by==auth.user)
        
        # define the fields to show on grid
        fields = (db.file.id, db.file.file, db.file.name, db.file.filename, db.file.short_url, db.file.posted_on, db.file.access_token)

        # define headers as tuples/dictionaries
        headers = {'file.id':   'ID',
           'file.name': 'Name',
           'file.filename': 'Filename',
           'file.short_url': 'Short URL',
           'file.posted_on': 'Created At' }
           
        # define additional links
        links = [lambda row: A(SPAN('', _class='icon magnifier icon-zoom-in') + SPAN('View', _class='buttontext button'), _class='w2p_trap button btn', _href=URL("file","get",args=[row.access_token])), lambda row: A(SPAN('', _class='icon-download-alt') + SPAN('Download', _class='buttontext button'), _class='w2p_trap button btn', _href=URL("default","download",args=[row.file]))]

        # define sort order
        default_sort_order=[db.file.posted_on]
        files = SQLFORM.grid(query=query, fields=fields, headers=headers, links=links, orderby=default_sort_order,
                create=False, editable=False, searchable=False, details=False, maxtextlength=64, paginate=25)
        
        return dict(files=files)

def new():
    # define custom form
    form = SQLFORM(db.file, fields=['name', 'file'])
    
    # setup file object
    if request.vars.file != None:
        filename = request.vars.file.filename
        form.vars.filename = filename
        form.vars.ext = os.path.splitext(filename)[1]
        form.vars.access_token = base64.b64encode(sha.sha(str(random.random())).hexdigest())[:8]
        form.vars.short_url = bitly.shorten(URL('get', args=form.vars.access_token, scheme=True))
    if form.process().accepted:
        redirect(URL('get', args=[form.vars.access_token]))
    elif form.errors:
        response.flash = 'Form has errors'
        
    return dict(form=form)

def get():
    # get file by access_token arg
    file = db.file(db.file.access_token==request.args(0)) or redirect(URL('new'))
    
    # if image, display image tag
    if (file.ext in image_exts):
        output = IMG(_src=URL('default', 'download', args=file.file), _style='height:100px;')
    # if code, display content with syntax highlighting
    elif (file.ext in code_exts):
        output = CODE(open(os.path.join(request.folder,'uploads', file.file),'rb').read(), _language=code_exts[file.ext])
    # if plain text, display content
    elif (file.ext == '.txt'):
        output = open(os.path.join(request.folder,'uploads', file.file),'rb').read()
    else:
        output = ''
        
    return dict(file=file, output=output)

def comments():
    
    # define comment form and set coment.file to current file
    if auth.is_logged_in():
        comment_form=SQLFORM(db.comment, fields=['body'])
        comment_form.vars.file = request.args(0)
        if comment_form.process().accepted:
            response.flash = 'Comment saved'
        elif comment_form.errors:
            response.flash = 'Comment has errors'
    else:
        comment_form = P('Login to comment')
        
    # get comments
    comments = db(db.comment.file==request.args[0]).select()
        
    return dict(comment_form=comment_form, comments=comments)
