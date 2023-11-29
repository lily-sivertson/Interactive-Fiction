import json
import random
import time
import os 


def find_passage(game, pid):
  if "passages" in game:
    for passage in game["passages"]:
      if pid == passage["pid"]:
        return passage
  return {}

def changetext(ptext,level):
  characters=[{ "norm":"a", "warps":["ᔑ"] },
              { "norm":"b", "warps":["ʖ"] },
              { "norm":"c", "warps":["ᓵ"] },
              { "norm":"d", "warps":["↸"] },
              { "norm":"e", "warps":["ᒷ"] },
              { "norm":"f", "warps":["⎓"] },
              { "norm":"g", "warps":["⊣"] },
              { "norm":"h", "warps":["⍑"] },
              { "norm":"i", "warps":["╎"] },
              { "norm":"j", "warps":["⋮"] },
              { "norm":"k", "warps":["ꖌ"] },
              { "norm":"l", "warps":["ꖎ"] },
              { "norm":"m", "warps":["ᒲ"] },
              { "norm":"n", "warps":["リ"] },
              { "norm":"o", "warps":["𝙹"] },
              { "norm":"p", "warps":["!¡"] },
              { "norm":"q", "warps":["ᑑ"] },
              { "norm":"r", "warps":["∷"] },
              { "norm":"s", "warps":["ᓭ"] },
              { "norm":"t", "warps":["ℸ"] },
              { "norm":"u", "warps":["⚍"] },
              { "norm":"v", "warps":["⍊"] },
              { "norm":"w", "warps":["∴"] },
              { "norm":"x", "warps":[" ̇/"] },
              { "norm":"y", "warps":["||"] },
              { "norm":"z", "warps":["⨅"] }
              #{ "norm":"", "warps":[] },
             
             ]
  words=ptext
  temp=""
  
  for i in range(len(words)):
    rnum=random.randint(0,99)
    lett=words[i:i+1]
    if rnum<=level:
      #if any(c["norm"]==lett for c in characters):
      mi = next((item for item in characters if item['norm'] == lett), None)
      if mi is None:
        temp+=lett
      else:
        temp=temp+ mi["warps"][0]
    else:
      temp=temp+lett
  print(temp)

def render(game, passage, score, moves, hea):
  print(f"------------------------------\nMoves: {moves}    Health: {hea}    Score:{score}") # make it so the health displays in diff colors based on how much there is 
  

  
  if sanity<= 30:
    print(f"Sanity:\u001b[31m {sanity}\u001b[0m")
  elif sanity<75:
    print(f"Sanity: {sanity}")
  if "name" in passage:
    print('\n\033[4m'+passage["name"]+ '\033[0m') # escapes underline the passage name

  if count!=0 and passage["pid"]=="0":
    time.sleep(2)
    print("That was such a strange dream you had. It felt so... real... You wonder what that voice could have possibly meant when it said, 'would you like to play again?' It was just a dream though, right? Either way, you don't want to dwell on it too long, so you push it away and open your eyes. \n")
    time.sleep(5)
  if "text" in passage:
    if sanity>75:
      print(passage["text"])
    elif sanity>55:
      changetext(passage["text"],5)
    elif sanity>45:
      changetext(passage["text"],10)
    elif sanity>30:
      changetext(passage["text"],15)
    elif sanity<=30:
      changetext(passage["text"],20)
    

  if "pitems" in passage: # checks if there are items you can get here
    
    for i in passage["pitems"]:
      for obs in game["items"]:
        if obs["iid"]== i["piid"] and obs not in inventory and "item-text" in i:
          if sanity>75:
            print(i["item-text"])
          elif sanity>55:
            changetext(i["item-text"],5)
          elif sanity>45:
            changetext(i["item-text"],10)
          elif sanity>30:
            changetext(i["item-text"],15)
          elif sanity<=30:
            changetext(i["item-text"],20)


  '''print(f"the drain should run at {mg} moves. currently we are at {dn} moves")
  if mg== dn: #mechanic for the drain
    if passage["pid"]=="8":
      print("You hear a loud whirring noise. Before you can register what it may be, you feel something sharp slice into you")
      global health
      health=0
    else:
      print("You hear a whirring noise in the distance")
    global dnumto
    dnumto=0
    global mgo
    mgo=random.randint(4,10)
    return "die"'''
    
    
  if "links" in passage:
    print("\nChoose one of the following (type quit to exit or inventory to open inventory. You can also type your own commands to pick up items or do certain things):")
    for link in passage["links"]:
      if "label" in link:
        print(f"  [{link['selection']}] {link['label']} ")

