import json

from django.http import HttpResponse
from django.template import loader
from django.core.serializers.json import DjangoJSONEncoder
from django.contrib.auth.decorators import login_required

from apps.game.state import board

# Create your views here.


@login_required
def board_view(request):
    template = loader.get_template("game/board.html")
    context = {
        "user": request.user,
        "room_name": "room1",  # TODO edit this to be the actual room name for the board
        "board": board.as_json(),
        "winner": board.winner,
        "turn": "White" if board.turn == 0 else "Black",
        "legal_moves_json": json.dumps(board.legal_moves, cls=DjangoJSONEncoder),
    }
    return HttpResponse(template.render(context, request))
