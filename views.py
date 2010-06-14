# -*- encoding: UTF-8 -*-
'''
Chat application views, some are tests... some are not
@author: Federico Cáceres <fede.caceres@gmail.com>
'''
from datetime import datetime

from django.http import HttpResponse, Http404
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.contrib.auth.models import User 

from models import Room, Message

@login_required
def send(request):
    '''
    Expects the following POST parameters:
    chat_room_id
    message
    '''
    p = request.POST
    r = Room.objects.get(id=int(p['chat_room_id']))
    r.say(request.user, p['message'])
    return HttpResponse('')

@login_required
def sync(request):
    '''Return last message id

    EXPECTS the following POST parameters:
    id
    '''
    if request.method != 'POST':
        raise Http404
    post = request.POST

    if not post.get('id', None):
        raise Http404

    r = Room.objects.get(id=post['id'])
    
    lmid = r.last_message_id()    
    
    return HttpResponse(jsonify({'last_message_id':lmid}))

@login_required
def receive(request):
    '''
    Returned serialized data
    
    EXPECTS the following POST parameters:
    id
    offset
    
    This could be useful:
    @see: http://www.djangosnippets.org/snippets/622/
    '''
    if request.method != 'POST':
        raise Http404
    post = request.POST

    if not post.get('id', None) or not post.get('offset', None):
        raise Http404
    
    try:
        room_id = int(post['id'])
    except:
        raise Http404

    try:
        offset = int(post['offset'])
    except:
        offset = 0
    
    r = Room.objects.get(id=room_id)

    m = r.messages(offset)

    
    return HttpResponse(jsonify(m, ['id','author','message','type']))


@login_required
def join(request):
    '''
    Expects the following POST parameters:
    chat_room_id
    message
    '''
    p = request.POST
    r = Room.objects.get(id=int(p['chat_room_id']))
    r.join(request.user)
    return HttpResponse('')


@login_required
def leave(request):
    '''
    Expects the following POST parameters:
    chat_room_id
    message
    '''
    p = request.POST
    r = Room.objects.get(id=int(p['chat_room_id']))
    r.leave(request.user)
    return HttpResponse('')


@login_required
def test(request):
    '''Test the chat application'''
    
    u = User.objects.get(id=1) # always attach to first user id
    r = Room.objects.get_or_create(u)

    return render_to_response('chat/chat.html', {'js': ['/media/js/mg/chat.js'], 'chat_id':r.pk}, context_instance=RequestContext(request))


def jsonify(object, fields=None, to_dict=False):
    '''Simple convert model to json'''
    try:
        import json
    except:
        import django.utils.simplejson as json
 
    out = []
    if type(object) not in [dict,list,tuple] :
        for i in object:
            tmp = {}
            if fields:
                for field in fields:
                    tmp[field] = unicode(i.__getattribute__(field))
            else:
                for attr, value in i.__dict__.iteritems():
                    tmp[attr] = value
            out.append(tmp)
    else:
        out = object
    if to_dict:
        return out
    else:
        return json.dumps(out)
