from rcon_protocol import Rcon

class RCON():
    def __init__(self):
        self.conn = Rcon('192.168.0.7', 'test123')
        self.conn.connect()
        
        self.whitelist = RCON.whitelist(self)
        self.op = RCON.op(self)

    class op:
        def __init__(self, rcon):
            self.rcon = rcon

        def add(self, nickname):
            return self.rcon.conn.command(f'/op {nickname}')
        
        def remove(self, nickname):
            return self.rcon.conn.command(f'/deop {nickname}')

    class whitelist:
        def __init__(self, rcon):
            self.rcon = rcon

        def enable(self):
            return self.rcon.conn.command('/whitelist on')

        def refresh(self):
            return self.rcon.conn.command('/whitelist reload')

        def add(self, nickname):
            return self.rcon.conn.command(f'/whitelist add {nickname}')

        def remove(self, nickname):
            return self.rcon.conn.command(f'/whitelist remove {nickname}')
    
    def online_players(self):
        return self.conn.command('/list')[+39].split()
    
    def online_status(self):
        return '/'.join([s for s in self.conn.command('/list').split() if s.isdigit()])

    def change_time(self, time):
        return self.conn.command(f'/time set {time}')

    def change_weather(self, w_type):
        return self.conn.command(f'/weather {w_type}')
    
    def give_item(self, nickname, item_id, amount):
        return self.conn.command(f'/give {nickname} {item_id} {amount}')

rcon = RCON()