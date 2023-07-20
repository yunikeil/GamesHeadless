import time
import asyncio


class Timeout:
    bot = None
    objects = {}

    def __init__(self, chat_id, message_id, timeout=5*60):
        # TODO или переписать на получение объекта сообщения или переписать update_message
        if timeout == None: 
            return
        self.objects[f"{chat_id}:{message_id}"] = self
        print(f"New timeot: {chat_id}:{message_id}, temouts:\n", self.objects)
        self.update(chat_id, message_id)
        self.chat_id = chat_id
        self.message_id = message_id
        self.timeout = timeout
        loop = asyncio.get_running_loop()
        loop.create_task(self.sleep_until_timeout())

    @classmethod
    def update(cls, chat_id, message_id, timeout=5*60):
        try:
            timeout = cls.objects[f"{chat_id}:{message_id}"]
            print("Updated!")
            timeout.last_update_time = time.time()
        except KeyError:
            Timeout(chat_id, message_id, timeout)
    
    @classmethod
    def remove(cls, chat_id, message_id, timeout=5*60):
        try:
            timeout = cls.objects[f"{chat_id}:{message_id}"]
            print("Removed!")
            timeout.objects.pop(f"{chat_id}:{message_id}")
        except KeyError:
            print("Removed!")
            pass

    async def update_message(self):
        print("Msg updated!")
        message = self.bot.get_message(chat_id=self.chat_id, message_id=self.message_id)
        self.bot.edit_message_text(
            chat_id=self.chat_id,
            message_id=self.message_id,
            text=message.text,
            reply_markup=None
        )

    async def sleep_until_timeout(self):
        await asyncio.sleep(self.timeout)
        while True:
            now_time = time.time()
            time_diff = self.last_update_time + self.timeout - now_time

            if time_diff <= 0:
                try:
                    await self.update_message()
                except Exception as e:
                    print(f"Failed to delete message: {e}")
                break
            await asyncio.sleep(time_diff)


if __name__ == "__main__":
    timeout = Timeout(None, 123, 321, 600)

    print(Timeout.objects)

    timeout1 = Timeout(None, 1234, 3211, 600)

    print(Timeout.objects)

    timeout.remove()

    print(Timeout.objects)