def get_input(passage, game):
  while True:
    global score
    global moves
    global health
    global flour
    global breadleft
    global hero 
    global sanity
    global villain
    response=input("\nWhat would you like to do?: ")
    if response.strip().upper() == "QUIT" :
      return "QUIT"
    
    if "pitems" in passage:
      for item in passage["pitems"]:
        if response.strip().lower() in item["cstr"]: 
          for i in game["items"]: #i is each item in the index of items
            if i["iid"]== item["piid"] and i not in inventory:
              if "reqi" in i: # if the item has a requiremnt to get
                reqmet= True  
                for r in i["reqi"]:
                  if not any(d['iid']==r for d in inventory):
                    reqmet=False
                    #print("requirements not met")
                    
                if reqmet==True:
                  print(f"\n{i['text']}") 
                  inventory.append(i)
                  if "scorea" in i:
                    score+= int(i["scorea"])
                    print(f"your score increases by {i['scorea']}")
                  if i["iid"]=="2":
                    flour-=1
                    #print(f"there is only {flour} flour left")
                  for th in inventory:
                    if th["iid"] in i["reqi"]:
                      inventory.remove(th)
                else:
                  print(f"\n{i['text']}")
                  
              else:
                print(f"\n{i['text']}")
                inventory.append(i)
                if "scorea" in i:
                  score+= int(i["scorea"])
                  print(f"your score increases by {i['scorea']}")
            elif i["iid"]== item ["piid"]:
              print("you already have this item.")

    '''for item in game["items"]:
      #make it so this is only called by a certain string like "make bread" or "cover knife"
      if "reqi" in item:
        reqmet= True  
        for r in item["reqi"]:
          if not any(d['iid']==r for d in inventory):
            reqmet=False
        if reqmet==True:
          print(f"\n{item['text']}") 
          inventory.append(item)
          for th in inventory:
            if th["iid"] in item["reqi"]:
              inventory.remove(th)'''
    if response.strip().lower()=="stab dinah":
      if passage["pid"] in apid:
        if any(d['iid']=="6" for d in inventory):
          print("\nYou walk up to Dinah and take out the knife from your inventory and stab her. She screams and tries to roll away, but her injuries make her unable to escape you. She dies a slow and painful death.\n ")
          time.sleep(4)
          villain+=1
          sanity-=20
          print("You look down at her carcass, wondering what to do now. Your stomach folds, reminding you just how hungry you are... and you could use the energy...")
          while True:
            response=input("\nWhat would you like to do? \n\n  [1] eat her\n  [2] ignore the carcass \n\nYour choice: ")
            if response.strip()=="1" or response.strip()=="2":
              break
          if response.strip()=="1":
            for i in range(3):
              print(".")
              time.sleep(1)
            print("You eat the remains of Dinah.")
            time.sleep(2)
            sanity-=50
            print("\nYou feel much better afterwards. You feel like you have the energy to make it out of this place, and your health goes up from the food. You gain 50 health points. ")
            passage = find_passage(game, "36")
            render(game, passage, score, moves, health)
            #response = get_input(passage, game)
            #update(game,response)
          else:
            passage = find_passage(game, "37")
            render(game, passage, score, moves, health)
        else:
          print("You have nothing to stab Dinah with.")
      
    if "breadleft" in passage:
      breadleft-=1
      if passage["breadleft"]=="hero":
        hero+=1
      elif passage["breadleft"]=="villain":
        villain+=1
        
              
    if response.strip().lower()=="make bread": #specific instructions for making bread
      reqmet=True
      item= game["items"][7]
      for r in item["reqi"]:
        if not any(d['iid']==r for d in inventory):
          reqmet=False
      if reqmet==True:
        
        moves+=1
        score+=50
        print("\n-------------------------\n You take out the ingredients you have collected from your inventory, setting them down in front of you. Then you take out your bread recipe and set it down so you can reference it.")
        time.sleep(3)
        print("\n You mix together the flour and yeast until they are well blended. Then you add the water to the mixture and stir it all together")
        time.sleep(3)
        print("\n You knead the dough until you are satisfied with your work. You then store the dough away for safekeeping in your inventory. You put the empty containers and your bread recipe back in your inventory too. You gain 50 score for your handiwork. \n--------------\n")
        
        
        inventory.append(item)
        for r in item["reqi"]:
          for iinv in inventory:
            if r==iinv["iid"] and r!="1":
              inventory.remove(iinv)
        inventory.append(game["items"][2])
        inventory.append(game["items"][3])
      else: 
        print("you do not have everything you need to make bread")
  
          
      
    if (response.strip().upper() == "INVENTORY") and (len(inventory)>0):
      print("\n\033[4mInventory\033[0m")
      for i in range(len(inventory)):
        print(f" [{i+1}] \u001b[35m{inventory[i].get('name')}\u001b[0m")
        
      while response.strip().lower()!= "close":
        response= input("\nIf you would like to take a closer look at any of the items, indicate which one by typing its name. Otherwise, type close to close the inventory: ")
        for i in range(len(inventory)):
          if response.strip().lower()==inventory[i].get("name"):
            print(f"\n\u001b[35m{inventory[i].get('name')}\u001b[0m - {inventory[i].get('desc')}")
      print("You close the inventory.")
          
    elif response.strip().upper() == "INVENTORY":
      print("There is nothing in the inventory")
      
    if "links" in passage:
      for l in passage["links"]:
        if l["selection"]== response:
          return l["pid"]
        elif "label" in l:
          if l["label"].strip().lower()==response.strip().lower():
            return l["pid"]

