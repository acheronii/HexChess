import json

from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
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


def flip_board(request):
    flipped = request.session.get("flipped", False)
    request.session["flipped"] = not flipped
    return HttpResponseRedirect(reverse("game:game_page"))


def ajax_move_view(request):
    if request.method == "POST":
        fro, to = request.POST.get("move").split(">")
        # sanitize to make sure that we are only moving if the move is legal
        if fro in board.legal_moves.keys() and to in board.legal_moves[fro]:
            # convert locations to ints
            fro = [int(x) for x in fro.split("_")]
            to = [int(x) for x in to.split("_")]
            # move the piece
            board.move_piece((int(fro[0]), int(fro[1])), (int(to[0]), int(to[1])))
            board.next_turn()
        else:
            return JsonResponse({"reload": "True"}, status=200)
        return JsonResponse(
            {
                "winner": board.winner,
                "turn": "White" if board.turn == 0 else "Black",
                "check": board.check,
                "legal_moves_json": json.dumps(
                    board.legal_moves, cls=DjangoJSONEncoder
                ),
            }
        )
    return JsonResponse({"error": "Invalid Request"}, status=400)
