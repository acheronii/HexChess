from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.template import loader

from engine.board import Board

# Create your views here.

board = Board()


def board_view(request):
    template = loader.get_template("game/board.html")
    context = {
        "board": board.as_json(),
        "turn": "White" if board.turn == 0 else "Black",
    }
    return HttpResponse(template.render(context, request))


def on_click(request):
    tile_id = request.POST.get("tile_id").split()
    board.on_click(int(tile_id[0]), int(tile_id[1]))
    return HttpResponseRedirect(reverse("game:game_page"))


def reset_board(request):
    board.__init__()
    return HttpResponseRedirect(reverse("game:game_page"))


def flip_board(request):
    raise NotImplementedError("achii has not done this yeet")
    board.flip()
    return HttpResponseRedirect(reverse("game:game_page"))
