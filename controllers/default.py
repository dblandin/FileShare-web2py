# -*- coding: utf-8 -*-

def index():
    redirect(URL('file', 'new'))

def user():
    return dict(form=auth())

def download():
    return response.download(request,db)

def call():
    return service()


@auth.requires_signature()
def data():
    return dict(form=crud())
