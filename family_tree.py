from graphviz import Digraph

class Person(object):

    def __init__(self, values,index):
        self.first_name = values['Prénom']
        self.last_name = values['Nom']
        self.birth_date = values['Date de naissanace']
        self.father_name = values['Prénon père']
        self.gender = values['Sexe']
        self.index = str(index)
        self.father = None

    def set_father(self,father):
        self.father = father

    def get_fathers_names(self):
        fathers = str(self.father_name).strip()
        fathers = fathers.split("بن")
        fathers = [x.strip() for x in fathers]
        return fathers

class Family(object):
    members = []
    count = 0

    def populate(self, rows):
        for row in rows:
            person = Person(row, self.count)
            self.count += 1
            self.members.append(person)

    def build_tree(self):
        dot = Digraph(comment='Family Tree',
                      node_attr={'style': 'filled'})
        for person in self.members:
            if person.gender == 'انثى':
                dot.node(person.index, person.first_name + r'\n' + str(person.birth_date), color='#ffadef')
            else:
                dot.node(person.index, person.first_name + r'\n' + str(person.birth_date), color='lightblue2')

        for person in self.members:
            if person.father != None:
                j = person.father.index
                k = person.index
                dot.edge(j, k)

        return dot

    def sort_family(self, reverse):
        def myFunc(e):
            return e.birth_date

        sorted = self.members
        return sorted.sort(key=myFunc, reverse=reverse)

    def find_father(self, member):
        if member.father == None and member.father_name != '':
            father = None
            for person in self.members:
                if self.is_the_same(member, person):
                    continue
                else:
                    if member.birth_date <= person.birth_date:
                        continue
                    else:
                        if member.father_name != person.first_name:
                            continue
                        else:
                            father = person
                            break

            if father == None:
                father == self.find_father_from_self(member)
            member.set_father(father)

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
        print()
        self.count += 1
        self.members.append(father)
        member.set_father(father)

        if (fathers_names):
            self.find_father_from_self(father)
        return father

    def is_the_same(self, member1, member2):
        if member1.first_name == member2.first_name \
                and member1.birth_date == member2.birth_date \
                and member1.father_name == member2.father_name:
            return True
        else:
            return False