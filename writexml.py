from XMLGenerator import XMLGenerator
import yaml
import os
from random import choice
'''
bookstore = XMLGenerator("book_store.xml")

node_book_store = bookstore.createNode("bookstore")
bookstore.setNodeAttr(node_book_store,"name","new hua")
bookstore.setNodeAttr(node_book_store,"website","http://www.ourunix.org")
bookstore.addNode(node = node_book_store)

node_book_01 = bookstore.createNode("book1")
node_book_01_name = bookstore.createNode("name")
bookstore.setNodeValue(node_book_01, "hello")
bookstore.setNodeValue(node_book_01_name, "Hamlet")
bookstore.addNode(node_book_01_name, node_book_01)

node_book_01_author = bookstore.createNode("author")
bookstore.setNodeValue(node_book_01_author, "Wiliam Shakespeare")
bookstore.addNode(node_book_01_author, node_book_01)

bookstore.addNode(node_book_01, node_book_store)

bookstore.genXml()
'''

ori_path = "/Users/dyh127/Desktop/project/trecvid_actev/annotations"
type_yml = "VIRAT_S_000000.types.yml"
act_yml = "VIRAT_S_000000.activities.yml"
geom_yml = "VIRAT_S_000000.geom.yml"
region_yml = "VIRAT_S_000000.activities.yml"
save_xml = "VIRAT_S_000000.xml"

type_path = os.path.join(ori_path, type_yml)
act_path = os.path.join(ori_path, act_yml)
geom_path = os.path.join(ori_path, geom_yml)
region_path = os.path.join(ori_path, region_yml)

f = open(type_path)
y = yaml.load(f)
f.close()
object_type_dict = {}
for type in y:
    if type.keys()[0] == 'types':
        id1 = type.values()[0]["id1"]
        cset3 = type.values()[0]["cset3"].keys()[0]
        object_type_dict.update({id1:cset3})

f = open(act_path)
y = yaml.load(f)
f.close()
object_act_dict = {}
act_type_dict = {}
count = 0
for act in y:
    if act.keys()[0] == 'act':
        #print act.values()[0]['actors']
        id2 = act.values()[0]['id2']
        act2 = act.values()[0]['act2'].keys()[0]
        if id2 not in act_type_dict.keys():
            act_type_dict.update({id2:act2})
        for actor in act.values()[0]['actors']:
            count += 1
            id1 = actor['id1']
            timespan = actor['timespan'][0].values()[0]
            if id1 not in object_act_dict.keys():
                object_act_dict[id1] = {}
            object_act_dict[id1].update({id2:timespan})
#for q in object_act_dict.keys():
#    print object_act_dict[q]

f = open(geom_path)
y = yaml.load(f)
f.close()
bbox_dict = {}
for geom in y:
    #print geom
    if geom.keys()[0] == 'geom':
        id1 = geom.values()[0]['id1']
        ts0 = geom.values()[0]['ts0']
        g0 = geom.values()[0]['g0']
        g0 = g0.split(' ')
        #print g0
        if id1 not in bbox_dict.keys():
            bbox_dict.update({id1:{}})
        bbox_dict[id1].update({ts0:g0})
#for object_id in bbox_dict.keys():
#    print bbox_dict[object_id]

annotation = XMLGenerator(save_xml)
annotation_node = annotation.createNode('annotation')
annotation.addNode(node = annotation_node)
for id1 in sorted(object_type_dict.keys()):
    track = annotation.createNode('track')
    annotation.setNodeAttr(track,'label','object')
    annotation.setNodeAttr(track,'id',str(id1))
    count = 0
    for frame in sorted(bbox_dict[id1].keys()):
        count += 1
        box = annotation.createNode('box')
        keyframe_value = '0'
        if count == 1 or count == len(bbox_dict[id1].keys()) or count % 20 == 0:
            keyframe_value = '1'
        if id1 in object_act_dict.keys():
            for id2 in object_act_dict[id1].keys():
                if str(frame) == str(object_act_dict[id1][id2][0]) or str(frame) == str(object_act_dict[id1][id2][1]):
                    keyframe_value = '1'
        annotation.setNodeAttr(box, 'keyframe', keyframe_value)
        annotation.setNodeAttr(box, 'occluded', '0')
        outside_value = '0'
        if count == len(bbox_dict[id1].keys()):
            outside_value = '1'
        annotation.setNodeAttr(box, 'outside', outside_value)
        g0 = bbox_dict[id1][frame]
        annotation.setNodeAttr(box, 'xtl', g0[0])
        annotation.setNodeAttr(box, 'ytl', g0[1])
        annotation.setNodeAttr(box, 'xbr', g0[2])
        annotation.setNodeAttr(box, 'ybr', g0[3])
        annotation.setNodeAttr(box, 'frame', str(frame))

        attribute = annotation.createNode('attribute')
        annotation.setNodeAttr(attribute, 'name', 'type')
        annotation.setNodeValue(attribute, object_type_dict[id1])
        annotation.addNode(attribute, box)

        id2_here = -1
        if id1 in object_act_dict.keys():
            for id2 in object_act_dict[id1].keys():
                if frame in range(object_act_dict[id1][id2][0], object_act_dict[id1][id2][1] + 1):
                    id2_here = id2
                    break
        if id2_here == -1:
            act_type = '__undefined__'
        else:
            act_type = act_type_dict[id2_here]
        attribute = annotation.createNode('attribute')
        annotation.setNodeAttr(attribute, 'name', 'actNum')
        annotation.setNodeValue(attribute, str(id2_here))
        annotation.addNode(attribute, box)

        attribute = annotation.createNode('attribute')
        annotation.setNodeAttr(attribute, 'name', 'actType')
        annotation.setNodeValue(attribute, act_type)
        annotation.addNode(attribute, box)

        annotation.addNode(box, track)
    annotation.addNode(track, annotation_node)
annotation.genXml()
