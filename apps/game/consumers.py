import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.core.serializers.json import DjangoJSONEncoder

from apps.game.state import boards


class GameConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"{self.room_name}"
        user = self.scope["user"]
        print(f"Room [{self.room_group_name}] User connected: {user.username}")

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)

        message_type = data.get("type")

        board = boards[self.room_group_name]["board"]

        # should never happen, but tell to refresh the page if it doesnt exist (creates a game)
        if not board:  # TODO send an error
            await self.channel_layer.group_send(
                self.room_group_name, {"type": "broadcast_reset"}
            )

        if message_type == "color_choose":
            board.players[data.get("color")] = self.scope["user"].username
            # send to all that there is a player of that color and who the
            # player is. they should remove that button
            response = {
                "type": "color_choose",
                "color": data.get("color"),
                "player": self.scope["user"].username,
            }
            await self.channel_layer.group_send(
                self.room_group_name,
                {"type": "broadcast_color_choose", "data": response},
            )

        elif message_type == "move":
            move = data.get("move")
            player = self.scope["user"].username
            print(f"Room [{self.room_group_name}]: Move {move} made by {player}")

            # verify that the player can make a move
            current_turn = board.turn
            if (
                (current_turn == 0 and player != board.players["white"])
                or current_turn == 1
                and player != board.players["black"]
            ):
                await self.send(
                    text_data=json.dumps(
                        {
                            "type": "error",
                            "error": "You are not allowed to make this move.",
                        }
                    )
                )
                return

            fro, to = move.split(">")
            if fro in board.legal_moves.keys() and to in board.legal_moves[fro]:
                # convert locations to ints
                fro = [int(x) for x in fro.split("_")]
                to = [int(x) for x in to.split("_")]
                # move the piece
                board.move_piece((int(fro[0]), int(fro[1])), (int(to[0]), int(to[1])))
                board.next_turn()

                response = {
                    "type": "move",
                    "move": move,
                    "turn": "White" if board.turn == 0 else "Black",
                    "winner": board.winner,
                    "check": board.check,
                    "legal_moves_json": json.dumps(
                        board.legal_moves, cls=DjangoJSONEncoder
                    ),
                }
            else:
                await self.send(
                    text_data=json.dumps(
                        {
                            "type": "error",
                            "error": "You are not allowed to make this move.",
                        }
                    )
                )
                return
            # response = {"move": move}
            await self.channel_layer.group_send(
                self.room_group_name, {"type": "broadcast_move", "data": response}
            )
        elif message_type == "reset":
            board.__init__()
            await self.channel_layer.group_send(
                self.room_group_name, {"type": "broadcast_reset"}
            )

    async def broadcast_reset(self, event):
        await self.send(text_data=json.dumps({"type": "reset"}))

    async def broadcast_move(self, event):
        await self.send(text_data=json.dumps(event["data"]))

    async def broadcast_color_choose(self, event):
        await self.send(text_data=json.dumps(event["data"]))
