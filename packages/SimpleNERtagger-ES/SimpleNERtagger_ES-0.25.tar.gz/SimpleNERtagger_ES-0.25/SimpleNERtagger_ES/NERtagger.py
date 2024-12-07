import re
import pandas as pd

from transformers import AutoTokenizer, AutoModelForTokenClassification
from transformers import pipeline

#NER tagger en español versión 2.
#Por: Jesús Armenta-Segura. CIC-IPN, IFE:LL&DH@ITESM
#Revisar documentación para ver el changelog con respecto a la versión 1.
#En la versión 3 se incluirán modelos vía ollama para taggear puestos, hora/momento y relaciones interpersonales.
class NER_tagger:
  def __init__(self, transformer):
    self.transformer = transformer
    if self.transformer: #Si se declara un transformer, se carga.
      try:
        self.tokenizer = AutoTokenizer.from_pretrained(self.transformer)
        self.model = AutoModelForTokenClassification.from_pretrained(self.transformer)
        self.nlp = pipeline("ner", model=self.model, tokenizer=self.tokenizer, aggregation_strategy="average") #V2.4 añade aggregation strategy para ya no utilizar el algoritmo raro de reunificación de tokens.
        print(f"\nTransformer cargado: {self.transformer}")
      except:
        print(f"\nError al cargar el transformer {self.transformer}, se procederá sin transformer (no se marcarán ni nombres ni lugares)")
    else:
      print("\nNo se ha cargado ningún transformer. Imposible marcar por nombre o lugar.")
      return

  #ESTA FUNCIÓN:
  #Corre el NER-tagger del transformer.
  #Reunifica las palabras partidas por el auto-tokenizador.
  #Finalmente regresa los tags en formato DataFrame con columnas tag, palabra, start y end. Si no hay palabras taggeadas, regresa el diccionario con listas vacías como valor.
  def tag_transformer(self, text, dict_tag):
    ## PASO 1: Los taggers usuales regresan tags en el formato BIO.
    dict_tags = []
    for targ in dict_tag:
      dict_tags += [{'tag':targ, 'palabra':x['word'], 'start':x['start'],'end':x['end'], 'index':x['index']} for x in self.tags if x['entity_group'] in dict_tag[targ]] # self.tags se define en otras funciones, y consiste en el resultado del BERT-NERTagger ya ejecutado sobre el texto.

    dict_tags = sorted(dict_tags, key=lambda x: x["index"]) #Ordenados por orden de aparición.

    ##### V2.4 utiliza aggregation_strat=Average, lo que hace que esto ya no sea más necesario:
    # Reunificamos palabras partidas por el tokenizador de BERT: "Pa, ##lab ##ra" ---> "Palabra"
    #z = 0 #Con esta variable, nos ahorramos un chorro de recursos para evitar iterar sobre todo dict_tags una-y-otra-vez.
    #to_delete = []
    #for y in dict_tags: # Iterando en orden de aparición
    #  if y['palabra'][:2] == "##": # Debido a la naturaleza del tokenizador de BERT, esto nunca se alcanzará en la primera iteración, a menos que un chistocito arruine el programa metiendo un texto que inicie con "##".
    #    try: # Sólo podría fallar en la primera iteración del for.
    #      y['palabra'] = z['palabra'] + y['palabra'][2:] # Reunificamos la palabra.
    #    except:
    #      raise Exception("Un chistosito pensó que sería divertido iniciar su reporte con '##'. Soluciónalo eliminando dichos caracteres especiales del inicio.")
    #    y['start'] = z['start'] # Ahora el inicio de la palabra será el inicio de la primera mitad.
    #    to_delete.append(z) #Borraremos este z ya que y ha tomado su lugar.
    #    z = y # Considerando el caso de que una palabra se divida en más de dos partes. IMPORTANTE QUE SE EJECUTE HASTA LO ÚLTIMO DE LA ITERACIÓN.
    #  else:
    #    z = y
    #for x in to_delete:
    #  dict_tags.remove(x)

    final_tags = {'tag':[x['tag'] for x in dict_tags], 'palabra':[x['palabra'] for x in dict_tags], 'start':[x['start'] for x in dict_tags],'end':[x['end'] for x in dict_tags]} # dict_tags pero sin el index de token y en formato de DataFrame.

    return final_tags


  #ESTA FUNCIÓN:
  #Usa la librería regex para compilar la gramática Backus-Naur que genera (casi) todos los emails del mundo.
  #Usa esa gramática para encontrar dichos patrones en el texto
  #Considera dos casos: con TLD y sin TLD.
  #Al final, captura ambos casos evitando redundancias.
  def tag_emails(self, text, tag):
    #Construcción de la gramática Backus-Naur que genera (casi) todos los emails del mundo.
    DOM = r"[a-zA-Z0-9-_àèìòùäëïöüáéíóúç+*]+"               # DOM  ::= Dominio de internet. Puede ser tan simple como "yahoo", o tan complicado como "deez-natz-funny". El TLD es considerado más adelante.
    USER = r"[a-zA-Z0-9-_àèìòùäëïöüáéíóúç+*.]+"             # USER ::= Algún string sin caracteres raros.
    TLD = r"\.[a-zA-Z0-9-_àèìòùäëïöüáéíóúç+*]+(?:\.[a-zA-Z0-9-_àèìòùäëïöüáéíóúç+*]+)*"
    email_regex = USER+r"\s{0,200}"+r"@"+r"\s{0,200}"+DOM       # email_regex ::= USER @ DOM. Se considera la posibilidad de que haya espacios alrededor del arroba (hasta 200 por lado).
    email_regex_TLD = USER+r"\s{0,200}"+r"@"+r"\s{0,200}"+DOM+TLD   # email_regex ::= USER @ DOM. Se considera la posibilidad de que haya espacios alrededor del arroba (hasta 200 por lado).

    pattern = re.compile(email_regex)
    matches = pattern.finditer(text)
    TLD_pattern = re.compile(email_regex_TLD)
    TLD_matches = TLD_pattern.finditer(text)

    final_tags = {'tag':[], 'palabra':[], 'start':[],'end':[]}

    for x in TLD_matches: # Nunca supimos por qué el hacerlo por extensión provocaba que tronara.
      final_tags['tag'].append(tag)
      final_tags['palabra'].append(x.group())
      final_tags['start'].append(x.start())
      final_tags['end'].append(x.end())

    for x in matches: # Nunca supimos por qué el hacerlo por extensión provocaba que tronara.
      if x.start() not in final_tags['start']: # Evita redundancias.
        final_tags['tag'].append(tag)
        final_tags['palabra'].append(x.group())
        final_tags['start'].append(x.start())
        final_tags['end'].append(x.end())

    return final_tags

  #ESTA FUNCIÓN:
  #Usa la librería regex para compilar la gramática Backus-Naur que genera números de teléfono en diversos formatos.
  #Luego los filtra asegurando que haya al menos 6 números en la cadena rescatada.
  #Finalmente regresa los tags en formato DataFrame con columnas tag, palabra, start y end. Si no hay palabras taggeadas, regresa el diccionario con listas vacías como valor.
  def tag_telefonos(self, text, tag):
    TEL = r"[0-9 -+]{6,}" #Números, pudiendo estar separados por espacios o guiones medios. Se incluye el + para casos como "+52".
    pattern = re.compile(TEL)

    NUM = r"[0-9]"
    num_pattern = re.compile(NUM) #Esto nos permitirá contar los números en el string rescatado, y evitar taggear como teléfono una secuencia aleatoria de espacios.
    matches = [x for x in pattern.finditer(text) if len(num_pattern.findall(x.group())) > 5] #len > 5 porque consideramos el caso minimal 12345678, con ocho números. De ahí, consideramos versiones mutiladas, por ejemplo con 6 números, para estar seguros.

    final_tags = {'tag':[], 'palabra':[], 'start':[],'end':[]}
    for x in matches:
      final_tags['tag'].append(tag)
      final_tags['palabra'].append(x.group())
      final_tags['start'].append(x.start())
      final_tags['end'].append(x.end())

      #text = text.replace(x.group(), " "+tag+" ")

    return final_tags


  def NERtagging(self, texto, unir_tags_iguales, mails_tag, tels_tag, nombres_tag, lugares_tag):
    # Variables referenciadas dentro de todos los procesos de etiquetamiento:
    self.separate_tags = unir_tags_iguales # Esto fue un error de dislexia. En un universo paralelo yo nombré esta variable self.unir_tags_iguales.

    if mails_tag:
      mail_tags = self.tag_emails(texto, str(mails_tag))
    else: #AÑADIR EN LA DOCUMENTACIÓN: Aguas con poner como falso la detección de un tag: será pasado por alto por el algoritmo, pudiendo detectar webs de correos como nombres o lugares.
      mail_tags = {'tag':[], 'palabra':[], 'start':[],'end':[]}

    if tels_tag:
      tel_tags = self.tag_telefonos(texto, str(tels_tag))
    else:
      tel_tags = {'tag':[], 'palabra':[], 'start':[],'end':[]}

    if self.transformer:
      self.tags = self.nlp(texto)
      transf_tags = {}
      if lugares_tag:
        transf_tags[(str(lugares_tag))] = ['B-LOC','I-LOC']
      if nombres_tag:
        transf_tags[(str(nombres_tag))] = ['B-ORG','B-PER','I-ORG','I-PER']
      if len(transf_tags) > 0:
        trans_tags = self.tag_transformer(texto, transf_tags) #Descartados por ahora: 'B-MISC','I-MISC',
      else:
        trans_tags = {'tag':[], 'palabra':[], 'start':[],'end':[]}
    else:
      trans_tags = {'tag':[], 'palabra':[], 'start':[],'end':[]}

    all_tags = {'tag':[]+mail_tags['tag']+tel_tags['tag']+trans_tags['tag'],                 #+nom_tags['tag']+lug_tags['tag'],
                'palabra':[]+mail_tags['palabra']+tel_tags['palabra']+trans_tags['palabra'], #+nom_tags['palabra']+lug_tags['palabra'],
                'start':[]+mail_tags['start']+tel_tags['start']+trans_tags['start'],         #+nom_tags['start']+lug_tags['start'],
                'end':[]+mail_tags['end']+tel_tags['end']+trans_tags['end']}                 #+nom_tags['end']+lug_tags['end']}

    all_tags = pd.DataFrame(all_tags).sort_values(by=['start']).reset_index().drop(["index"], axis=1)


    if self.separate_tags:
      to_drop = []
      la_palabra = ''
      inicier = 0
      for x in range(len(all_tags)):
        if all_tags['tag'][x] == all_tags['tag'][min(x+1,len(all_tags)-1)] and all_tags['end'][x] == all_tags['start'][min(x+1,len(all_tags)-1)]-1: # Tiene sentido iniciar el algoritmo de unificación.
          la_palabra += ' '+all_tags['palabra'][x]
          to_drop.append(min(x+1,len(all_tags)))
        elif len(la_palabra)>0:
          all_tags.loc[inicier, 'palabra'] = la_palabra + ' '+all_tags['palabra'][x]
          all_tags.loc[inicier, 'end'] = all_tags['end'][x]

          la_palabra = ''
          inicier = min(x+1,len(all_tags))
        else:
          inicier = min(x+1,len(all_tags))

      all_tags = all_tags.drop(to_drop)

    all_tags = all_tags[all_tags["palabra"].astype(str).str.len() > 1].reset_index().drop(["index"], axis=1) # Sólo conservar palabras con más de 1 caracter.

    # Tiempo de remover tags solapados. E.g. Juanito@Tokio.jp tiene los tags [NOMBRE]@[LUGAR].jp y [MAIL] al mismo tiempo
    jerarquia = {str(mails_tag):3, str(tels_tag):2, str(nombres_tag):1, str(lugares_tag):0} # Añadir a futuras versiones la posibilidad de manipular este orden.
    all_tags['jerarquía'] = all_tags['tag'].apply(lambda x:jerarquia[x]) # Genera columna auxiliar para eliminar empalmes en términos de las jerarquías de los tags.

    to_drop = [] # empalmes a eliminar, guardados por su index.
    for x in range(len(all_tags)-1):
      if all_tags['start'][x+1] < all_tags['end'][x]: # Encontrando empalmes (pero no los de Santiago NL).
        if all_tags['jerarquía'][x] < all_tags['jerarquía'][x+1]: #x-ésimo tiene menor jerarquía que el x+1-ésimo.
          to_drop.append(x)
        else: #x-ésimo tiene mayor o misma jerarquía que el x+1-ésimo.
          to_drop.append(x+1)

    all_tags = all_tags.drop(to_drop).reset_index().drop(["index", "jerarquía"], axis=1) # También quitamos la columna de Jerarquía, que la usamos sólo de manera auxiliar.


    # Enmascarar
    masked_texto = texto
    if len(all_tags) > 0:
      masked_texto  = texto[:all_tags['start'][0]] + all_tags['tag'][0]
      for x in range(len(all_tags)-1):
        masked_texto += texto[all_tags['end'][x]:all_tags['start'][x+1]] + all_tags['tag'][x+1]
      masked_texto += texto[all_tags['end'][len(all_tags)-1]:]
    #else:
      #print("ADVERTENCIA: No se encontraron entidades nombradas. Se regresa el texto original y un DataFrame vacío.")

    return masked_texto, all_tags
