class Payload:

    def __init__(self, value=None):
        self.value = value

    def v(self):
        return self.value

    def __setattr__(self, name, value):
        if (name == "v"):
            name = "value"

        # If value is a Payload copy in its value
        if isinstance(value, Payload):
            value = value.v()
            
        self.__dict__[name] = value

    def __iter__(self):
        for v in self.value:
            yield v

    def __bool__(self):
        return bool(self.value)
    
            
#
# Srtring operations
#

    def __str__(self):
        return "<%s> " % self.value.__str__()

    def __repr__(self):
        return ("%s" % self.value)

#
# Arithmetic operations
#
    def __add__(self, other):
        if isinstance(other, Payload):
            ans = self.value + other.value
        else:
            ans = self.value + other

        return Payload(ans)

    def __radd__(self, other):
        assert(not isinstance(other, Payload))
        return Payload(other + self.value)

    def __iadd__(self, other):
        if isinstance(other, Payload):
            self.value = self.value + other.value
        else:
            self.value = self.value + other
        return self

    def __sub__(self, other):
        if isinstance(other, Payload):
            ans = self.value - other.value
        else:
            ans = self.value - other

        return Payload(ans)

    def __rsub__(self, other):
#        print("Subing %s to %s" % (self.value, other))
        assert(not isinstance(other, Payload))
        return Payload(other - self.value)


    def __isub__(self, other):
        if isinstance(other, Payload):
            self.value = self.value - other.value
        else:
            self.value = self.value - other
        return self


    def __mul__(self, other):
        if isinstance(other, Payload):
            ans = self.value * other.value
        else:
            ans = self.value * other

        return Payload(ans)

    def __rmul__(self, other):
        assert(not isinstance(other, Payload))
        return Payload(other * self.value)


    def __imul__(self, other):
        if isinstance(other, Payload):
            self.value = self.value * other.value
        else:
            self.value = self.value * other
        return self


#
# Comparison operations
#

    def __eq__(self, other):
        if (isinstance(other, Payload)):
            return (self.value == other.value)
        else:
            return (self.value == other)

    def __ne__(self, other):
        if (isinstance(other, Payload)):
            return (self.value != other.value)
        else:
            return (self.value != other)


if __name__ == "__main__":

    a = Payload(1)
    print("A = %s" % a)
    print("---")

    b = Payload(1)
    print("B = %s" % b)
    print("---")

    a_plus_1 = a + 1
    print("A+1 = %s" % a_plus_1)
    print("---")

    a_plus_b = a + b
    print("A+B = %s" % a_plus_b)
    print("---")

    print("A = %s" % a)
    a += 1
    print("A+=1 = %s" % a)
    print("---")

    print("A = %s" % a)
    print("B = %s" % b)
    a += b
    print("A+=B = %s" % a)
    print("---")

    print("A = %s" % a)
    a_sub_1 = a - 1
    print("A-1 = %s"% a_sub_1)
    print("---")
    

    print("A = %s" % a)
    print("B = %s" % b)
    a_sub_b = a - b
    print("A-B = %s"% a_sub_b)
    print("---")
    

    print("A = %s" % a)
    a_mul_2 = a * 2
    print("A*2 = %s" % a_mul_2)
    print("---")

    print("A = %s" % a)
    two_mul_a = 2 * a
    print("2*A = %s" % two_mul_a)
    print("---")

    b = Payload(2)
    print("A = %s" % a)
    print("B = %s" % b)
    a_mul_b = a * b
    print("A*B = %s" % a_mul_b)
    print("---")

    print("A = %s" % a)
    a *= 2
    print("A*=2 = %s" % a)
    print("---")

    print("A = %s" % a)
    print("B = %s" % b)
    a *= b
    print("A*=B = %s" % a)
    print("---")


    c = Payload(8)
    d = Payload(8)
    e = Payload(1)
    print("C = %s" % c)
    print("D = %s" % d)
    print("E = %s" % e)

    print("C == D %s" % (c == d))
    print("C == E %s" % (c == e))
    print("C != D %s" % (c != d))
    print("C != E %s" % (c != e))
    print("C == 8 %s" % (c == 8))
    print("C == 1 %s" % (c == 1))
    print("C != 8 %s" % (c != 8))
    print("C != 1 %s" % (c != 1))

    print("8 == C %s" % (8 == c))
    print("1 == C %s" % (1 == c))
    print("8 != C %s" % (8 != c))
    print("1 != C %s" % (1 != c))


    
