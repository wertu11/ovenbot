class A:
    def __init__(self):
        self.value = 5
class B(A):
 def __init__(self):
    super().__init__()
    self.value += 5
obj = B()
print(obj.value)
