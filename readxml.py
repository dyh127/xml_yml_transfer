from xml.dom import minidom
import yaml
import os

ori_path = "/home/dingyuhang/annotations"
xml_name = "12_test.xml"

xml_path = os.path.join(ori_path, xml_name)
dom = minidom.parse(xml_path)

root = dom.documentElement
print root.nodeName
print root.nodeValue
print root.nodeType

trackNodes = root.getElementsByTagName('track')
geom_list = []
type_list = []
act_list = []
act_type_dict = {}
object_type_dict = {}
act_object_frame_dict = {}
id0 = 0
for track in trackNodes:
    id1 = track.getAttribute('id')
    boxNodes = track.getElementsByTagName('box')
    typeNode = boxNodes[0].getElementsByTagName('attribute')[0]
    type = typeNode.childNodes[0].data
    if id1 not in object_type_dict.keys():
        object_type_dict.update({id1:type})
    for box in boxNodes:
        geom_frame_dict = {'geom': {'src': 'truth','id1':id1}}
        geom_frame_dict['geom'].update({'id0':id0})
        frame = box.getAttribute('frame')
        ts1 = float(frame)/30.0
        xtl = box.getAttribute('xtl')
        ytl = box.getAttribute('ytl')
        xbr = box.getAttribute('xbr')
        ybr = box.getAttribute('ybr')
        g0 = (' ').join([xtl,ytl,xbr,ybr])
        geom_frame_dict['geom'].update({'ts0':int(frame),'ts1':ts1,'g0':g0})
        actNumNode =  box.getElementsByTagName('attribute')[1]
        actNum = actNumNode.childNodes[0].data
        actTypeNode = box.getElementsByTagName('attribute')[2]
        actType = actTypeNode.childNodes[0].data
        if actNum not in act_type_dict.keys():
            act_type_dict.update({actNum:actType})
        geom_list.append(geom_frame_dict)
        if actNum not in act_object_frame_dict.keys():
            act_object_frame_dict[actNum] = {}
        if id1 not in act_object_frame_dict[actNum].keys():
            act_object_frame_dict[actNum][id1] = []
        act_object_frame_dict[actNum][id1].append(int(frame))

for id2 in act_object_frame_dict.keys():
    act_dict_here = {'act':{'act2':{act_type_dict[id2]:1.0},'id2':id2,'src':'truth','actor':{}}}
    id1_list = act_object_frame_dict[id2].keys()
    for id1 in id1_list:
        minFrame = min(act_object_frame_dict[id2][id1])
        maxFrame = max(act_object_frame_dict[id2][id1])
        timespan = [minFrame, maxFrame]
        act_dict_here['act']['actor'].update({'id1':id1,'timespan':{'tsr0':timespan}})
    act_dict_here['act'].update({'timespan':timespan})
    act_list.append(act_dict_here)


for id1 in object_type_dict.keys():
    type = object_type_dict[id1]
    type_id1_dict = {'types':{'id1':id1,'cset3':{type:1.0}}}
    type_list.append(type_id1_dict)



geom_name = 'test.geom.yml'
geom_path = os.path.join(ori_path, geom_name)
f = open(geom_path, 'w')
yaml.safe_dump(geom_list,f,encoding='utf-8',allow_unicode=True)
f.close()

type_name = 'test.type.yml'
type_path = os.path.join(ori_path, type_name)
f = open(type_path, 'w')
yaml.safe_dump(type_list, f,encoding='utf-8',allow_unicode=True)
f.close()

act_name = 'test.activity.yml'
act_path = os.path.join(ori_path, act_name)
f = open(act_path, 'w')
yaml.safe_dump(act_list, f, encoding='utf-8',allow_unicode=True)
f.close()
