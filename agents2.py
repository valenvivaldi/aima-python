from agents import *


# DEFINCION DEL AGENTE
class Aspiradora(Agent):
    location = random.randint(0,1)
    print("las aspiradora inicia en location {}".format(location))

    def moveright(self):
        self.location += 1

    def moveleft(self):
        self.location -= 1

    def suck(self, thing):
        '''returns True upon success or False otherwise'''
        if isinstance(thing, Dirt):
            return True
        return False


# DEFINICION DEL ENVIROMENT Y LAS COSAS

class Dirt(Thing):
    pass


class Floor(Environment):
    def percept(self, agent):
        '''return a list of things that are in our agent's location'''
        things = self.list_things_at(agent.location)
        return things

    def execute_action(self, agent, action):
        '''changes the state of the environment based on what the agent does.'''
        if action == "moveright":
            print('{} esta en {} y decide moverse a la derecha'.format(str(agent)[1:-1], agent.location))
            agent.moveright()
        elif action == "moveleft":
            print('{} esta en {} y decide moverse a la izquierda'.format(str(agent)[1:-1], agent.location))
            agent.moveleft()
        elif action == "suck":
            items = self.list_things_at(agent.location, tclass=Dirt)
            if len(items) != 0:
                if agent.suck(items[0]):  # Have the dog eat the first item
                    print('{} aspiro {} en la posicion: {}'
                          .format(str(agent)[1:-1], str(items[0])[1:-1], agent.location))
                    self.delete_thing(items[0])  # Delete it from the Park after.

    def is_done(self):
        result = not any(isinstance(thing, Dirt) for thing in self.things)
        if result:
            print("¡¡¡la aspiradora limpió todo el piso!!!")
        return result


def program(percepts):
    '''Returns an action based on the dog's percepts'''
    for p in percepts:
        if isinstance(p, Dirt):
            return 'suck'

    if roomba.location == 0: # location 0 is left, location 1 is right
        return 'moveright'
    else:
        return 'moveleft'


piso = Floor()

suciedad = Dirt()
suciedad2 = Dirt()

roomba = Aspiradora(program)
piso.add_thing(roomba, roomba.location)

piso.add_thing(suciedad, 0)
piso.add_thing(suciedad2, 1)


piso.run(5)
