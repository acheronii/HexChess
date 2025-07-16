import json

from django.http import HttpResponse
from django.template import loader
from django.core.serializers.json import DjangoJSONEncoder
from django.contrib.auth.decorators import login_required

from apps.game.state import boards
from engine.board import Board

# Create your views here.


@login_required
def game_index_view(request):
    nums = [int(x) for x in boards.keys() if x.isnumeric()]
    new_board_num = 1 + max(nums) if nums else 1

    template = loader.get_template("game/index.html")
    context = {
        "Board_list": boards,
        "new_board_num": new_board_num,
    }
    return HttpResponse(template.render(context, request))


@login_required
def board_view(request, room):
    if room in boards.keys():
        board = boards[room]["board"]
    else:
        boards[room] = {}
        boards[room]["board"] = Board()
        board = boards[room]["board"]

    template = loader.get_template("game/board.html")
    context = {
        "user": request.user,
        "room_name": room,
        "board": board.as_json(),
        "winner": board.winner,
        "turn": "White" if board.turn == 0 else "Black",
        "legal_moves_json": json.dumps(board.legal_moves, cls=DjangoJSONEncoder),
    }
    return HttpResponse(template.render(context, request))
