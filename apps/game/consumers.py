import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.core.serializers.json import DjangoJSONEncoder

from apps.game.state import board
# from . import board


class GameConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"game_{self.room_name}"

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)

        move = data.get("move")
        # player = self.scope["user"].username

        """
        TODO add validation for player and move, form payload to send to the javascript
        something like :
            # Check that the player is the correct player
            current_turn = board.turn
            if (current_turn == 0 and user != room.white_player) or \
                (current_turn == 1 and user != room.black_player):
                    # Not this user's turn — reject
                    await self.send(text_data=json.dumps({
                        "error": "You are not allowed to make this move."
                    }))
                    return

            # 1. Apply the move (this modifies your game state on the backend)
            # look at views.ajax_move_view to copy for this
            board.move_piece(from_pos, to_pos)
            board.next_turn()

            # 2. Prepare all state you want the clients to know
            response = {
                "move": move_str, # for displaying the change
                "turn": "White" if board.turn == 0 else "Black",
                "winner": board.winner,
                "legal_moves_json": json.dumps(board.legal_moves, cls=DjangoJSONEncoder),
                # optionally, board diff or full board state
            }

            # 3. Broadcast to all clients in room
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "broadcast_move",
                    "payload": response
                }

        """

        fro, to = move.split(">")
        if fro in board.legal_moves.keys() and to in board.legal_moves[fro]:
            # convert locations to ints
            fro = [int(x) for x in fro.split("_")]
            to = [int(x) for x in to.split("_")]
            # move the piece
            board.move_piece((int(fro[0]), int(fro[1])), (int(to[0]), int(to[1])))
            board.next_turn()
            response = {
                "move": move,
                "turn": "White" if board.turn == 0 else "Black",
                "winner": board.winner,
                "check": board.check,
                "legal_moves_json": json.dumps(
                    board.legal_moves, cls=DjangoJSONEncoder
                ),
            }
        else:
            response = {"reload": "True"}
        # response = {"move": move}
        await self.channel_layer.group_send(
            self.room_group_name, {"type": "broadcast_move", "data": response}
        )

    async def broadcast_move(self, event):
        await self.send(text_data=json.dumps(event["data"]))
