from vkbottle.bot import Bot
from vkcoinapi import *
from SimpleQIWI import QApi


# Токены
token = "vk1.a.-X-Oar_fCt2sMnZL_F2LHeNL9P8Uu9CbVpEBe2d1AWtHr4Ez-JDPf60irJx8jV0ED8I932o9TimeOkcqaijzb-iTw9h6362un_kQNn7s82IzE7__Sc86Deym-vIOiR9rGZODcL8ca4JNNTMBBfBZq2GDyIRtnALNR6S6pH0IuPBz1NZfU36zRcWli0_32AqK"
user_id="722870620"
key

qtoken="b992a735a9a34a0a08dee84c785c45f3"
phone = "vk1.a.2X6PoViiUc_7kxA8jRZOglLY3Xd96xnFyhnyVdSfG3s9zaSYL3DsMGI17b5CqhPjZMz6CYgH7h_cc6WQrgXWxd1xqyoqHtkijsNUX064QNvYdEp3Lt_xsldZSJUVyCTTPpKcyHq2PrPa8xby5xTSURydQMPnddS60MHez3LmtbJIePXJr9x9qPdCEVtePloO"

# Переменные
coin = VKCoin(key = key, merchantId = user_id)
reserve_vkc = (coin.getBalance())["response"][str(user_id)]/1000
print(reserve_vkc)
api = QApi(token=qtoken, phone=phone)
admins = [362948702]