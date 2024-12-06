#  Pyrogram - Telegram MTProto API Client Library for Python
#  Copyright (C) 2017-present Dan <https://github.com/delivrance>
#
#  This file is part of Pyrogram.
#
#  Pyrogram is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published
#  by the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  Pyrogram is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with Pyrogram.  If not, see <http://www.gnu.org/licenses/>.

from io import BytesIO

from pyrogram.raw.core.primitives import Int, Long, Int128, Int256, Bool, Bytes, String, Double, Vector
from pyrogram.raw.core import TLObject
from pyrogram import raw
from typing import List, Optional, Any

# # # # # # # # # # # # # # # # # # # # # # # #
#               !!! WARNING !!!               #
#          This is a generated file!          #
# All changes made in this file will be lost! #
# # # # # # # # # # # # # # # # # # # # # # # #


class SendPaidReaction(TLObject):  # type: ignore
    """Sends one or more paid Telegram Star reactions », transferring Telegram Stars » to a channel's balance.


    Details:
        - Layer: ``195``
        - ID: ``9DD6A67B``

    Parameters:
        peer (:obj:`InputPeer <pyrogram.raw.base.InputPeer>`):
            The channel

        msg_id (``int`` ``32-bit``):
            The message to react to

        count (``int`` ``32-bit``):
            The number of stars to send (each will increment the reaction counter by one).

        random_id (``int`` ``64-bit``):
            Unique client message ID required to prevent message resending

        private (``bool``, *optional*):
            Each post with star reactions has a leaderboard with the top senders, but users can opt out of appearing there if they prefer more privacy.  If the user explicitly chose to make their paid reaction(s) private, pass boolTrue to messages.sendPaidReaction.private.  If the user explicitly chose to make their paid reaction(s) private, pass boolFalse to messages.sendPaidReaction.private.  If the user did not make any explicit choice about the privacy of their paid reaction(s) (i.e. when reacting by clicking on an existing star reaction on a message), do not populate the messages.sendPaidReaction.private flag.

    Returns:
        :obj:`Updates <pyrogram.raw.base.Updates>`
    """

    __slots__: List[str] = ["peer", "msg_id", "count", "random_id", "private"]

    ID = 0x9dd6a67b
    QUALNAME = "functions.messages.SendPaidReaction"

    def __init__(self, *, peer: "raw.base.InputPeer", msg_id: int, count: int, random_id: int, private: Optional[bool] = None) -> None:
        self.peer = peer  # InputPeer
        self.msg_id = msg_id  # int
        self.count = count  # int
        self.random_id = random_id  # long
        self.private = private  # flags.0?Bool

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "SendPaidReaction":
        
        flags = Int.read(b)
        
        peer = TLObject.read(b)
        
        msg_id = Int.read(b)
        
        count = Int.read(b)
        
        random_id = Long.read(b)
        
        private = Bool.read(b) if flags & (1 << 0) else None
        return SendPaidReaction(peer=peer, msg_id=msg_id, count=count, random_id=random_id, private=private)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 0) if self.private is not None else 0
        b.write(Int(flags))
        
        b.write(self.peer.write())
        
        b.write(Int(self.msg_id))
        
        b.write(Int(self.count))
        
        b.write(Long(self.random_id))
        
        if self.private is not None:
            b.write(Bool(self.private))
        
        return b.getvalue()
