from async_tkinter_loop import async_handler
import asyncio

class Write_And_Verify_Char:
    def __init__(self, client, textboxes):
        self.client = client
        self.textboxes = textboxes

    @async_handler
    async def write_and_verify_characteristic(self, CHARACTERISTIC_UUID):
        if not self.client:
            print("No device connected")
            return

        data_to_write = self.get_data()

        await self.client.write_gatt_char(CHARACTERISTIC_UUID, data_to_write, response=True)

        await asyncio.sleep(0.1)

        read_data = await self.client.read_gatt_char(CHARACTERISTIC_UUID)

        if data_to_write == read_data:
            print("Write success")
        else:
            print("Data mismatch")

    def get_data(self):
        data_array = []

        for textbox in self.textboxes:
            text = textbox.get("1.0", "end-1c").strip()
            if text:
                try:
                    data_array.append(int(text))
                except ValueError:
                    print(f"Invalid input in a textbox: {text}")
            else:
                data_array.append(0)

        return bytearray(data_array)

