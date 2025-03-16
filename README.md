fix  <svg> <input type=radio name=choice id=choice{{forloop.counter}} value=choice.id> </svg>  
into <svg> <input type=radio name=choice id=choice{{forloop.counter}} value={{choice.id}}> </svg>
