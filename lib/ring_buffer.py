class CRingBuffer:
  def __init__(self,size=20):
    self.__size=size
    self.__the_buffer = [None for i in range(size)]
    self.__tail = 0
    self.__head = 0
  
  def add(self,element):
      self.__the_buffer[self.__head] = element
      self.__head += 1
      if self.__head == self.__size:
          self.__head = 0
      if self.__head == self.__tail:
          self.__tail += 1
      if self.__tail == self.__size:
          self.__tail = 0

  def get_size(self):
      return self.__size
      
  def get_all(self):
      my_list = []
      if self.__tail > self.__head:
          for i in range(self.__tail-1,self.__size):
              if not self.__the_buffer[i] == None:
                  my_list.append(self.__the_buffer[i])        
          for i in range(0,self.__head):
              if not self.__the_buffer[i] == None:
                  my_list.append(self.__the_buffer[i])        
      elif self.__head - self.__tail == self.__size - 1:
          if not self.__the_buffer[self.__size - 1] == None:
              my_list.append(self.__the_buffer[self.__size - 1])
          for i in range(self.__tail, self.__head):
              if not self.__the_buffer[i] == None:
                  my_list.append(self.__the_buffer[i])
      else:
          for i in range(self.__tail,self.__head):
                  if not self.__the_buffer[i] == None:
                      my_list.append(self.__the_buffer[i])
      return my_list      


if __name__ =="__main__":
    my_ringbuffer = CRingBuffer(10)
    for i in range(1,5):
        my_ringbuffer.add(i)
        
    the_result = my_ringbuffer.get_all()
    for i in range (0, len(the_result)):
        if not the_result[i] == None:
            print(the_result[i])
        else:
            print("Oh..., None")
             

