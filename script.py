try:
    import secrets
    import psutil
    from multiprocessing import Pool
    import traceback
    import os
    import time
    import json
except ImportError as e:
    print('Failed to import module: {}'.format(e))
    print('Have you installed the requirements?')
    quit()


def clear_screen():
    # Clear screen command based on operating system
    os.system('cls' if os.name == 'nt' else 'clear')


class GenerateRandomKey:

    def __init__(self):
        try:
            self.rows, self.cols = self.generate_columns_and_rows()
            self.chart = self.generate_random_chart(self.rows, self.cols)
        except Exception as e:
            print(f"Error in __init__: {e}")
            traceback.print_exc()
            clear_screen()

    def generate_random_row(self, cols):
        try:
            row = []
            for _ in range(cols):
                random_char = chr(secrets.randbelow(95) + 32)
                row.append(random_char)
            return row
        except Exception as e:
            print(f"Error in generate_random_row: {e}")
            traceback.print_exc()
            clear_screen()

    def generate_random_chart(self, rows, cols):
        try:
            num_processes = psutil.cpu_count(logical=True)
            with Pool(num_processes) as pool:
                chart = pool.map(self._generate_random_row_wrapper,
                                 [cols] * rows)
            return chart
        except Exception as e:
            print(f"Error in generate_random_chart: {e}")
            traceback.print_exc()
            clear_screen()

    def _generate_random_row_wrapper(self, cols):
        try:
            return self.generate_random_row(cols)
        except Exception as e:
            print(f"Error in _generate_random_row_wrapper: {e}")
            traceback.print_exc()
            clear_screen()

    def generate_random_key(self, integer):
        try:
            key = []
            for _ in range(integer):
                x = secrets.randbelow(self.rows)
                y = secrets.randbelow(self.cols)
                char_at_position = self.chart[x][y]
                key.append((x, y, char_at_position))
            return key
        except Exception as e:
            print(f"Error in generate_random_key: {e}")
            traceback.print_exc()
            clear_screen()

    def generate_columns_and_rows(self):
        try:
            rows = secrets.randbelow(7500) + 250
            cols = secrets.randbelow(7500) + 250
            return rows, cols
        except Exception as e:
            print(f"Error in generate_columns_and_rows: {e}")
            traceback.print_exc()
            clear_screen()

    def generate_random_key_str(self, key, hex_length):
        try:
            key_str = ''.join([item[2] for item in key])
            frd = secrets.token_hex(int(hex_length))
            key_str += f"{frd}"
            return key_str, frd
        except Exception as e:
            print(f"Error in generate_random_key_str: {e}")
            traceback.print_exc()
            clear_screen()

    def save_generated_keys(self, json_data, filename="save.json"):
        try:
            with open(str(filename), 'w') as writeJson:
                writeJson.write(str(json_data))
        except Exception as e:
            print(f"Error in save_generated_keys: {e}")
            traceback.print_exc()
            clear_screen()

    def create_storage_object(self):
        try:
            return {"keys": [], "ids": []}
        except Exception as e:
            print(f"Error in create_storage_object: {e}")
            traceback.print_exc()
            clear_screen()


def generate_key(hex_length, key_length):
    try:
        generator = GenerateRandomKey()
        hashkey = generator.generate_random_key(int(key_length))
        real_key, idd = generator.generate_random_key_str(
            hashkey, int(hex_length))
        return real_key, idd
    except Exception as e:
        print(f"Error in generate_key: {e}")
        traceback.print_exc()
        clear_screen()

print('=' * 50)
print('Keygen CPU Test')
print('The Keygen CPU Test is a performance test for generating random keys.')
print(f"Time: {time.asctime()}")
print('=' * 50)
settings = {
  "use_static_num": False,
  "static_number": 50,
  "key_length": 255,
  "hex_length": 16
}
ifstat = settings['use_static_num']
key_length = settings['key_length']
hex_length = settings['hex_length']
if ifstat:
    num_static = settings['static_number']
    repetition = int(num_static)
else:
    num_cpus = psutil.cpu_count()
    repetition = int(num_cpus) * 5
    print(f'Using Dynamic Mode: {repetition} Keys')
try:
    start_time = time.time()
    keys_generated = 0
    memory_before = psutil.virtual_memory().used
    cpu_usage_data = []
    memory_usage_data = []
    key_rate_data = []
    for i in range(repetition):
        key, idd = generate_key(hex_length, key_length)
        print(f"Key: {key}\nID: {idd}")
        print(f"{i + 1}/{repetition}")
        keys_generated += 1
        # Collect data for plotting
        cpu_usage_data.append(psutil.cpu_percent())
        memory_usage_data.append(psutil.virtual_memory().used)
        key_rate_data.append(keys_generated / (time.time() - start_time))
    end_time = time.time()
    memory_after = psutil.virtual_memory().used
    memory_used = memory_after - memory_before
    print('=' * 50)
    print('Score:')
    print('The less, the better')
    print(f"Time Taken: {end_time - start_time}")
    print(f"Keys Generated: {keys_generated}")
    print(f"Memory Used: {memory_used} bytes")
    print(f"Key Generation Rate: {keys_generated / (end_time - start_time):.2f} keys/second")
    print('=' * 50)
except Exception as e:
    print(f"Error in main execution: {e}")
    traceback.print_exc()
    clear_screen()
