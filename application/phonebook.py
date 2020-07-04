#######################################
# Program to read and show a phone book from AVM Fritz!Box XML export
# multiple entries for a phone category e.g. 'mobile' will not shown yet
# written by Hermann12, in Corona short time work
# class will be called from vCard_Reader, if you open a avm_phonebook.xml
#######################################
class PhoneBook:
    """The XML phone book parse """
    
    def __init__(self, tree):
        self.tree = tree
        self.address()

        
    def address(self):
        contact_items=[]
        contact_item={}
        names=[]
        phone_dic={}
        for contacts in self.tree.iter(tag='phonebook'):
            for contact in contacts.findall("./contact"):       
                for category in contact.findall("./category"):
                    category=category.text
             
                for person in contact.findall("./person/realName"):
                    print('realName: ',person.text)
                    names.append(person.text)
                    
                for uniqueid in contact.findall("./uniqueid"):
                    print('uniqueid: ',uniqueid.text)
                    phone_dic[uniqueid.text] = person.text
                    contact_item[uniqueid.text] = person.text
                    
                for telephony in contact.findall("./telephony"):
                    for number in telephony.findall("./number"):
                        if number.attrib['type'] == 'home':
                            print('home: ',number.text)
                            contact_item['home']=number.text
                        if number.attrib['type'] == 'mobile':
                            print('mobile: ',number.text)
                            contact_item['mobile']=number.text
                        if number.attrib['type'] == 'work':
                            print('work: ',number.text)
                            contact_item['work']=number.text
                    contact_items.append(contact_item)
                    print(contact_items)
                contact_item={}
            
                        
                    
            print(phone_dic)
            print(sorted(names))
            phone_dict2 = {y:x for x,y in phone_dic.items()} # dict2 ist reverse wegen bug.
        return phone_dic, contact_items

"""
########## for testing only
import xml.etree.ElementTree as ET
#tree = ET.ElementTree(file='Telefonkontakte iPhone K 04.07.20 12-54.xml')
tree = ET.ElementTree(file='FRITZ.Box_Telefonbuch_19.06.20_1815.xml')
root = tree.getroot()
print(root)
PhoneBook(tree)
"""

