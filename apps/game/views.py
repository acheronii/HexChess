import json

from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.template import loader
from django.core.serializers.json import DjangoJSONEncoder
from django.contrib.auth.decorators import login_required

from apps.game.state import board

# Create your views here.


@login_required
def board_view(request):
    flipped = request.session.get("flipped", False)
    template = loader.get_template("game/board.html")
    context = {
        "user": request.user,
        "room_name": "room1",  # TODO edit this to be the actual room name for the board
        "board": board.as_json(flipped),
        "winner": board.winner,
        "turn": "White" if board.turn == 0 else "Black",
        "legal_moves_json": json.dumps(board.legal_moves, cls=DjangoJSONEncoder),
    }
    return HttpResponse(template.render(context, request))


def reset_board(request):
    if request.method == "POST":
        board.__init__()
        request.session["flipped"] = False
        return HttpResponseRedirect(reverse("game:game_page"))