def update(game, response):
  return response



f = open('game.json')
game = json.load(f)
f.close()
count=0
apid=["31","32","33","34"]

sanity=100
while True:
  breadleft=4
  hero=0
  villain=0
  pid = 0
  passage = {}
  inventory= []
  response = ""
  moves=0
  health=100 
  score=0
  sanity=int((sanity+300)/4)
  flour=4
  #sanity=100
  dnumto=0
  mgo=random.randint(4,8)
  if "startnode" in game:
    pid = game["startnode"]
  
  while health>0:
    
    passage = find_passage(game, pid)
    render(game, passage, score, moves, health)
    if "hdam" in passage:  
      health-= int(passage["hdam"])
    if "score" in passage: 
      score+= int(passage["score"])
    response = get_input(passage, game )
    if response == "QUIT":
      break
    pid = update(game, response)
    moves+=1
    dnumto+=1
    if "sandam" in passage: 
      sanity-=int(passage["sandam"])

    if flour==0 and passage['pid']=="1":
      break
    if breadleft==0:
      break
  if response.strip().lower()=="quit":
    break

  #secret ending:run out of flour
  if flour==0 and passage['pid']=="1":
    time.sleep(2)
    os.system('clear')
    print("\nYou suddenly feel something change about the atmosphere around you.")
    time.sleep(3)
    print("\nYou hear a woman yell in the distance, 'what's wrong with you??!!' ")
    time.sleep(3)
    print("\n you think they are talking to you at first, but then you hear a scared voice mumble a response in reply. You cannot make out their words however")
    time.sleep(3)
    print("\nYou hear the woman yell 'I dont care!! I made it very clear that you were not to use all the flour before the 19th!! Now we don't have anything to make more bread!!!' ")
    print("\nYou think about how the flour went down everytime you took more from the pantry to make bread. You feel a bit bad that someone else is getting in trouble for you actions, but it doesn't affect you. You keep listening. ")
    time.sleep(3)
    print("\nYou hear the woman sigh in annoyance and say, 'Whatever. I knew I should have never let a fool like you into the kitchen. You never were good at anything, but I thought I would give you a chance at least. Now we'll just have to try and sell all the bread that we have in the store now.'")
    print("\n you hear the other person say something back, and then hear footsteps in the distance\n--------------------------")
    input("press enter to continue: ")
    print("\nIt is quiet for a minute. Then you hear a bell ring as a customer walks into The Bread Store. You start to resume your daily life, but something feels different about this exchange.")
    time.sleep(5)
    print("You hear the woman who was yelling and the customer talking, but you are unable to make out their words. For some reason, you feel... hopeful..")
    time.sleep(3)
    print("\nYou hear footsteps coming towards you. The next thing you know, you are being picked up and carried. You assume it is the woman who was yelling. She walks you over to another counter and sets you down in front of a stranger")
    time.sleep(3)
    print("\nThe stranger looks at you and says 'that's perfect. how much for this loaf?'")
    time.sleep(3)
    print("\nThe stranger and the woman exchange some words that mean nothing to you in your excitement. You could care less about what they are saying, it has no meaning to you. You just cant over the fact the stranger just called you perfect.")
    time.sleep(5)
    print("\n Next thing you know, you are being packaged up. The stranger picks you up and says to the woman, 'thanks for the bread, have a nice day!' ")
    time.sleep(3)
    print("\nYou have never been more excited in you life as you feel the stranger carry you forwards. \nThe stanger pauses for a moment and you hear the bell ring as the door opens. Suddenly the temperature drops, but you don't care. ")
    print("\nAll you care about is that it is November 17th, and it is the day that you have finally been sold...\n")
    
    print("\n\n Game Over.")
    input("press enter to continue...")
    for i in range(3):
      print(".")
      time.sleep(1)
    os.system('clear')
    print("\nEverything fades to darkness. You assume that it will end here, but something is keeping you here.")
    time.sleep(3)
    print("\nYou hear a voice call out your name.")
    time.sleep(2)
    print("\n\u001b[31m'Congratulations!'\u001b[0m they say.\n \u001b[31m'You managed to get sold!\u001b[0m ")
    time.sleep(2)
    print("\n\u001b[31m'I had so much fun watching you navigate through this world, I must say... I didnt think it was possible to win the game like you did so I was quite...impressed...'\u001b[0m says the voice")
    time.sleep(2)
    print("\nyou feel a bit uneasy... you are not sure how to respond to the voice so you simply ask 'do you need something?'")
    time.sleep(2)
    print("\n\u001b[31m'ah yes, my apologies... I came here to ask...'")
    time.sleep(2)
    print("\n\nconsidering how... unique... this ending is, and how much I enjoyed watching you play... well...")

  #ending villain
  elif villain==4 and breadleft==0:
    print("\n\n-------------------------\nSuddenly you feel something change about the atmosphere...")
    time.sleep(3)
    print("\nYou feel... excited...\n In the distance you can hear the bell ring on the door as a customer walks in")
    time.sleep(3)
    print("\nYou hear voices talking in the next room over. The voices stop shortly and you hear footsteps coming towards you.")
    time.sleep(3)
    print("\nA woman enters the kitchen, looks around for a bit, then picks you up and says: 'It's your lucky day I guess! I can't find any other loaves so you will have to do!'")
    time.sleep(3)
    print("\nYou are carried out of the kitchen and set on the counter in the other room in front of a stranger. She looks at you and says, 'well, this isnt the best looking loaf iv'e seen but it's fine... I guess...'")
    print("\nThe next thing you know, you are being packages up and carried out into the cold. However, you can't focus on the cold, lost in thought.")
    input("press enter to continue:")
    for i in range(3):
      print(".")
      time.sleep(1)
    os.system('clear')
    print("\nEverything fades to darkness. You are so focused on your racing thoughts that you barely even notice.")
    time.sleep(3)
    print("\nEven though you got sold, even though you sabotaged everyone else, people are still not happy with you.")
    time.sleep(3)
    print("\n\n You finally did it. You got sold, but why doesn't it feel as good as you thought it would? Why did their words sting so much? You have always known that you were not good enough... why does it bother you so much now?")
    time.sleep(4)
    print("\nYou thought it would be different when you got sold, that someone would want you, but nothing ever changes. You have never been, and never will be good enough.")
    time.sleep(4)
    print("\nIt's not fair. You have always been looking forward to this day, the day you finally got sold... You worked so hard to get here. You deserve to be happy, but everyone else is ruining it...")
    print("\n\n Game Over.")
    input("press enter to continue:")
    for i in range(3):
      print(".")
      time.sleep(1)
    os.system('clear')

    print("\nEverything fades to darkness. You assume that it will end here, but something is keeping you here.")
    time.sleep(3)
    print("\nYou hear a voice call out your name.")
    time.sleep(2)
    print("\n\u001b[31m'Congratulations on getting sold!'\u001b[0m they say.\n \u001b[31m'I always knew you could do it!! =)\u001b[0m ")
    time.sleep(2)
    print("\n\u001b[31m'I had so much fun watching you navigate through this world, I must say... I was very impressed with how ruthless you were. You really don't like others, do you? I would almost think that you enjoyed yourself, hehe'\u001b[0m says the voice")
    time.sleep(2)
    print("\nyou feel a bit uncomfortable... you reply telling the voice that you were just doing what you had to do. Thats the truth, isn't it?...")
    time.sleep(2)
    print("\nthe voice does not reply, just letting out a laugh that sends shivers down your fibers...\n\n You want it to stop so you weakly ask: 'did you, er, need something?'")
    print("\n\u001b[31m'ah yes, my apologies... I came here to ask...'")
    time.sleep(2)
    print("\n\nconsidering how you must be feeling right now... and how much fun I had watching you play my game, well...")
    
  #ending hero
  elif hero==4 and breadleft==0:
    print("\n\n-------------------------\nSuddenly you feel something change about the atmosphere...")
    time.sleep(3)
    print("\nYou feel... so hopeless...")
    time.sleep(2)
    print("\nEven though you saved all the other breads, you were never able to save yourself...")
    time.sleep(3)
    print("\nYou are starting to come to terms with it... you will never be able to make it out of this store... you don't want to be here anymore.")
    for i in range(3):
      print(".")
      time.sleep(1)
    print("\nYou let yourself give in to the exhaustion that has been plaguing you all this time. You let yourself slip into oblivion, finally ready to leave this world. At least if you cannot help yourself, you were able to help others... right?")
    input("type enter to continue: ")
    for i in range(3):
      print(".")
      time.sleep(1)
    os.system('clear')
    time.sleep(1)
    print("\nEverything fades to black around you. You expect to lose consciousness immeditiately but something is holding you back...")
    time.sleep(3)
    print("\nYou hear a voice call out to you from the darkness")
    time.sleep(3)
    print("\n\u001b[31m'Oh dear, what do we have here'\u001b[0m they say.\n \u001b[31m'Did you give up that easily?' \u001b[0m ")
    time.sleep(2)
    print("\nyou are not sure how to respond. You would like to to think that you made it a long way and made a big difference even though ultimately you couldn't save yourself. You remain silent..")
    time.sleep(4)
    print("\n\u001b[31m'Oh well. Playing the hero is so boring anyways. I would much rather watch people suffer than thrive... Plus being nice to other people never gets you anywhere...'\u001b[0m says the voice")
    time.sleep(4)
    print("\n\u001b[31m'Anyways... enough of that. The reason why I am here is to ask you a question...'\u001b[0m says the voice")
    time.sleep(3)
    print("\nYou wait expectantly for the question")
    time.sleep(2)
    
  #ending neither
  elif hero<4 and villain<4 and breadleft==0:
    print("\n\n-------------------------\nSuddenly you feel something change about the atmosphere...")
    time.sleep(3)
    print("\nYou feel... so hopeless...")
    time.sleep(2)
    print("\nYou haven't contributed anything meaningful this entire time that you have been in the bread store. You didn't save everyone, but you also did not manage to get sold... What purpose did you serve?")
    for i in range(3):
      print(".")
      time.sleep(1)
    print("\nYou pass out from exhaustion and loss of hope in the world. You will never amount to anything clearly")
    input("type enter to continue: ")
    for i in range(3):
      print(".")
      time.sleep(1)
    os.system('clear')
    time.sleep(1)
    print("\nEverything fades to black around you. You expect to lose consciousness immeditiately but something is holding you back...")
    time.sleep(3)
    print("\nYou hear a voice call out to you from the darkness")
    time.sleep(3)
    print("\n\u001b[31m'Oh dear, what do we have here'\u001b[0m they say.\n \u001b[31m'Did you give up that easily?' \u001b[0m ")
    time.sleep(2)
    print("\nyou are not sure how to respond...")
    time.sleep(4)
    print("\n\u001b[31m'Oh well. It should have been expected from soneone like you to never amount to anything... being indecisive or not committing to your goals never gets you anywhere...'\u001b[0m says the voice")
    time.sleep(4)
    print("\nYou do not know what this is supposed to mean, Youa re about to ask when the voice speaks up again.")
    print("\n\u001b[31m'Well, besides that... The reason why I am here is to ask you a question...'\u001b[0m says the voice")
    time.sleep(3)
    print("\nYou wait expectantly for the question, wanting this conversation to end already")
    time.sleep(2)

  #death sequence
  elif health<=0:
    print("\n\u001b[31mYou died.\u001b[0m ") #death print sequence
    
    print("\nHowever, you do not seem to fade away just yet...")
    time.sleep(3)
    print("\nYou feel something holding you in place for now, preventing you from slipping out of existence forever. Maybe someone is looking out for you after all.  ")
    time.sleep(5)
    print("\nYou cannot see anything around you... it's just darkness. You are just starting to wonder whether still being here is actually a good thing when you hear something call out to you. ")
    time.sleep(5)
    print("\nit asks you: ")
  
  while True:
    time.sleep(2)
    print("\n\n\u001b[31m Would you like to play again? \u001b[0m")
    response=input("\n  [1] yes\n  [2] no\n\nyour choice: ") 
    for i in range(3):
      print(".")
      time.sleep(1)
    if response.strip().lower()=="yes" or response=="1":
      print("\u001b[31mgood luck then... I can't wait to see what you will do this time, knowing what you do now =)...\u001b[0m")
      time.sleep(3)
      os.system('clear')
      time.sleep(1)
      count+=1
      break
    elif response.strip().lower()=="no" or response=="2":
      print("\u001b[31m I see. Bye bye for now then... I hope I will see you again in some other lifetime... I had so much fun watching you... play my game \u001b[0m")
      break
    else:
      print("that is not an answer... I'll ask you once again...")
  if response.strip()=="2" or response.strip().lower()=="no":
    break
  
print("Thanks for playing!")
