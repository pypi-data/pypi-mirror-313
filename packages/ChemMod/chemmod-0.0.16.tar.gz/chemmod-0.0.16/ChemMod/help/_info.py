def info(request = None):
  '''\nInfo is a function that gives you info about a given function or element in your Package.
      \nIt can take a search string. It must be written as a string.
      \nFor instance 'bjerrum_plot'
      \nYou can also just type nothing in the function and it will ask you what you are looking for.
  \n-------------------------------------------------------------------
      \nTwo examples:
      \ninfo('bjerrum_plot')
      \n---Returns
      \ninformation about your bjerrum_plot function
      \ninfo()
      \n---Returns 
      \nHey there, I am your assistant. Please input the name of the function here: [_(type here)_]
      \nIf you write bjerrum_plot in the box you get information about your bjerrum_plot function:)
  '''
  from ChemMod.help import content_data

  if type(request)!=str and request != None:
    print('The F*ck What???!? That is not a godda*m name dude?')
  elif request == None:
    request = str(input('Hey there, I am your assistant. Please input the name of the function here: ')).lower().strip()

  keys = []
  length = len(request)

  try:
    information = print(content_data[request]['Info'])
  except KeyError:

    request_parts = []

    for i in range(length-2):
      request_parts.append(request[i:i+3])

    try:

      key_set = content_data.keys()
      for i in key_set:
        keys.append(i)

      probable_requests = []

      for i in range(len(content_data)):
        if keys[i].startswith(request[0]):
          probable_requests.append(keys[i])

      print(probable_requests)

      probability = []

      for i in range(len(probable_requests)):
        probability_count = 0
        for j in range(len(request_parts)):
          if request_parts[j] in probable_requests[i]:
            probability_count += 1
          if probable_requests[i].startswith(request[:j+1]):
            probability_count += 1
        probability.append(probability_count)

      print(probability)

      for i in range(len(probability)):
        if max(probability) == probability[i]:
          request = probable_requests[i]

      # if max(probability) == 0:



      information = print(content_data[request]['Info'])

    except KeyError:
      information = print('Sorry, but I was not able to find anything like that. Please try to write another name')
      return


  return information

