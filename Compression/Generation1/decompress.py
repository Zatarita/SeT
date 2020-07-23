import zlib, shutil

class h1a_compressed_data():
    name = ""
    data = None
    decompressed_data = []

    count = 0
    offsets = []
    sizes = []
    blocks = []

    def __init__(self,data = None, percent_hook = None, status_hook = None):
        if data: self.data = data
        if percent_hook: self.percentage_changed = percent_hook
        if status_hook: self.status_changed = status_hook
        if data: self.load_data(self.data)

    def load_data(self, data):
        #remove old data
        self.blocks.clear()
        self.sizes.clear()
        self.offsets.clear()

        self.count = int.from_bytes(self.data[0:4], "little")

        self.status_changed("Loading data from offsets...")
        self.percentage_changed(0.00)

        self.status_changed("Parsing offsets...")
        for i in range(self.count):
            self.percentage_changed(float(i)/self.count / 3)
            self.offsets.append(int.from_bytes(self.data[4 + 4*i: 8 + 4*i], "little"))
        self.offsets.append(len(self.data))

        self.status_changed("Calculating sizes...")
        self.percentage_changed(0.33)
        for i in range(len(self.offsets) - 1):
            self.percentage_changed(0.33 + (float(i)/self.count / 3))
            self.sizes.append(self.offsets[i+1] - self.offsets[i])
        self.offsets.pop()

        self.status_changed("Loading data...")
        self.percentage_changed(0.66)
        for i in range(self.count):
            self.percentage_changed(0.66 + (float(i)/self.count / 3))
            self.blocks.append(self.data[self.offsets[i] + 4:self.offsets[i] + 4 + self.sizes[i]])

        self.status_changed("File loaded!")
        self.percentage_changed(1.00)

    def decompress(self):
        self.status_changed("Decompressing blocks...")
        for i in range(len(self.blocks)):
            self.percentage_changed(float(i)/len(self.blocks))
            self.decompressed_data.append(zlib.decompress(self.blocks[i]))
        self.status_changed("Done!")
        return b''.join(self.decompressed_data)

    def save(self, path):
        with open(path, "wb") as file:
            if len(self.decompressed_data) == 0: return

            self.status_changed("Writing file...")
            for i in range(len(self.decompressed_data)):
                self.percentage_changed(float(i)/len(self.decompressed_data))
                file.write(self.decompressed_data[i])

    def percentage_changed(self, percentage):
        pass

    def status_changed(self, status):
        pass
