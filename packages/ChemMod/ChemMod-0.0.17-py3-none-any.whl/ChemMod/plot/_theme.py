def theme(color_theme):
  
  from ChemMod.plot import theme_data
  import ChemMod.plot

  def find_theme(request = None):
    if type(request)!=str and request != None:
      print('The F*ck What???!? That is not a godda*m name dude?')
    elif request == None:
      request = str(input('Hey there, I am your assistant. Please input the name of the theme here: ')).lower().strip()

    keys = []
    length = len(request)

    try:
      information = theme_data[request]
    except KeyError:

      request_parts = []

      for i in range(length-2):
        request_parts.append(request[i:i+3])

      try:

        key_set = theme_data.keys()
        for i in key_set:
          keys.append(i)

        probable_requests = []

        for i in range(len(theme_data)):
          if keys[i].startswith(request[0]):
            probable_requests.append(keys[i])

        probability = []

        for i in range(len(probable_requests)):
          probability_count = 0
          for j in range(len(request_parts)):
            if request_parts[j] in probable_requests[i]:
              probability_count += 1
            if probable_requests[i].startswith(request[:j+1]):
              probability_count += 1
          probability.append(probability_count)

        for i in range(len(probability)):
          if max(probability) == probability[i]:
            request = probable_requests[i]

        # if max(probability) == 0:
          
        information = theme_data[request]
      
      except KeyError:
        information = print('Sorry, but I was not able to find anything like that. Please try to write another name')
        return

    return information
  


  global theme_list_for_formatting_of_plots

  ChemMod.plot.theme_list_for_formatting_of_plots = find_theme(color_theme)
