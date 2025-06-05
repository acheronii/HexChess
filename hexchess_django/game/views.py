from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.template import loader

import sys

sys.path.append("C:/Users/jchur/Desktop/Code/HexChessProject/src")
from board import Board

# Create your views here.

board = Board()

def board_view(request):
    template = loader.get_template("game/board.html")
    context = {"board": board.as_json(),
               "turn": "White" if board.turn == 0 else "Black"
               }
    return HttpResponse(template.render(context, request))

def on_click(request):

    tile_id = request.POST.get('tile_id').split()
    board.on_click(int(tile_id[0]), int(tile_id[1]))
    template = loader.get_template("game/board.html")
    context = {"board": board.as_json(),
               "turn": "White" if board.turn == 0 else "Black"
               }
    return HttpResponse(template.render(context, request))


def move_piece(request):    
    template = loader.get_template("game/board.html")
    
    # Extract the actual coordinates 
    # TODO: change how this is done when i change the input format
    
    try: 
        from_str = request.POST['Hex_from']
        to_str = request.POST['Hex_to']
    except:
        context = {"board": board.as_json(), 
                   "error_message": "Please select a move"}
        return HttpResponse(template.render(context, request))
    
    from_q, from_r = from_str.split(" ")
    from_hex = (int(from_q), int(from_r))
    to_q, to_r = to_str.split(" ")
    to_hex = (int(to_q), int(to_r))

    if (not board.move_piece(from_hex, to_hex)):
        context = {"board": board.as_json(), 
                   "error_message": "Illegal Move"}
        return HttpResponse(template.render(context, request))

    context = {"board": board.as_json(), "change_message": f"Moved from {from_hex} to {to_hex}"}
    return HttpResponse(template.render(context, request))
