
class State:
    '''State is used to predict the next branch (jump or no jump)

    Args:
        :param ``size_bit``: the size of bit each state has
        :param ``value``: set a start value in decimal (between 0 and highest possible with n bits)

    self.value is a string representing a binary number
    '''

    def __init__(self, size_bit=2, value = "0b0") -> None:
        self.size_bit = size_bit
        if size_bit <= 0:
            self.size_bit = 2 

        self.value = "0b0"
        self.set_val(value)



    def get_val(self, bin=False):
        r'''return value of state as binary or decimal'''
        if bin:
            return self.value
        else:
            return int(self.value, 2)



    def set_val(self, val):
        r'''Set value of state

            :param ``val``: binary number ("0b101")
        '''
        self.value = "0b" + (self.size_bit - len(val) + 2)*"0" + val[2:]                # +2 for "0b" which aren't counted for size_bit



    def set_state(self, actual):
        r'''Set value depending on actual

        Args:
            :param ``actual``: outcome of branch
        '''
        if actual == "0":                 # no Jump
            self.no_jump()
        if actual == "1":                 # Jump
            self.jump()   



    def no_jump(self):
        r'''decrement value by 1'''
        if( self.get_val() != 0 ):                                                      # not zero 
            bin_num = bin( int(self.value, 2) - 1 )
            self.set_val(bin_num)



    def jump(self):
        r'''increment value by 1'''
        if( self.get_val() < pow(2, self.size_bit)-1 ):                                 # smaller than highest number ( 2^size_bit -1 )
            bin_num = bin( int(self.value, 2) + 1 )
            self.set_val(bin_num)



    def get_jump_val(self):
        r'''Return jump value of state.
        
        - In the lower half of the possible value range (depending on size_bit) return ``0``.
        - Otherwise return ``1``.
        '''

        if( self.get_val() < pow(2, self.size_bit-1)):    
            return "0"
        else:
            return "1"



    def left_shift(self, x):
        r'''Shift the value to the left and push x from the right and return the binary value
        
        Args:    
            :param :char(0/1) ``x``: A bit that is shifted from the right side

        In Detail:
            Iterate through value and move all values without the first two (0b)
        '''

        new_value = "0b"
        for i in range( len(self.value) ):
            if(i<=2):
                continue
            new_value += self.value[i]
        new_value += str(x)

        self.set_val(new_value)
        return new_value


    
    def xor_address(self, address):
        r'''XOR the value of the state with a address

        Args:
            :param ``address``: hex address to xor with the state
        '''

        address_str =   bin( int(address, 16) )                         # Convert address to binary
        address_str = "0b" + self.size_bit * '0' + address_str[2:]      # Fill with '0's, depending on size_bit
        address_str = address_str[-self.size_bit:]                      # Cut the end

        # XOR the cut address with the state value
        xor_address = int(address_str, 2) ^ int(self.value, 2)          # XOR the int values of address and state value
        return bin(xor_address)