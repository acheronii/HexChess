from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.template import loader

from engine.board import Board

# Create your views here.

board = Board()


def board_view(request):
    flipped = request.session.get("flipped", False)
    template = loader.get_template("game/board.html")
    context = {
        "board": board.as_json(flipped),
        "turn": "White" if board.turn == 0 else "Black",
    }
    return HttpResponse(template.render(context, request))


def on_click(request):
    if request.method == "POST":
        tile_id = request.POST.get("tile_id").split()
        if board.on_click(int(tile_id[0]), int(tile_id[1])):
            return HttpResponseRedirect(reverse("game:flip"))
        else:
            return HttpResponseRedirect(reverse("game:game_page"))


def reset_board(request):
    if request.method == "POST":
        board.__init__()
        request.session["flipped"] = False
        return HttpResponseRedirect(reverse("game:game_page"))


def flip_board(request):
    flipped = request.session.get("flipped", False)
    request.session["flipped"] = not flipped
    return HttpResponseRedirect(reverse("game:game_page"))
