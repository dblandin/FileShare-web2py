# coding: utf8
def index():
    redirect(URL('new'))

def new():
    import sha, random, base64, os
    import applications.BlandinDevon_Assignment01.modules.bitly as bitly
    form = SQLFORM(db.file, fields=['name', 'file'])
    if request.vars.file != None:
        filename = request.vars.file.filename
        form.vars.filename = filename
        form.vars.ext = os.path.splitext(filename)[1]
        form.vars.access_token = base64.b64encode(sha.sha(str(random.random())).hexdigest())[:8]
        form.vars.short_url = bitly.shorten(URL('get', args=form.vars.access_token, scheme=True))
    if form.process().accepted:
        response.flash = 'Form accepted'
        redirect(URL('get', args=[form.vars.access_token]))
    elif form.errors:
        response.flash = 'Form has errors'
        
    return dict(form=form)

def get():        
    
    file = db.file(db.file.access_token==request.args(0)) or redirect(URL('new'))
    if (file.ext == '.jpg'):
        image_output = IMG(_src=URL('default', 'download', args=file.file), _style='height:100px;')
    else:
        image_output = ''
    
    return dict(file=file, image_output=image_output)
