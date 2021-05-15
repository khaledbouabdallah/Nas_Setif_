from graphviz import Digraph


# Class represnte one person
class Person(object):

    # Create a new Person
    def __init__(self, values, index):
        self.first_name = values['Prénom']
        self.last_name = values['Nom']
        self.birth_date = values['Date de naissanace']
        self.father_name = values['Prénon père']
        self.gender = values['Sexe']
        self.index = str(index)
        self.father = None

    # set father(Person)
    def set_father(self, father):
        self.father = father

    # return father name as a list of ancestors
    def get_fathers_names(self):
        fathers = str(self.father_name).strip()
        fathers = fathers.split("بنت")
        fathers = " بن ".join(fathers)
        fathers = fathers.split("بن")
        fathers = [x.strip() for x in fathers]
        return fathers


# Class reresente a group of people that have father-son relationship
class Family(object):
    # family start with 0 members
    members = []
    count = 0

    # populate the family from a list of Persons
    def populate(self, rows):
        for row in rows:
            person = Person(row, self.count)
            self.count += 1
            self.members.append(person)

    # build tree model using the father relationship
    def build_tree(self):

        dot = Digraph(comment='Family Tree',
                      node_attr={'style': 'filled'})
        # create nodes of family memebers (pink : females / blue : males)
        for person in self.members:
            if person.gender == 'انثى':
                dot.node(person.index, person.first_name + r'\n' + str(person.birth_date), color='#ffadef')
            else:
                dot.node(person.index, person.first_name + r'\n' + str(person.birth_date), color='lightblue2')
        # draw edges between nodes using father relationship
        for person in self.members:
            if person.father != None:
                j = person.father.index
                k = person.index
                dot.edge(j, k)

        return dot

    # sort family from young to old
    def sort_family(self, reverse):
        def myFunc(e):
            return e.birth_date

        sorted = self.members
        return sorted.sort(key=myFunc, reverse=reverse)

    # find the father of a person in this family
    def find_father(self, member):
        if member.father == None and member.father_name != '':
            father = None
            for person in self.members:
                print('****')
                print('member father name:' + member.get_fathers_names()[0])
                print('person first name :' + person.first_name)
                print('member ansestors :' + " بن ".join(member.get_fathers_names()[1:]))
                print('person ansestors :' + " بن ".join(person.get_fathers_names()))
                if self.is_the_same(member, person):
                    print(1)
                    continue
                else:
                    if member.birth_date <= person.birth_date:
                        print(2)
                        continue
                    else:
                        example1 = member.get_fathers_names()[1:]
                        example2 = person.get_fathers_names()
                        example2 = example2[:len(example1)]
                        if person.first_name == member.get_fathers_names()[0] \
                                and \
                                " بن ".join(example1) == " بن ".join(example2):
                            print(3)
                            father = person
                            break

            if father == None:
                pass

            if father == None:
                self.find_father_from_self(member)
                return "new member"
            else:
                member.set_father(father)
                return 'no new member'
        else:
            return 'already has father'

    def add_fathers(self):

        self.sort_family(False)
        i = 0
        family_lenth = len(self.members)
        while i < family_lenth:
            print('----------')
            print(self.members[i].first_name)
            new = self.find_father(self.members[i])
            if self.members[i].father:
                print(self.members[i].father.first_name)
            print(new)
            if new == 'new member':
                i = 0
                family_lenth = len(self.members)
                self.sort_family(False)
            elif new == 'no new member':
                i += 1
                pass
            else:
                i += 1

    # set the father of a person from the father name column
    def find_father_from_self(self, member):

        fathers_names = member.get_fathers_names()
        father_name = fathers_names.pop(0)

        new_fathers_names = " بن ".join(fathers_names)
        father_info = {'Nom': member.last_name,
                       'Prénom': father_name,
                       'Date de naissanace': member.birth_date - 20,
                       'Prénon père': new_fathers_names,
                       'Sexe': 'ذكر', }

        father = Person(father_info, index=self.count)
        self.count += 1
        member.set_father(father)
        self.members.append(father)

    # return true of two persons have the same informations
    def is_the_same(self, member1, member2):
        if member1.first_name == member2.first_name \
                and member1.birth_date == member2.birth_date \
                and member1.father_name == member2.father_name:
            return True
        else:
            return False