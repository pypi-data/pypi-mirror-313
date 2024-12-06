from enum import Enum,auto

class instruction(Enum):
    sa = auto()
    sb = auto()
    pa = auto()
    pb = auto()
    ra = auto()
    rb = auto()
    rr = auto()
    rra = auto()
    rrb = auto()
    rrr = auto()

class push_swap:
    def __init__(self, stack_a:list[int], print_flag:bool = True):
        self.stack_a = stack_a
        self.stack_b = []
        self.step = 0
        self.print_flag = print_flag

    def sa(self):
        if 2 <= len(self.stack_a):
            self.stack_a[0],self.stack_a[1] = self.stack_a[1], self.stack_a[0]

    def sb(self):
        if 2 <= len(self.stack_b):
            self.stack_b[0],self.stack_b[1] = self.stack_b[1], self.stack_b[0]

    def ss(self):
        self.sa()
        self.sb()

    def pa(self):
        if 0 < len(self.stack_b):
            self.stack_a.insert(0,self.stack_b.pop(0))

    def pb(self):
        if 0 < len(self.stack_a):
            self.stack_b.insert(0,self.stack_a.pop(0))

    def ra(self):
        self.stack_a.append(self.stack_a.pop(0))

    def rb(self):
        self.stack_b.append(self.stack_b.pop(0))
    
    def rr(self):
        self.ra()
        self.rb()

    def rra(self):
        self.stack_a.insert(0,self.stack_a.pop())

    def rrb(self):
        self.stack_b.insert(0,self.stack_b.pop())

    def rrr(self):
        self.rra()
        self.rrb()

    def run(self, command:instruction):
        self.step += 1
        match command:
            case instruction.sa:
                self.sa()
            case instruction.sb:
                self.sb()
            case instruction.pa:
                self.pa()
            case instruction.pb:
                self.pb()
            case instruction.ra:
                self.ra()
            case instruction.rb:
                self.rb()
            case instruction.rr:
                self.rr()
            case instruction.rra:
                self.rra()
            case instruction.rrb:
                self.rrb()
            case instruction.rrr:
                self.rrr()
            case _:
                raise BaseException("Error!")
        if self.print_flag:
            print(command.name)

    def runcmd(self, command:str):
        if command == "":
            return 
        self.step += 1
        match command:
            case "sa":
                self.sa()
            case "sb":
                self.sb()
            case "pa":
                self.pa()
            case "pb":
                self.pb()
            case "ra":
                self.ra()
            case "rb":
                self.rb()
            case "rr":
                self.rr()
            case "rra":
                self.rra()
            case "rrb":
                self.rrb()
            case "rrr":
                self.rrr()
            case _:
                raise BaseException(f"command \"{command}\" not found")
                self.step -= 1
        # if self.print_flag:
        #     print(command.name)

    def inverce_runcmd(self, command:str):
        self.runcmd(self.inverse_func(command))

    def inverse_func(self, command:str) -> str:
        # 逆関数
        # sa <-> sa
        # sb <-> sb
        # pa <-> pb
        # pb <-> pa
        # ra <-> rra
        # rra <-> ra
        # rb <-> rrb
        # rrb <-> rb
        # rr <-> rrr
        # rrr <-> rr
        self.step -= 2
        match command:
            case "sa":
                return "sa"
            case "sb":
                return "sb"
            case "pa":
                return "pb"
            case "pb":
                return "pa"
            case "ra":
                return "rra"
            case "rb":
                return "rrb"
            case "rr":
                return "rrr"
            case "rra":
                return "ra"
            case "rrb":
                return "rb"
            case "rrr":
                return "rr"
            case _:
                # raise BaseException("Error!")
                return ""


